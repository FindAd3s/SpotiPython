import requests


USER_ID = "12145090977"
CREATE_PLAYLIST_URL = 'https://api.spotify.com/v1/users/' + USER_ID + '/playlists'
print(CREATE_PLAYLIST_URL)
ACCESS_TOKEN = 'BQBURM4cQPaaduGUYorCDE7V-DTkl5-xkF18ODskEF0KmzBTFYECaLauVT7x2RigLT2EzqWOwbgDfQCx5OxWHwjjbbVX8xfZqp8_Cd9l3Tnjgw1LSmUCZbmPULhgAURKU127_nUGwfXD_w3ixX8a_PTbBQi5XcJ8JVKMvmFpVjlT6GD7crd-0mdUs5c8_YlfktGHDCXShjYV_9F0uz3QMdZYMRkvG7TGOkfa318CUyD0LQ'

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
    return json_resp

def main():
    playlist = create_playlist(
        name = "My Private Test Playlist",
        public = False
    )
    print(f"Playlist: {playlist}")

if __name__ == '__main__':
    main()