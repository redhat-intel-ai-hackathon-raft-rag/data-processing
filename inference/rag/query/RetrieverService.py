class RetrieverService:
    def __init__(self, graph_db_service, embedding_db_service):
        self.graph_db_service = graph_db_service
        self.embedding_db_service = embedding_db_service
    
    def retrieve_documents_by_query(self, query, topic=None):
        """
        Retrieve relevant documents by calculating query similarity and community information.
        1. Retrieve similar documents from the embedding service.
        2. If a topic is provided, retrieve influential nodes for the topic from the graph database.
        """
        # Step 1: Retrieve similar documents based on the query
        documents, metadatas = self.embedding_db_service.query_similar_documents(query)
        
        # Step 2: Optionally retrieve influential nodes based on the topic
        influential_nodes = []
        if topic:
            influential_nodes = self.graph_db_service.retrieve_influential_nodes(topic)
        
        # Step 3: Return documents and influential nodes
        return {
            'documents': documents,
            'metadata': metadatas,
            'influential_nodes': influential_nodes
        }

    def store_document(self, document, metadata):
        """
        Add document to both the embedding service (for similarity retrieval)
        and optionally to the graph database (for graph-based algorithms).
        """
        # Store in embedding database
        self.embedding_db_service.add_document(document, metadata)
        
        # Optionally, add the document metadata to the graph database as a node
        if 'node_id' in metadata:
            self.graph_db_service.store_properties(metadata['node_id'], metadata)
