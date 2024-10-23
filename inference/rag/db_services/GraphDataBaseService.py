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
