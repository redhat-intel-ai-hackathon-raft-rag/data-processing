import chromadb
from llmmodel import embedding_pipeline


client = chromadb.Client()
collection = client.create_collection(
    name="embeddings",  # Equivalent to your table name
    metadata={"description": "Collection for embeddings with id, text, and embedding_model"}
)


def injest_data(embeddings_data):
    '''
    embeddings_data = [
        {
            "id": "123",  # Non-null ID
            "text": "Example sentence for embedding.",  # Non-null text
            "embedding_model": "OpenAI GPT-4",  # Non-null embedding model
            "embedding": [0.1, 0.2, 0.3, ...]  # Embedding vector, will serve as unique pk
        }
    ]
    '''
    collection.add(
        embeddings=[data["embedding"] for data in embeddings_data],
        metadatas=[{
            "id": data["id"],
            "text": data["text"],
            "embedding_model": data["embedding_model"]
        } for data in embeddings_data]
    )


if __name__ == "__main__":
    from sqlalchemy.orm import sessionmaker
    from inference.db.sqldb import Webpage, BookDocument, engine  # Assuming sqldb.py is the file where Webpage is defined

    Session = sessionmaker(bind=engine)
    session = Session()
    results = session.query(Webpage.id, Webpage.text).all()
    embeddings_data = []
    for i, result in enumerate(results):
        embeddings_data.append({
            "id": result.id,
            "text": result.text,
            "embedding_model": "Vertex AI text-embedding-004 Task: RETRIEVAL_DOCUMENT",
            "embedding": embedding_pipeline(result.text)[0].values
        })
        if i % 1000 == 0:
            print(f"Processing {i}th record")
    results = session.query(BookDocument.id, BookDocument.text).all()
    embeddings_data = []
    for i, result in enumerate(results):
        embeddings_data.append({
            "id": result.id,
            "text": result.text,
            "embedding_model": "Vertex AI text-embedding-004 Task: RETRIEVAL_DOCUMENT",
            "embedding": embedding_pipeline(result.text)[0].values
        })
        if i % 1000 == 0:
            print(f"Processing {i}th record")
    # Close the session
    session.close()