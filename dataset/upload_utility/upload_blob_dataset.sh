export $(egrep -v '^#' .env | xargs)
LOCAL_FOLDER=dataset/raw_dataset/pdf
find $LOCAL_FOLDER -type f -name "*.pdf" | while read -r file; do
    echo "Uploading $file"
    UPDATE_PATH="${PRESIGNED_URL_FOR_BUCKET_FOR_UPLOAD}${PREFIX_FOLDER}/$(basename "$file")"
    echo "UPDATE_PATH: $UPDATE_PATH"
    curl -X PUT --data-binary "@$file" -H "Content-Type: application/octet-stream" "$UPDATE_PATH"
done