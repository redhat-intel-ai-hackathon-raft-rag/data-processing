# read .env file
export $(egrep -v '^#' .env | xargs)
LOCAL_FOLDER=dataset
rm -rf dataset_temp
# create tar ball of the dataset folder only including the necessary *.json, *.csv, *.txt, *.pdf files
# and upload it to the bucket
# cp -r dataset dataset_temp
# find dataset_temp -type f -not -name "*.json" -not -name "*.csv" -not -name "*.txt"  -not -name "*.epub" -delete
# find dataset_temp -type f -name requirements.txt -delete
# find dataset_temp -type d -empty -delete
# tar -czf dataset.tar.gz dataset_temp
# curl -X PUT --data-binary "@dataset.tar.gz" -H "Content-Type: application/octet-stream" $PRESIGNED_URL_FOR_BUCKET_FOR_UPLOAD"dataset.tar.gz"
# rm -rf dataset_temp dataset.tar.gz

# Copy dataset to a temporary directory
cp -r dataset dataset_temp

# Delete all files except PDF files and requirements.txt
find dataset_temp -type f \( -not -name "*.pdf" -and -not -name "requirements.txt" \) -delete

# Delete empty directories
find dataset_temp -type d -empty -delete

# Define prefix folder for PDFs
PREFIX_FOLDER="dataset_pdf"

# Create a tar file for PDF uploads
tar -czf dataset_pdf.tar.gz -C dataset_temp $(find dataset_temp -type f -name "*.pdf" -exec basename {} \;)

# Upload each PDF file separately
find dataset_temp -type f -name "*.pdf" | while read -r file; do
    echo "Uploading $file"
    UPDATE_PATH="${PRESIGNED_URL_FOR_BUCKET_FOR_UPLOAD}${PREFIX_FOLDER}/$(basename "$file")"
    echo "UPDATE_PATH: $UPDATE_PATH"
    curl -X PUT --data-binary "@$file" -H "Content-Type: application/octet-stream" "$UPDATE_PATH"
done

# Cleanup temporary files
rm -rf dataset_temp dataset_pdf.tar.gz
