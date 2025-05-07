import requests
import base64

CLIENT_ID = 'bd42287be7a6470b8a9ac3cf102f6df8'
CLIENT_SECRET = '78dc4c00f17b4e4497f380c4e2ae1784'

def get_spotify_token():
    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_auth = base64.b64encode(auth_string.encode()).decode()

    headers = {
        "Authorization": f"Basic {b64_auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    response.raise_for_status()
    return response.json()["access_token"]
def get_album_cover(titulo, autor):
    token = get_spotify_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }

    query = f"{titulo} {autor}"
    params = {
        "q": query,
        "type": "track",
        "limit": 1
    }

    response = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)
    response.raise_for_status()
    results = response.json()

    try:
        track = results["tracks"]["items"][0]
        image_url = track["album"]["images"][0]["url"]
        return image_url
    except (IndexError, KeyError):
        return None
