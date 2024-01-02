import requests

API_KEY = '0802f6108be14a466f034ffe151465f1'
song_lyrics={}

def get_lyrics(artist_name, track_name):
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
        return "Track not found."
print(get_lyrics("Aalap Raju","Chinna Chinna"))