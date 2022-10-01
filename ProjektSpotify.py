from bs4 import BeautifulSoup
import requests as re
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

"""
    this program allows you to create your own Spotify playlist using 
    the Spotify API and the OAuth 2.0 protocol
"""

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
response = re.get(f"https://www.billboard.com/charts/hot-100/{date}")
soup = BeautifulSoup(response.text, "html.parser")
title_songs_tag = soup.find_all(name="h3", id="title-of-a-story", class_="a-no-trucate")
title_songs = [song.getText().strip("\n\t") for song in title_songs_tag]

artiste_song_tag = soup.find_all(name="span", class_=["a-no-trucate"])
artistes = [artiste.getText().strip("\n\t") for artiste in artiste_song_tag]
# print(artistes)

# =============================== Spotipy =============================
id_client = "515d33e111794329921879a6834d1a86"
secret = "371d5fa9e1654d4da5d93ea6e3f312ca"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="playlist-modify-private",
    redirect_uri="http://example.com",
    client_id=id_client,
    client_secret=secret,
    show_dialog=True,
    cache_path="token.txt"
))
id_user = sp.current_user()["id"]
user_name = sp.current_user()["display_name"]

songs_url = []
images = []
for song, artiste in zip(title_songs, artistes):
    items = sp.search(q=f"track: {song}  artist: {artiste} ", type="track")["tracks"]["items"]
    try:
        songs_url.append(items[0]["uri"])
        images.append(items[0]["album"]["images"][0]["url"])  # for image
    except IndexError:
        print(f"{song} doesn't exist in spotify. skipped.")

# print(json.dumps(images, sort_keys=False, indent=3))
playlist_id = sp.user_playlist_create(user=id_user, name=f" {date} Billboard 100", public=False)["id"]

# print playlist
sp.playlist_add_items(playlist_id=playlist_id, items=songs_url)
print("done !")