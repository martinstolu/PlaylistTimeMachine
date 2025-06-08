import requests
import spotipy
from Demos.win32ts_logoff_disconnected import username
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
import datetime
import os



while True:
    user_input = input("What year would you like to travel to? (YYYYMMDD): ")
    try:
        travel_date = datetime.datetime.strptime(user_input, "%Y%m%d")
        today = datetime.datetime.today()
        if travel_date > today:
            print("That date is in the future. Please enter a past date.")
        else:
            break
    except ValueError:
        print("Invalid format. Please enter the date in YYYYMMDD format (e.g., 20250607).")

year = travel_date.year

# Optional: Use the parsed date
print(f"Traveling to {travel_date.strftime('%B %d, %Y')}...")


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

url= f"https://www.officialcharts.com/charts/singles-chart/{user_input}/7501/"
response = requests.get(url, headers)
web_output = response.text
soup = BeautifulSoup(web_output, "html.parser")
spans = soup.select('div.description.block p a ')

songs_and_artists = []
only_songs = []
# Iterate in steps of 2, since song and artist alternate in your list
for i in range(0, len(spans), 2):
    song_spans = spans[i].select('span')
    artist_spans = spans[i+1].select('span')

    # Get the last non-icon span (the actual song title)
    song_title = song_spans[-1].get_text(strip=True) if song_spans else ""
    artist_name = artist_spans[0].get_text(strip=True) if artist_spans else ""

    songs_and_artists.append((song_title, artist_name))
    only_songs.append(song_title)

# print("\nThe top 100 songs are:\n")
#
# for song in only_songs:
#     print(f"{song}")

client_id = os.environ["client_id"]
client_secret = os.environ["client_secret"]
username = os.environ["username"]
redirect_uri = os.environ["redirect_uri"]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope="playlist-modify-private",
                                               show_dialog=True,
                                               username=username
                                               ))

user_id = sp.current_user()["id"]

song_uris = []
for song in only_songs:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
print(song_uris)
playlist = sp.user_playlist_create(user=user_id, name=f"{year} Billboard 100", public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)







