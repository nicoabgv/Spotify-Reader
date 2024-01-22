import json
import os
import argparse

def merge_and_sort_json(input_folder, output_file):
    """
    Merge and sort Spotify JSON files from the input_folder into a unified and sorted output_file.

    Parameters:
        input_folder (str): Path to the folder containing JSON files.
        output_file (str): Path to the output JSON file.

    Returns:
        None
    """
    all_data = []

    json_files = [f for f in os.listdir(input_folder) if f.endswith('.json')]

    for file_name in json_files:
        with open(os.path.join(input_folder, file_name), 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
                all_data.extend(data)
            except json.JSONDecodeError:
                print(f"Error decoding JSON in file: {file_name}")

    all_data.sort(key=lambda x: x.get('ts', ''))

    with open(output_file, 'w', encoding='utf-8') as output:
        json.dump(all_data, output, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Merge and sort Spotify JSON files.')
    parser.add_argument('input_folder', type=str, help='Input folder containing JSON files')
    parser.add_argument('output_file', type=str, help='Unified and sorted output file in JSON format')

    args = parser.parse_args()

    try:
        merge_and_sort_json(args.input_folder, args.output_file)
        print(f"Merge and sort successful. Result saved to {args.output_file}")
    except Exception as e:
        print(f"Error: {e}")
