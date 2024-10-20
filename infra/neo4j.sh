docker pull neo4j:latest && \
docker run -p 7474:7474 -p 7687:7687 --name neo4j -e NEO4J_AUTH=none neo4j:latest