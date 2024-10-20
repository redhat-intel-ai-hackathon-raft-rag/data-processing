results = community.walktrap(graph)  # Include all nodes and relationships

for record in results:
    node_id = record["nodeId"]
    community_id = record["communityId"]
    print(f"User ID: {node_id}, Community ID: {community_id}")