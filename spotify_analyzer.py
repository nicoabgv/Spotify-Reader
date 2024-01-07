import os 
import json
from heapq import nlargest
from datetime import datetime
from collections import Counter, defaultdict
import openpyxl
import matplotlib.pyplot as plt

def open_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None
    
def show_total_songs_listened(json_data):
    total_songs = len(json_data)
    
    print(f"Total number of songs listened: {total_songs}")

def show_total_time_listened(json_data):
    total_time_ms = sum(info_reproduccion["ms_played"] for info_reproduccion in json_data)
    total_time_sec = total_time_ms / 1000
    total_time_min, total_time_sec = divmod(total_time_sec, 60)
    total_time_hr, total_time_min = divmod(total_time_min, 60)
    total_time_days, total_time_hr = divmod(total_time_hr, 24)
    
    print(f"Total time spent listened: {int(total_time_days)} days, {int(total_time_hr)} hours, {int(total_time_min)} minutes, {int(total_time_sec)} seconds")

def show_top_played_songs(json_data):
    played_songs = defaultdict(int)
    for playback_info in json_data:
        song = playback_info["master_metadata_track_name"]
        played_songs[song] += 1
    top_played_songs = nlargest(5, played_songs.items(), key=lambda x: x[1])
    print("Top 5 most played songs:")
    for idx, (song, plays) in enumerate(top_played_songs, start=1):
        print(f"{idx}. Song: {song}, Plays: {plays}")

def show_top_artists(json_data):
    played_artists = defaultdict(int)
    for playback_info in json_data:
        artist = playback_info["master_metadata_album_artist_name"]
        played_artists[artist] += 1
    top_played_artists = nlargest(5, played_artists.items(), key=lambda x: x[1])
    print("Top 5 most played artists:")
    for idx, (artist, plays) in enumerate(top_played_artists, start=1):
        print(f"{idx}. Artist: {artist}, Plays: {plays}")

def show_avg_duration(json_data):
    total_durations = sum(info["ms_played"] for info in json_data)
    avg_duration_ms = total_durations / len(json_data)
    avg_duration_minutes = avg_duration_ms / 60000
    print(f"Average song duration: {avg_duration_minutes:.2f} minutes")

def show_most_used_devices(json_data):
    used_devices = Counter(info["platform"] for info in json_data)
    print("Analysis of most used devices:")
    for device, count in used_devices.most_common():
        print(f"{device}: {count} plays")

def compare_periods(json_data):
    period_to_analyze = input("Enter the period to analyze (e.g., '2023-01' for January 2023): ")
    period_to_analyze = datetime.strptime(period_to_analyze, '%Y-%m')

    period_plays = defaultdict(int)
    for info in json_data:
        ts = datetime.strptime(info["ts"], '%Y-%m-%dT%H:%M:%SZ')
        period_plays[ts.strftime('%Y-%m')] += 1

    plays_in_period = period_plays[period_to_analyze.strftime('%Y-%m')]

    print(f"Plays in period {period_to_analyze.strftime('%B %Y')}: {plays_in_period}")
    print("Comparison with other periods:")

    for period, plays in period_plays.items():
        if period != period_to_analyze.strftime('%Y-%m'):
            difference = plays - plays_in_period
            print(f"{period}: {difference:+} plays")

def show_graphs(json_data):
    graph_options = {
        "1": ("show_top_played_songs_graph", "Show Top Played Songs"),
        "2": ("show_top_artists_graph", "Show Top Artists"),
        "3": ("show_playback_time_distribution_graph", "Show Playback Time Distribution"),
        "4": ("show_playback_trends_graph", "Show Playback Trends"),
    }

    print("\nGraph options:")
    for key, (_, label) in graph_options.items():
        print(f"{key}. {label}")

    option = input("Choose a graph to display: ")
    if option in graph_options:
        graph_function_name, _ = graph_options[option]
        graph_function = globals()[graph_function_name]
        graph_function(json_data)
    else:
        print("Invalid option. Please choose a valid option.")

def show_top_played_songs_graph(json_data):
    played_songs = Counter(
        info["master_metadata_track_name"]
        if info["master_metadata_track_name"] is not None
        else "None"
        for info in json_data
    )
    
    top_played_songs = nlargest(5, played_songs.items(), key=lambda x: x[1])
    
    song_names = []
    plays_list = []
    
    for song, plays in top_played_songs:
        song_names.append(song)
        plays_list.append(plays)
    
    plt.figure(figsize=(10, 6))
    plt.barh(song_names, plays_list, color='lightblue')
    plt.xlabel('Plays')
    plt.ylabel('Songs')
    plt.title('Top Played Songs')
    plt.tight_layout()
    plt.show()

def show_top_artists_graph(json_data):

    played_artists = Counter(info["master_metadata_album_artist_name"] for info in json_data)
    top_played_artists = nlargest(5, played_artists.items(), key=lambda x: x[1])
    
    artist_names = [artist for artist, _ in top_played_artists]
    plays = [plays for _, plays in top_played_artists]

    plt.figure(figsize=(10, 6))
    plt.barh(artist_names, plays, color='lightcoral')
    plt.xlabel('Plays')
    plt.ylabel('Artists')
    plt.title('Top Played Artists')
    plt.tight_layout()
    plt.show()

def show_playback_time_distribution_graph(json_data):
   
    playback_times = [info["ms_played"] / 1000 for info in json_data]

    plt.figure(figsize=(10, 6))
    plt.hist(playback_times, bins=20, color='green', alpha=0.7)
    plt.xlabel('Playback Time (seconds)')
    plt.ylabel('Number of Songs')
    plt.title('Distribution of Playback Times for Songs')
    plt.tight_layout()
    plt.show()

def show_playback_trends_graph(json_data):
    
    plays_per_date = defaultdict(int)
    for info in json_data:
        ts = datetime.strptime(info["ts"], '%Y-%m-%dT%H:%M:%SZ')
        date = ts.date()
        plays_per_date[date] += 1

    dates = list(plays_per_date.keys())
    plays = [plays_per_date[date] for date in dates]

    plt.figure(figsize=(10, 6))
    plt.plot(dates, plays, marker='o')
    plt.xlabel('Date')
    plt.ylabel('Number of Plays')
    plt.title('Playback Trends Over Time')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def analyze_playback_reasons(json_data):
    start_reasons = Counter(info["reason_start"] for info in json_data)
    end_reasons = Counter(info["reason_end"] for info in json_data)

    print("Playback start reasons:")
    for reason, count in start_reasons.items():
        print(f"{reason}: {count} times")

    print("\nPlayback end reasons:")
    for reason, count in end_reasons.items():
        print(f"{reason}: {count} times")

def export_to_excel(json_data, source_file):
    excel_workbook = openpyxl.Workbook()
    sheet = excel_workbook.active
    sheet.title = "Spotify Statistics"

    current_row = 1
    sheet.cell(row=current_row, column=1, value="Date")
    sheet.cell(row=current_row, column=2, value="Hour")
    sheet.cell(row=current_row, column=3, value="Song")
    sheet.cell(row=current_row, column=4, value="Artist")
    sheet.cell(row=current_row, column=5, value="Minutes played")
    sheet.cell(row=current_row, column=6, value="Platform")
    sheet.cell(row=current_row, column=7, value="IP address")
    sheet.cell(row=current_row, column=8, value="Reason start")
    sheet.cell(row=current_row, column=9, value="Reason end")

    for info in json_data:
        current_row += 1
        ts = datetime.strptime(info["ts"], '%Y-%m-%dT%H:%M:%SZ')
        date = ts.strftime('%Y-%m-%d')
        hour = ts.strftime('%H:%M:%S')
        song = info["master_metadata_track_name"]
        artist = info["master_metadata_album_artist_name"]
        duration = info["ms_played"] / 1000 / 60 
        formatted_duration = '{:.2f}'.format(duration)  
        platform = info["platform"]
        ip_address = info["ip_addr_decrypted"]
        reason_start = info["reason_start"]
        reason_end = info["reason_end"]

        sheet.cell(row=current_row, column=1, value=date)
        sheet.cell(row=current_row, column=2, value=hour)
        sheet.cell(row=current_row, column=3, value=song)
        sheet.cell(row=current_row, column=4, value=artist)
        sheet.cell(row=current_row, column=5, value=formatted_duration)
        sheet.cell(row=current_row, column=6, value=platform)
        sheet.cell(row=current_row, column=7, value=ip_address)
        sheet.cell(row=current_row, column=8, value=reason_start)
        sheet.cell(row=current_row, column=9, value=reason_end)
    
    excel_file = source_file + ".xlsx" 
    excel_workbook.save(excel_file)
    print(f"Stats exported to '{excel_file}'.")

file_path = input("Enter the JSON file path: ")
source_file = os.path.basename(file_path).split('.')[0]

json_data = open_json_file(file_path)

if json_data:
    export_to_excel(json_data, source_file)
else:
    print("Could not open the JSON file.")

if json_data:
    while True:
        print("\nOptions:")
        print("1. Show total of songs listened")
        print("2. Total time spent listened")
        print("3. Show the top 5 most played songs")
        print("4. Show the top 5 most played artists")
        print("5. Show the average song duration")
        print("6. Show analysis of most used devices")
        print("7. Compare statistics between different periods")
        print("8. Show statistical graphs")
        print("9. Export statistics to Excel")
        print("10. Analyze playback reasons")
        print("11. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            show_total_songs_listened(json_data)
        elif choice == "2":
            show_total_time_listened(json_data)
        elif choice == "3":
            show_top_played_songs(json_data)
        elif choice == "4":
            show_top_artists(json_data)
        elif choice == "5":
            show_avg_duration(json_data)
        elif choice == "6":
            show_most_used_devices(json_data)
        elif choice == "7":
            compare_periods(json_data)
        elif choice == "8":
            show_graphs(json_data)
        elif choice == "9":
            export_to_excel(json_data, source_file)
        elif choice == "10":
            analyze_playback_reasons(json_data)
        elif choice == "11":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose a valid option.")
