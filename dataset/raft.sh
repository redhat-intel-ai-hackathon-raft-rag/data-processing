output_folder="dataset/generated_dataset"

# Find all files in raw_dataset with specified extensions
find dataset/raw_dataset -type f \( -name "*.json" -o -name "*.csv" -o -name "*.txt" -o -name "*.pdf" \) | while read -r file; do
    # Check for json files
    if [[ ${file: -5} == ".json" ]]; then
        python -m dataset.raft.raft --doc_type json --text_field_name text --file_path "$file" --output_folder "$output_folder"
    fi

    # Check for pdf files
    if [[ ${file: -4} == ".pdf" ]]; then
        python -m dataset.raft.raft --doc_type pdf --file_path "$file" --output_folder "$output_folder"
    fi

    # Check for text files
    if [[ ${file: -4} == ".txt" ]]; then
        python -m dataset.raft.raft --doc_type text --file_path "$file" --output_folder "$output_folder"
    fi

    # Check for csv files
    if [[ ${file: -4} == ".csv" ]]; then
        python -m dataset.raft.raft --doc_type csv --file_path "$file" --output_folder "$output_folder"
    fi
done
