from neo4j.gds.algorithms import similarity

results = similarity.simrank(graph)  # Include all nodes and relationships

for record in results:
    node_id1 = record["nodeId1"]
    node_id2 = record["nodeId2"]
    simrank = record["simrank"]
    print(f"Paper ID 1: {node_id1}, Paper ID 2: {node_id2}, SimRank: {simrank}")