from neo4j import GraphDatabase


class GraphDatabaseService:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def expand_community(self, node_id):
        """
        Expand community around a specific node
        using Louvain or similar algorithms.
        """
        query = """
        CALL gds.louvain.stream({
            nodeProjection: 'Node',
            relationshipProjection: 'REL_TYPE',
            maxIterations: 10
        })
        YIELD nodeId, communityId
        WHERE gds.util.asNode(nodeId).id = $node_id
        RETURN nodeId, communityId
        """
        with self.driver.session() as session:
            result = session.run(query, node_id=node_id)
            return result.single()

    def retrieve_influential_nodes(self, topic):
        """Retrieve high PageRank or centrality nodes for a given topic."""
        query = """
        MATCH (n:Node)
        WHERE n.topic = $topic
        RETURN n, n.pagerank AS rank
        ORDER BY rank DESC LIMIT 10
        """
        with self.driver.session() as session:
            result = session.run(query, topic=topic)
            return [record['n'] for record in result]

    def store_properties(self, node_id, properties):
        """Store calculated properties like influence score in a Neo4j node."""
        query = """
        MATCH (n:Node {id: $node_id})
        SET n += $properties
        RETURN n
        """
        with self.driver.session() as session:
            session.run(query, node_id=node_id, properties=properties)

    def retrieve_properties(self, node_id):
        """Retrieve properties of a node."""
        query = """
        MATCH (n:Node {id: $node_id})
        RETURN n
        """
        with self.driver.session() as session:
            result = session.run(query, node_id=node_id)
            return result.single()['n']
        
    def retrieve_community(self, community_id):
        """Retrieve nodes in a community."""
        query = """
        MATCH (n:Node)
        WHERE n.community = $community_id
        RETURN n
        """
        with self.driver.session() as session:
            result = session.run(query, community_id=community_id)
            return [record['n'] for record in result]
        
    def store_community_properties(self, community_id, properties):
        """Store calculated properties like community score in a Neo4j node."""
        query = """
        MATCH (n:Node {community: $community_id})
        SET n += $properties
        RETURN n
        """
        with self.driver.session() as session:
            session.run(query, community_id=community_id, properties=properties)

    def retrieve_community_properties(self, community_id):
        """Retrieve properties of a community."""
        query = """
        MATCH (n:Node {community: $community_id})
        RETURN n
        """
        with self.driver.session() as session:
            result = session.run(query, community_id=community_id)
            return result.single()['n']
        
    def retrieve_similar_nodes(self, node_id):
        """Retrieve similar nodes based on embeddings."""
        query = """
        MATCH (n:Node {id: $node_id})
        CALL gds.nodeSimilarity.stream('my-graph', {
            topK: 5,
            nodeProjection: 'Node',
            embeddingField: 'embedding'
        })
        YIELD node1, node2, similarity
        RETURN gds.util.asNode(node2) AS node, similarity
        """
        with self.driver.session() as session:
            result = session.run(query, node_id=node_id)
            return [record['node'] for record in result]
        
    def store_node_embedding(self, node_id, embedding):
        """Store embedding for a node."""
        query = """
        MATCH (n:Node {id: $node_id})
        SET n.embedding = $embedding
        RETURN n
        """
        with self.driver.session() as session:
            session.run(query, node_id=node_id, embedding=embedding)
    
    def retrieve_node_embedding(self, node_id):
        """Retrieve embedding for a node."""
        query = """
        MATCH (n:Node {id: $node_id})
        RETURN n.embedding AS embedding
        """
        with self.driver.session() as session:
            result = session.run(query, node_id=node_id)
            return result.single()['embedding']
    
    def store_relationship(self, node1_id, node2_id, relationship_type):
        """Store a relationship between two nodes."""
        query = """
        MATCH (n1:Node {id: $node1_id})
        MATCH (n2:Node {id: $node2_id})
        MERGE (n1)-[:REL_TYPE]->(n2)
        """
        with self.driver.session() as session:
            session.run(query, node1_id=node1_id, node2_id=node2_id)
    
    def retrieve_relationships(self, node_id):
        """Retrieve relationships for a node."""
        query = """
        MATCH (n:Node {id: $node_id})-[r]->(m)
        RETURN r, m
        """
        with self.driver.session() as session:
            result = session.run(query, node_id=node_id)
            return [(record['r'], record['m']) for record in result]
    
    def store_community_relationship(self, community_id1, community_id2, relationship_type):
        """Store a relationship between two communities."""
        query = """
        MATCH (n1:Node {community: $community_id1})
        MATCH (n2:Node {community: $community_id2})
        MERGE (n1)-[:REL_TYPE]->(n2)
        """
        with self.driver.session() as session:
            session.run(query, community_id1=community_id1, community_id2=community_id2)
    
    def retrieve_community_relationships(self, community_id):
        """Retrieve relationships for a community."""
        query = """
        MATCH (n:Node {community: $community_id})-[r]->(m)
        RETURN r, m
        """
        with self.driver.session() as session:
            result = session.run(query, community_id=community_id)
            return [(record['r'], record['m']) for record in result]
    
if __name__ == '__main__':
    service = GraphDatabaseService("bolt://localhost:7687", "neo4j", "password")
    print(service.expand_community(1))
    print(service.retrieve_influential_nodes("Machine Learning"))
    service.store_properties(1, {"influence_score": 0.8})
    print(service.retrieve_properties(1))
    print(service.retrieve_community(1))
    service.store_community_properties(1, {"community_score": 0.9})
    print(service.retrieve_community_properties(1))
    print(service.retrieve_similar_nodes(1))
    service.store_node_embedding(1, [0.1, 0.2, 0.3])
    print(service.retrieve_node_embedding(1))
    service.store_relationship(1, 2, "SIMILAR")
    print(service.retrieve_relationships(1))
    service.store_community_relationship(1, 2, "SIMILAR")
    print(service.retrieve_community_relationships(1))
    service.close()