from neo4j.gds.algorithms import community

# Assuming you have nodes representing users and relationships with properties reflecting user characteristics
results = community.community_expansion(graph, seed_ids=[123, 456])  # Specify seed user IDs

for record in results:
    node_id = record["nodeId"]
    community_id = record["communityId"]
    print(f"User ID: {node_id}, Community ID: {communityId}")