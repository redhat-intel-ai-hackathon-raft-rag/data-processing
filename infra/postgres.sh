docker run -d \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=postgres \
    -e POSTGRES_DB=rag \
    -p 5432:5432 \
    --name postgres \
    postgres