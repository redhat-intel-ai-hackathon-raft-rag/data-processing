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

cp -r dataset dataset_temp
find dataset_temp -type f \(-not -name "*.pdf" \) -delete
find dataset_temp -type f \(-name requirements.txt\) -delete
find dataset_temp -type d -empty -delete
# for pdf files, we need to tar them separately then upload for each file
PREFIX_FOLDER="dataset_pdf"
find dataset_temp -type f \(-name "*.pdf" \) | while read -r file; do
    echo "Uploading $file"
    UPDATE_PATH=$PRESIGNED_URL_FOR_BUCKET_FOR_UPLOAD"$PREFIX_FOLDER/$(basename $file)"
    echo "UPDATE_PATH: $UPDATE_PATH"
    curl -X PUT --data-binary "@$file" -H "Content-Type: application/octet-stream" $UPDATE_PATH
done
rm -rf dataset_temp dataset_pdf.tar.gz

