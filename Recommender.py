from collections import defaultdict
from sklearn.metrics import euclidean_distances
from scipy.spatial.distance import cdist
import difflib
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import pandas as pd

def write_recommended():
    song_cluster_pipeline = Pipeline([('scaler', StandardScaler()), 
                                  ('kmeans', KMeans(n_clusters=20, 
                                   verbose=False))
                                 ], verbose=False)

    data = pd.read_csv('MusicData.csv')
    library = pd.read_csv('metadata/MusicData.csv')

    X = data.select_dtypes(np.number)
    number_cols = list(X.columns)
    song_cluster_pipeline.fit(X.values)
    song_cluster_labels = song_cluster_pipeline.predict(X.values)
    data['cluster_label'] = song_cluster_labels


    def get_mean_vector(song_list, spotify_data):
    
        song_vectors = []
    
        song_vectors = song_list[number_cols].apply(lambda x: x.to_list(), axis=1).tolist()
    
        song_matrix = np.array(list(song_vectors))
        return np.mean(song_matrix, axis=0)


    def flatten_dict_list(dict_list):
    
        flattened_dict = defaultdict()
        for key in dict_list[0].keys():
            flattened_dict[key] = []
    
        for dictionary in dict_list:
            for key, value in dictionary.items():
                flattened_dict[key].append(value)

        return flattened_dict


    def recommend_songs(song_list, spotify_data,song_list_to_dict, n_songs=10):
    
        metadata_cols = ['name', 'year', 'artists']
        song_dict = flatten_dict_list(song_list_to_dict)
    
        song_center = get_mean_vector(song_list, spotify_data)
        scaler = song_cluster_pipeline.steps[0][1]
        scaled_data = scaler.transform(spotify_data[number_cols].values)
        scaled_song_center = scaler.transform(song_center.reshape(1, -1))
        distances = cdist(scaled_song_center, scaled_data, 'cosine')
        index = list(np.argsort(distances)[:, :n_songs][0])
    
        rec_songs = spotify_data.iloc[index]
        rec_songs = rec_songs[~rec_songs['name'].isin(song_dict['name'])]
        return rec_songs[metadata_cols].to_dict(orient='records')

        # Filter the DataFrame to select only the 'Name' and 'Year' columns
    filtered_df = library[['name', 'year']]

    # Convert the filtered DataFrame to a list of dictionaries
    result_list = filtered_df.to_dict(orient='records')

    # Rename the keys to match the desired format
    song_list_to_dict = [{'name': item['name'], 'year': item['year']} for item in result_list]

    songs=recommend_songs(library, data , song_list_to_dict)
    f=open("metadata/recommended_songs.txt","w")
    for i in songs:
        f.write(i['name']+'|'+i['artists']+'\n')
    f.close()
