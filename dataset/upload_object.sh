# read .env file
export $(egrep -v '^#' .env | xargs)
LOCAL_FOLDER=dataset

# create tar ball of the dataset folder only including the necessary *.json, *.csv, *.txt, *.pdf files
# and upload it to the bucket
cp -r dataset dataset_temp
find dataset_temp -type f -not -name "*.json" -not -name "*.csv" -not -name "*.txt" -not -name "*.pdf" -not -name "*.epub" -delete
find dataset_temp -type f -name requirements.txt -delete
find dataset_temp -type d -empty -delete
tar -czf dataset.tar.gz dataset_temp
curl -X PUT --data-binary "@dataset.tar.gz" -H "Content-Type: application/octet-stream" $PRESIGNED_URL_FOR_BUCKET_FOR_UPLOAD"dataset.tar.gz"
rm -rf dataset_temp dataset.tar.gz