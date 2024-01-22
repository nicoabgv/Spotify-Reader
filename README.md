# Spotify Analyzer

**Spotify Analyzer** is a Python program designed to analyze your complete Spotify listening history stored in JSON files, providing detailed statistics and visualizations based on your listening data.

## Getting Started

1. **Download Your Complete Spotify Data:**
   - Visit [Spotify Privacy Settings](https://www.spotify.com/account/privacy/).
   - In the "Download your data" section, request your data.
   - Choose the option "Request all my data" to ensure you receive your complete listening history.
   - Once received, extract the content and locate the JSON files.

2. **Run the Program:**
   - Execute the program by running the provided Python script.
   - Load your Spotify listening history JSON file through the program's user interface.

## Why Merge Spotify JSON Files?

Spotify provides your complete listening history in separate files. Merging them with **merge_json.py** before analysis ensures a more accurate understanding by considering your entire listening history at once. Although you can analyze files separately, merging them allows for a more comprehensive examination.

### Running merge_json.py

To merge Spotify JSON files, use the provided Python script:

```bash
python merge_json.py /path/to/your/json/files /path/to/unified/output.json
```
Replace "/path/to/your/json/files" with the folder containing your Spotify JSON files and "/path/to/unified/output.json" with the desired path for the unified output file.

## Features
- Display the total number of songs listened to
- Total time dedicated to listening
- Show the first and last played songs
- Display the top 5 most listened-to songs
- Display the top 5 most listened-to artists
- Show the most skipped songs
- Display the average duration of songs
- Show daily listening patterns
- Show annual statistics
- Display daily playback time statistics
- Analyze most used devices
- Display statistical charts
- Export statistics to Excel
- Analyze playback reasons

## Usage
1. **Open JSON File:**
   - Click the "Open JSON File" button to select your Spotify listening history JSON file.

2. **Choose Analysis Option:**
   - Select an option from the dropdown menu to analyze your Spotify listening history based on different criteria.

3. **View Results:**
   - Results will be displayed in the text area, and graphical analyses can be visualized.

4. **Export to Excel:**
   - Export your Spotify statistics to an Excel file for deeper analysis.

## Graphical Analysis
The program provides graphical representations for:
- Most Listened-to Songs
- Most Listened-to Artists
- Distribution of Playback Time
- Playback Trends Over Time

## Dependencies
- Python 3.x
- tkinter (for the graphical interface)
- matplotlib
- openpyxl

**Note:** Ensure you have the necessary dependencies installed before running the program.

**Important Note: Requesting Complete Listening History**
To ensure accurate and complete results, it is crucial to request your complete Spotify listening history:
- When requesting your data on the Spotify privacy page, choose the "Extended playback history" option.
- This will include your entire listening history from the creation of your account.

## Export to Excel
The program allows you to export your Spotify statistics to an Excel file for more detailed analysis. Simply choose the "Export statistics to Excel" option from the dropdown menu and follow the on-screen instructions.

## License
This project is under the MIT License.