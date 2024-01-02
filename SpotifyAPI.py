import base64
import requests
import os 


client_id = "2a6eb9ff85b24a5a9d7b4913bcf54021"
client_secret = "cfb7da66032d4ca6927dfbc4468e9e67"


def get_token(client_id,client_secret) :
    auth_str = f"{client_id}:{client_secret}"
    b64_auth_str = base64.urlsafe_b64encode(auth_str.encode()).decode()

    headers = {
        "Authorization": f"Basic {b64_auth_str}",
    }

    data = {
        "grant_type": "client_credentials",
    }

    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    response_data = response.json()
    return response_data["access_token"]

def new_token() :
    global access_token 
    access_token = get_token(client_id,client_secret)

new_token()
def get_lyrics(artist_name, track_name):
    API_KEY = '0802f6108be14a466f034ffe151465f1'
    base_url = 'https://api.musixmatch.com/ws/1.1/'
    search_url = f'{base_url}track.search'
    search_params = {
        'q_artist': artist_name,
        'q_track': track_name,
        'apikey': API_KEY
    }

    response = requests.get(search_url, params=search_params)
    data = response.json()

    if data['message']['body']['track_list']:
        track_id = data['message']['body']['track_list'][0]['track']['track_id']
        lyrics_url = f'{base_url}track.lyrics.get'
        lyrics_params = {
            'track_id': track_id,
            'apikey': API_KEY
        }

        response = requests.get(lyrics_url, params=lyrics_params)
        lyrics_data = response.json()

        if 'lyrics' in lyrics_data['message']['body']:
            lyrics = lyrics_data['message']['body']['lyrics']['lyrics_body']
            return lyrics.strip().split("*******")[0]
        else:
            return "Lyrics not found."
    else:
        return "Lyrics not found."

def search_song(song_name):
    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    params = {
        "q": song_name,
        "type": "track",
        "limit": 1,
    }

    response = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)
    response_data = response.json()
    # Extract details of the first result
    if response_data["tracks"]["items"]:
        first_result = response_data["tracks"]["items"][0]
        for i in first_result["artists"]:
            ly=get_lyrics(i["name"],first_result["name"])
            print(ly)
            if ly:
                if ly not in ["Lyrics not found.","Track not found."," ",""]:
                    break
                else:
                    continue
        f=open("playlist/lyrics.txt","a",encoding='utf-8')
        f.write(" ".join(ly.split('\n'))+'\n')
        f.close()
        song_details = {
            "name": first_result["name"],
            "artists": [artist["name"] for artist in first_result["artists"]],
            "year": first_result["album"]["release_date"].split("-")[0],
            "album": first_result["album"]["name"],
            "popularity": first_result["popularity"],
            "track_id": first_result["id"],  # Adding the track ID to the song_details
        }
        return song_details
    else:
        return None
    

def get_audio_features(track_id):
    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    response = requests.get(f"https://api.spotify.com/v1/audio-features/{track_id}", headers=headers)
    features_data = response.json()

    return features_data



def get_metadata(song_name):
    song_details = search_song(song_name)
    

    if song_details:
        track_id = song_details["track_id"]
        audio_features = get_audio_features(track_id)
        song_details["audio_features"] = audio_features  # Adding audio features to song_details
        #add genre to the song details dictionary
        print(song_details)
        return song_details
    
    return None

'''
song_name = "Thalaivar Hukum"
song_details = get_metadata(song_name)
print (song_details)

if song_details:
    print("Song Name:", song_details["name"])
    print("Artists:", ", ".join(song_details["artists"]))
    print("Album:", song_details["album"])
    print("Release Date:", song_details["release_date"])
    print("Audio Features:", song_details["audio_features"])
'''