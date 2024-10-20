from neo4j.gds.algorithms import community


results = centrality.eigenvector(graph)  # Include all nodes and relationships

for record in results:
    node_id = record["nodeId"]
    eigenvector = record["eigenvector"]
    print(f"Website ID: {node_id}, Eigenvector Centrality: {eigenvector}")