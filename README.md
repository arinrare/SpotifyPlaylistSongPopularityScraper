# Spotify Playlist Song Popularity Scraper

This project scrapes song and artist statistics from Spotify playlists and merges the data for analysis.

## Features
- Scrapes song statistics from Spotify playlists
- Collects artist statistics
- Merges and exports data to CSV files
- Designed for data analysis and research

## Files
- `song_scrape.py`: Main script for scraping song and artist data from Spotify playlists.
- `config.py`: Configuration file for API keys and settings.
- `merged_artist_stats.csv`: Output file with merged artist statistics.
- `song_stat_spotify_popularity.csv`: Output file with song statistics and Spotify popularity.
- `song_stats_playlist_popularity.csv`: Output file with song statistics and playlist popularity.

## Requirements
- Python 3.7+
- Spotipy (or other Spotify API library)
- pandas

## Setup
1. Clone the repository:
   ```sh
   git clone git@github.com:arinrare/SpotifyPlaylistSongPopularityScraper.git
   cd SpotifyPlaylistSongPopularityScraper
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # or
   source .venv/bin/activate  # On macOS/Linux
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the project root directory with your Spotify Developer credentials:
   ```env
   CLIENT_ID_ID=your_spotify_client_id
   CLIENT_SECRET=your_spotify_client_secret
   ```
   You can obtain these values by creating an application at the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).

5. (Optional) If your project uses `config.py` for additional settings, configure them as needed.

## Usage
Run the main script to start scraping:
```sh
python song_scrape.py
```

Output CSV files will be generated in the project directory.

## License
MIT License

## Author
arinrare
