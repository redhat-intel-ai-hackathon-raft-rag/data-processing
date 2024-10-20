results = community.louvain_modularity(graph)  # Include all nodes and relationships

for record in results:
    node_id = record["nodeId"]
    community_id = record["communityId"]
    print(f"Article ID: {node_id}, Community ID: {community_id}")