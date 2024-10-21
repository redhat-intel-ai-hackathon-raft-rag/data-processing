import chromadb


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
    from inference.db.sqldb import Raft, engine  # Assuming sqldb.py is the file where Raft is defined

    Session = sessionmaker(bind=engine)
    session = Session()
    results = session.query(Raft.id, Raft.text).all()
    embeddings_data = []
    for i, result in enumerate(results):
        embeddings_data.append({
            "id": result.id,
            "text": result.text,
            "embedding_model": "OpenAI GPT-4",
            "embedding": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        })
        if i % 1000 == 0:
            print(f"Processing {i}th record")

    # Close the session
    session.close()