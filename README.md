# Time Travel Spotify Playlist Generator 🎵🕰️

This Python project lets you **travel back in time** by generating a Spotify playlist of the top UK songs from a specific date!

It scrapes the Official Charts for the top 100 tracks, then searches and adds them to a private Spotify playlist.

---

## 🚀 Features
- Input a date in the format `YYYYMMDD`
- Scrape the **Official UK Singles Chart**
- Search for matching songs on **Spotify**
- Create a **private playlist** with those songs

---

## 🛠 Requirements

- Python 3.7+
- Spotify Developer Account
- A `.env` file with your credentials:
  ```env
  client_id=your_spotify_client_id
  client_secret=your_spotify_client_secret
