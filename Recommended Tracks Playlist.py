import json
import requests
import pandas as pd

# Change to your own user ID
# Get an OAuth Token from here https://developer.spotify.com/console/post-playlists/?user_id=&body=%7B%22name%22%3A%22New%20Playlist%22%2C%22description%22%3A%22New%20playlist%20description%22%2C%22public%22%3Afalse%7D
# Tick both private and public playlist editing

USER_ID = "" 
ACCESS_TOKEN = 'BQA03ry80XJU23zHAIAae-owu6RkJuMQoABm_ABn-C4Gps77oKtYwPUWDuifiOGwxq3ocrfUT_Z9kEA5W96byEZ3EQg-zhPfJ59w5aDUn8kDaE6i-EiXEmkcscZ0aix-Y5qcGafjEtBYPdB5luHLseRzZMQnDJnE7cz_IsDtJ5Eg81R1Jyu65hHiHZgic7eHfHQzPT9Tth8Lg163B4UvZSq3waIRm9ntUf9JFgfwKoD-tQ'

# Get Recommendation Seeds

CREATE_PLAYLIST_URL = 'https://api.spotify.com/v1/users/' + USER_ID + '/playlists'
# print(ADD_TO_PLAYLIST_URL)

def conversion (strsample):
    
    strsample = strsample.replace(":", "%3A")
    strsample = strsample.replace(",", "%2C")
    strsample = strsample.replace(" ", "%20")
    return strsample


def search_song (song, artist):

    if song != '' and artist != '':
        song = conversion(song)
        artist = conversion(artist)
        SEARCH_URL = "https://api.spotify.com/v1/search?q=track%3A"+ song + "%20artist%3A" + artist + "&type=track&artist%3A&market=ES"
    elif song == '':
        artist = conversion(artist)
        SEARCH_URL = "https://api.spotify.com/v1/search?q=artist%3A" + artist + "&type=track&artist%3A&market=ES"
    elif artist == '':
        song = conversion(song)
        SEARCH_URL = "https://api.spotify.com/v1/search?q=track%3A"+ song + "&type=track&artist%3A&market=ES"
    
    search = requests.get(
        SEARCH_URL, 
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        }        
    )
    print(SEARCH_URL)
    json_search = search.json()
    with open("search_result.json", "w") as jsonfile:
        json.dump(json_search, jsonfile)
    return json_search

def search_artist (artistURI):
    SEARCH_ARTIST_URL = "https://api.spotify.com/v1/artists/" + artistURI

    response = requests.get(
        SEARCH_ARTIST_URL,
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        }
    )
    json_artist = response.json()
    with open("artist_search.json", "w") as jsonfile:
        json.dump(json_artist, jsonfile)
    return json_artist
def get_recommendation (artistURI, artist_genre, songURI):

    print(artistURI)
    print(artist_genre)
    print(songURI)

    LIMIT = "10"
    SEED_ARTIST = artistURI
    SEED_GENRES = artist_genre
    SEED_TRACKS = songURI
    MARKET = "ES"

    GET_RECOMMENDATION_URL = 'https://api.spotify.com/v1/recommendations?limit='+ LIMIT + '&market=' + MARKET + '&seed_artists=' + SEED_ARTIST + '&seed_genres=' + SEED_GENRES + '&seed_tracks=' + SEED_TRACKS
    print(GET_RECOMMENDATION_URL)
    recommendation = requests.get(
        GET_RECOMMENDATION_URL, 
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        }        
    )
    json_reco = recommendation.json()

    with open("recommendations.json", "w") as jsonfile:
        json.dump(json_reco, jsonfile)
    
    return json_reco

def add_to_playlist (songs, playlistID):
    PLAYLIST_ID = playlistID
    ADD_TO_PLAYLIST_URL = 'https://api.spotify.com/v1/playlists/' + PLAYLIST_ID + '/tracks'
    response = requests.post(
        ADD_TO_PLAYLIST_URL+'?uris=' + songs,
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        }       
        
    )
    json_resp = response.json()
    return json_resp

def create_playlist (name, public):
    response = requests.post(
        CREATE_PLAYLIST_URL, 
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        },
        json = {
            "name": name,
            "public": public
        }        
    )
    json_resp = response.json()
    with open("playlist_info.json", "w") as jsonfile:
        json.dump(json_resp, jsonfile)
    return json_resp

# https://api.spotify.com/v1/playlists/3cEYpjA9oz9GiPac4AsH4n/tracks?uris=spotify%3Atrack%3A4iV5W9uYEdYUVa79Axb7Rh%2Cspotify%3Atrack%3A1301WleyT98MSxVHPZCA6M
def main():
    song = "Betty Get Money"
    artist = ""
    sample1 = []
    strsample = ''
    
    songsearch = search_song(song, artist)

    # Song search process
        # Always picking the first result
    song = str(songsearch["tracks"]["items"][0]["name"])
    songuri = songsearch["tracks"]["items"][0]["uri"][14:]
    artisturi = songsearch["tracks"]["items"][0]["artists"][0]["uri"][15:]

    # search_artist
    artistsearch = search_artist(artisturi)

    # genre
    artist_genre = artistsearch["genres"]
    artist_genre = ",".join(artist_genre)
    print(artist_genre)

    newplaylist = create_playlist(
        name = "My Private Test Playlist Based on " + song,
        public = False
    )
    playlistID = newplaylist["uri"][17:]

    Recommendations = get_recommendation(artisturi, artist_genre, songuri)

    for items in Recommendations["tracks"]:
        sample1.append(items["uri"])

    for items in sample1:
        strsample = strsample + ',' + items
    strsample = strsample[1:]
    strsample = conversion(strsample)
    
    add_to_playlist(
        songs = strsample,
        playlistID = playlistID
    )

if __name__ == '__main__':
    main()