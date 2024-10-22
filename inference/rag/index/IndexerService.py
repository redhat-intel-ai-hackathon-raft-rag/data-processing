class IndexerService:
    def __init__(self, graph_db_service, embedding_db_service):
        self.graph_db_service = graph_db_service
        self.embedding_db_service = embedding_db_service

    def index_document(self, document, metadata):
        """
        Index a new document in both the graph and embedding databases.
        - document: the document text
        - metadata: a dictionary containing metadata like `id`, `topic`, and more
        """
        # Step 1: Add the document to the graph database
        node_data = {
            'id': metadata['id'],
            'text': document,
            'topic': metadata.get('topic', 'unknown'),
            'score': metadata.get('score', 0)  # Example score
        }
        self.graph_db_service.add_node(node_data)

        # Step 2: Add the document to the embedding database
        self.embedding_db_service.add_document(document, metadata)

    def update_document(self, document_id, document, metadata):
        """
        Update an existing document's content and metadata in both databases.
        """
        # Step 1: Update the node properties in the graph database
        node_properties = {
            'text': document,
            'topic': metadata.get('topic', 'unknown'),
            'score': metadata.get('score', 0)
        }
        self.graph_db_service.update_node(document_id, node_properties)

        # Step 2: Update the document and its embedding in the embedding database
        self.embedding_db_service.update_document(document_id, document, metadata)

    def delete_document(self, document_id):
        """
        Delete a document from both the graph and embedding databases.
        """
        # Step 1: Delete the node from the graph database
        self.graph_db_service.delete_node(document_id)

        # Step 2: Delete the document from the embedding database
        self.embedding_db_service.delete_document(document_id)

    def create_indexes(self):
        """
        Optional: Create indexes in the graph database for better query performance.
        """
        # Example: Create an index on the "topic" property
        query = "CREATE INDEX ON :Node(topic)"
        with self.graph_db_service.driver.session() as session:
            session.run(query)
