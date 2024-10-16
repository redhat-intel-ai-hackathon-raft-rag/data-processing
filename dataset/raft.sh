output_folder="dataset/generated_dataset"
## for all file in raw_dataset with extension .json, .csv, .txt, .pdf
find raw_dataset -type f -name "*.json" -o -name "*.csv" -o -name "*.txt" -o -name "*.pdf" not -name "requirements.txt" | while read file; do
    # for json
    python raft --doc_type json --text_field_name text --file_path $file --output_folder $output_folder
    ## for pdf file
    python raft --doc_type pdf --file_path {str} --output_folder $output_folder
    ## for text file
    python raft --doc_type text --file_path {str} --output_folder $output_folder
done