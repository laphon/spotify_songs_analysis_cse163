"""
This Python file converts kpop_music_video.csv to
a dataset containing audio features using Spotify Web API.
Note that we have already generated a new dataset named
"spotify_kpop_songs.csv" with this following code already.
Recently, the API did not work like we expected anymore,
running this code will likely catch an error.
"""

from spotify_api import SpotifyAPI
import pandas as pd


# Gain access to Spotify's web API
# Modify according to your Spotify account
client_id = 'f34a2b94b177430db63de55bd4ace397'
client_secret = '8ce9f339845945c0a2822c99630d1bea'
spotify = SpotifyAPI(client_id, client_secret)


def is_kpop(_id):
    """
    Returns 1 if the song with _id is a k-pop song.
    Otherwise, returns 0.
    """
    track = spotify.get_track(_id)
    artists = track['album']['artists']
    genres = set()
    for artist in artists:
        artist_id = artist['id']
        genres.update(spotify.get_artist(artist_id)['genres'])
    if 'k-pop' in genres:
        return 1
    return 0


def search_kpop_songs(df):
    """
    Returns a list of k-pop songs from df that are found on Spotify.
    """
    found_ids = []
    for name in df['Song Name'].tolist():
        found = spotify.search(name, search_type='track')
        found_items = found['tracks']['items']
        if len(found_items) != 0:
            _id = found_items[0]['id']
            found_ids.append(_id)
    return found_ids


def kpop_dataframe(input_ids):
    """
    Creates a dataframe of k-pop songs with necessary features.
    """
    all_columns = {"name": [], "id": [], "artists": [], "genres": [],
                   'explicit': [], "release_date": [], "popularity": [],
                   'danceability': [], 'energy': [], 'key': [],
                   'loudness': [], 'mode': [], 'speechiness': [],
                   'acousticness': [], 'instrumentalness': [], 'liveness': [],
                   'valence': [], 'tempo': [], 'duration_ms': []}
    for _id in input_ids:
        if is_kpop(_id):
            # general
            all_columns['id'].append(_id)
            track = spotify.get_track(_id)
            all_columns['name'].append(track['name'])
            all_columns['release_date'].append(track['album']['release_date'])
            all_columns['popularity'].append(track['popularity'])
            all_columns['explicit'].append(track['explicit'])
            artists = []
            genres = set()
            for artist in track['artists']:
                artists.append(artist['name'])
                artist_id = artist['id']
                genres.update(spotify.get_artist(artist_id)['genres'])
            all_columns['artists'].append(artists)
            all_columns['genres'].append(genres)
            # audio_features
            required = ['danceability', 'energy', 'key',
                        'loudness', 'mode', 'speechiness',
                        'acousticness', 'instrumentalness', 'liveness',
                        'valence', 'tempo', 'duration_ms']
            audio_features = spotify.get_audio_features(_id)
            for feature in required:
                all_columns[feature].append(audio_features[feature])
    return pd.DataFrame(data=all_columns)


def convert_to_dataset(kpop_songs, target):
    """
    Generate a dataset with kpop_songs dataframe
    and save to a new csv file
    """
    found_ids = search_kpop_songs(kpop_songs)
    spotify_kpop_songs = kpop_dataframe(found_ids)
    spotify_kpop_songs.to_csv(target, sep=',', index=False)


def main():
    # Generate a dataset with kpop songs and save to a new csv file.
    # This process takes a very long time.
    kpop_songs = pd.read_csv("source_files/kpop_music_videos.csv")
    target = "source_files/spotify_kpop_songs.csv"
    convert_to_dataset(kpop_songs, target)


if __name__ == "__main__":
    main()
