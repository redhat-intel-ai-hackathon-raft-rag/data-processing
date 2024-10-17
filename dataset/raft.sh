output_folder="dataset/generated_dataset"
raft_checkpoint_file="dataset/generated_dataset/raft_checkpoint.txt"
find dataset/generated_dataset -type f -name "*_raft_extracted_text_*.json" | while read -r file; do
    echo "extracted_text_${file##*_raft_extracted_text_}" >> "$raft_checkpoint_file"
done
# remove duplicates
sort -u -o "$raft_checkpoint_file" "$raft_checkpoint_file"
# Find all files in raw_dataset with specified extensions
find dataset/raw_dataset -type f \( -name "*.json" -o -name "*.csv" -o -name "*.txt" -o -name "*.pdf" \) | while read -r file; do
    if [ -f "$raft_checkpoint_file" ]; then
        if grep -q "$file" "$raft_checkpoint_file"; then
            continue
        fi
    fi
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

    # Append the file to the raft_checkpoint_file
    echo "$file" >> "$raft_checkpoint_file"
done
