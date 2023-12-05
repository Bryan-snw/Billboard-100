from bs4 import BeautifulSoup
import requests
import pyperclip
import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth
# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials

billboard_url = "https://www.billboard.com/charts/hot-100"
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']

# Spotify Auth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri="https://example.com",
                                               scope="playlist-modify-private"))

user = sp.current_user()
user_id = user['id']

input_date = input("Which year do you want to travel to? (Type the date in YYYY-MM-DD format)\n")
print("Hang in there! this will take a while (￣o￣) . z Z\n")

# Scrapping Billboard Webpages
res = requests.get(url=f"{billboard_url}/{input_date}")
res.raise_for_status()
billboard_web_page = res.text

soup = BeautifulSoup(billboard_web_page, 'html.parser')
songs = soup.select('.o-chart-results-list__item  h3')

songs_list = [song.getText().strip() for song in songs]

year = input_date.split('-')[0]
songs_url = []

# Save song uri
for song in songs_list:
    result = sp.search(q=f"track:{song} year:{year}", type='track')
    try:
        uri = result['tracks']["items"][0]['uri']
        songs_url.append(uri)
    except IndexError:
        print(f"Sadly {song} doesnt exist in Spotify, it'll be skipped.")


# Create Playlist
playlist = sp.user_playlist_create(
    user=user_id,
    name=f"{input_date} Billboard 100",
    public=False
)

# add song to playlist
sp.playlist_add_items(playlist_id=playlist['id'], items=songs_url)
playlist_url = playlist['external_urls']['spotify']
# Copy to clipboard
pyperclip.copy(playlist_url)

print("\nヾ(≧▽≦*)o  Thank you for your patience q(≧▽≦q)")
print("Playlist Created!(☞ﾟヮﾟ)☞")
print(f"Here's the link to the playlist: {playlist_url}")
print("In fact, we already copied the link to your clipboard, Go listen to the banger!")
