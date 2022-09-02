# "https://api.spotify.com/v1/recommendations?limit=10&seed_artists=3UY1KK0iXeC0mpaK0ltFza&seed_genres=japanese%20pop%20rap%2Cjapanese%20r%26b%2Cjapanese%20teen%20pop&seed_tracks=6nYezkgAePhAmnxNTQRsLV"

import json
import requests
import pandas as pd

USER_ID = "12145090977"
LIMIT = "10"
SEED_ARTIST = "3UY1KK0iXeC0mpaK0ltFza"
SEED_GENRES = "japanese%20pop%20rap%2Cjapanese%20r%26b%2Cjapanese%20teen%20pop"
SEED_TRACKS = "6nYezkgAePhAmnxNTQRsLV"
MARKET = "ES"
PLAYLIST_ID = '69wxxNjForXxfYWJdAHSuD'
CREATE_PLAYLIST_URL = 'https://api.spotify.com/v1/users/' + USER_ID + '/playlists'
ADD_TO_PLAYLIST_URL = 'https://api.spotify.com/v1/playlists/' + PLAYLIST_ID + '/tracks'
GET_RECOMMENDATION_URL = 'https://api.spotify.com/v1/recommendations?limit='+ LIMIT + '&market=' + MARKET + '&seed_artists=' + SEED_ARTIST + '&seed_genres=' + SEED_GENRES + '&seed_tracks=' + SEED_TRACKS
print(CREATE_PLAYLIST_URL)
print(GET_RECOMMENDATION_URL)
print(ADD_TO_PLAYLIST_URL)
ACCESS_TOKEN = 'BQDyAlNnL40qHxP5gfVOTZGdA-SlxHnlwAxVP8nYOf_lFSRH4SCAmdLc-yrAtriotrnuIb1VnMTxkrJUdU-LiTFDQA8gcMTAs6i1m00hJKAWLi7v53SYuH5Ay8IesDIWwwN-nVpUf7LKj7ESzuT4S96B2fJXVQu1Xq8nWS7klAmBu274Ez9-cHxWE1sgVrHRVL-uUm7CM05awDA4c0M3_zbhyMFzQTeDDIYWBdYNEJX0yQ'

def get_recommendation ():

    recommendation = requests.get(
        GET_RECOMMENDATION_URL, 
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        }        
    )
    json_resp1 = recommendation.json()
    # print(type(json_resp))
    with open("sample.json", "w") as jsonfile:
        json.dump(json_resp1, jsonfile)
    
    return json_resp1

def add_to_playlist (songs):
    response = requests.post(
        ADD_TO_PLAYLIST_URL+'?uris=' + songs,
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        }       
        
    )
    json_resp = response.json()
    return json_resp
    
# https://api.spotify.com/v1/playlists/3cEYpjA9oz9GiPac4AsH4n/tracks?uris=spotify%3Atrack%3A4iV5W9uYEdYUVa79Axb7Rh%2Cspotify%3Atrack%3A1301WleyT98MSxVHPZCA6M
def main():
    sample1 = []
    strsample = ''
    Recommendations = get_recommendation()
    # print(Recommendations)
    # print(f"Recommended songs: {Recommendations}")
    for items in Recommendations["tracks"]:
        sample1.append(items["uri"])
    print(sample1)
    for items in sample1:
        strsample = strsample + ',' + items
    print(strsample[1:])
    strsample = strsample[1:]
    strsample = strsample.replace(":", "%3A")
    strsample = strsample.replace(",", "%2C")
    print(strsample)
    playlist = add_to_playlist(
        songs = strsample
    )
    print(f"Playlist: {playlist}")


if __name__ == '__main__':
    main()