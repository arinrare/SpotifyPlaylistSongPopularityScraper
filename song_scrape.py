import config

def generate_merged_artist_stats_csv(songs, filename="merged_artist_stats.csv", weight_playlist=None, weight_spotify=None, top_n=100):
    # Use weights from config if not provided
    if weight_playlist is None:
        weight_playlist = config.WEIGHT_PLAYLIST / 100.0
    if weight_spotify is None:
        weight_spotify = config.WEIGHT_SPOTIFY / 100.0
    artist_counter = Counter()
    artist_popularity = defaultdict(list)
    for song in songs:
        for artist in song['Artist'].split(', '):
            artist_counter[artist] += 1
            if song['Popularity'] != 'N/A':
                artist_popularity[artist].append(int(song['Popularity']))

    # Normalize playlist counts and popularity
    max_count = max(artist_counter.values()) if artist_counter else 1
    max_popularity = max([max(pops) if pops else 0 for pops in artist_popularity.values()]) if artist_popularity else 1

    merged_stats = []
    for artist in artist_counter:
        count = artist_counter[artist]
        avg_popularity = round(sum(artist_popularity[artist]) / len(artist_popularity[artist]), 2) if artist_popularity[artist] else 0
        norm_count = count / max_count if max_count else 0
        norm_popularity = avg_popularity / max_popularity if max_popularity else 0
        weighted_score = weight_playlist * norm_count + weight_spotify * norm_popularity
        merged_stats.append({
            'Artist': artist,
            'Song Count': count,
            'Average Popularity': avg_popularity,
            'Weighted Score': round(weighted_score, 4),
        })

    # Sort by weighted score descending
    merged_stats.sort(key=lambda x: x['Weighted Score'], reverse=True)

    # Write top N to CSV
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Artist', 'Song Count', 'Average Popularity', 'Weighted Score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in merged_stats[:top_n]:
            writer.writerow(row)
    print(f"CSV file '{filename}' generated with merged artist stats.")
def generate_artist_stats_by_popularity_csv(songs, filename="song_stat_spotify_popularity.csv"):
    artist_counter = Counter()
    artist_popularity = defaultdict(list)
    for song in songs:
        for artist in song['Artist'].split(', '):
            artist_counter[artist] += 1
            if song['Popularity'] != 'N/A':
                artist_popularity[artist].append(int(song['Popularity']))

    artist_stats = []
    for artist in artist_counter:
        count = artist_counter[artist]
        avg_popularity = round(sum(artist_popularity[artist]) / len(artist_popularity[artist]), 2) if artist_popularity[artist] else 'N/A'
        artist_stats.append({
            'Artist': artist,
            'Song Count': count,
            'Average Popularity': avg_popularity,
        })

    # Sort by average popularity (descending), then by song count (descending)
    artist_stats.sort(key=lambda x: (x['Average Popularity'] if x['Average Popularity'] != 'N/A' else -1), reverse=True)

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Artist', 'Song Count', 'Average Popularity']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in artist_stats:
            writer.writerow(row)
    print(f"CSV file '{filename}' generated with artist stats sorted by popularity.")
import csv
from collections import Counter, defaultdict
def generate_artist_stats_csv(songs, filename="song_stats_playlist_popularity.csv"):
    # Count songs per artist
    artist_counter = Counter()
    artist_popularity = defaultdict(list)
    for song in songs:
        for artist in song['Artist'].split(', '):
            artist_counter[artist] += 1
            if song['Popularity'] != 'N/A':
                artist_popularity[artist].append(int(song['Popularity']))

    # Prepare stats
    artist_stats = []
    for artist, count in artist_counter.most_common():
        avg_popularity = round(sum(artist_popularity[artist]) / len(artist_popularity[artist]), 2) if artist_popularity[artist] else 'N/A'
        artist_stats.append({
            'Artist': artist,
            'Song Count': count,
            'Average Popularity': avg_popularity,
        })

    # Write to CSV
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Artist', 'Song Count', 'Average Popularity']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in artist_stats:
            writer.writerow(row)
    print(f"CSV file '{filename}' generated with artist stats.")
# --- Spotify Playlist Scraper ---
# Requirements: spotipy
# 1. Run the script and enter a public playlist URL when prompted.

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re

# --- Spotify API credentials ---
CLIENT_ID = config.CLIENT_ID
CLIENT_SECRET = config.CLIENT_SECRET

# --- Helper to extract playlist ID from URL ---
def extract_playlist_id(url):
    match = re.search(r"playlist/([a-zA-Z0-9]+)", url)
    return match.group(1) if match else None

# --- Main scraping function ---
def scrape_spotify_playlist(playlist_url):
    playlist_id = extract_playlist_id(playlist_url)
    if not playlist_id:
        print("Invalid Spotify playlist URL.")
        return

    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))
    results = sp.playlist_tracks(playlist_id)
    songs = []
    while results:
        for item in results['items']:
            track = item['track']
            song = {
                'Title': track['name'],
                'Artist': ', '.join([artist['name'] for artist in track['artists']]),
                'Album': track['album']['name'],
                'Release Date': track['album']['release_date'],
                'Track URL': track['external_urls']['spotify'],
                'Duration (ms)': track['duration_ms'],
                'Popularity': track.get('popularity', 'N/A'),
            }
            songs.append(song)
        if results['next']:
            results = sp.next(results)
        else:
            results = None
    return songs

if __name__ == "__main__":
    print("--- Spotify Playlist Scraper ---")
    playlist_url = config.PUBLIC_PLAYLIST_URL
    songs = scrape_spotify_playlist(playlist_url)
    if songs:
        print(f"Playlist Name: {playlist_url}")
        print(f"\nFound {len(songs)} songs:")
        #for i, song in enumerate(songs, 1):
            #print(f"{i}. {song['Title']} - {song['Artist']} | Album: {song['Album']} | Released: {song['Release Date']} | Popularity: {song['Popularity']}")
            #print(f"   URL: {song['Track URL']}")
        # Generate artist stats CSV
        generate_artist_stats_csv(songs)
        # Generate artist stats sorted by popularity CSV
        generate_artist_stats_by_popularity_csv(songs)
        # Generate merged artist stats CSV (adjust weights as desired)
        generate_merged_artist_stats_csv(songs)
    else:
        print("No songs found or error occurred.")