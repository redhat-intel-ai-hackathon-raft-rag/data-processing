import os
import json
import tarfile
import re

# Define the directory containing your JSON array files
input_directory = 'dataset/generated_dataset_book'
output_file = 'combined_book.jsonl'
tarball_file = 'combined_book.tar.gz'


def is_english(text):
    # Regular expression to match non-ASCII characters
    return not bool(re.search(r'[^\x00-\x7F]', text))


# Open the output JSONL file
with open(output_file, 'w') as jsonl_file:
    # Read each JSON array file
    for filename in os.listdir(input_directory):
        file_path = os.path.join(input_directory, filename)
        if os.path.isfile(file_path) and filename.endswith('.json'):
            with open(file_path, 'r') as file:
                try:
                    # Load the JSON data 
                    json_data = json.load(file)
                    json_data = [
                        entry for entry in json_data
                        if is_english(entry["instruction"]) and
                        is_english(entry["input"]) and
                        is_english(entry["output"])
                    ]
                    # Check if it's a list
                    if isinstance(json_data, list):
                        for entry in json_data:
                            # Write each JSON object to the JSONL file
                            jsonl_file.write(json.dumps(entry) + '\n')
                    else:
                        print(f"Warning: {filename} does not contain a valid JSON array.")
                except json.JSONDecodeError as e:
                    print(f"Error reading {filename}: {e}")
print(f"Combined data written to {output_file}.")

# Create a tarball of the JSONL file
with tarfile.open(tarball_file, 'w:gz') as tar:
    tar.add(output_file, arcname=os.path.basename(output_file))

print(f"Tarball created: {tarball_file}.")
