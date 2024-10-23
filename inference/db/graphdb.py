from neo4j import GraphDatabase

# Neo4j Database Connection
class Neo4jClient:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_webpage(self, id, url, text, links, domain, title=None):
        query = """
        CREATE (w:Webpage {id: $id, url: $url, text: $text, links: $links, domain: $domain, title: $title})
        """
        with self.driver.session() as session:
            session.run(query, id=id, url=url, text=text, links=links, domain=domain, title=title)

    def create_book(self, id, title=None, cites=None):
        """
        Create a Book node. If 'cites' is provided (list of book ids), create CITES relationships.
        """
        query = """
        CREATE (b:Book {id: $id, title: $title})
        """
        with self.driver.session() as session:
            session.run(query, id=id, title=title)

        # Create CITES relationships if cites are provided
        if cites:
            with self.driver.session() as session:
                for cited_id in cites:
                    self.create_citation(id, cited_id)

    def create_book_document(self, id, text, book_id):
        query = """
        MATCH (b:Book {id: $book_id})
        CREATE (d:Document {id: $id, text: $text})-[:BELONGS_TO]->(b)
        """
        with self.driver.session() as session:
            session.run(query, id=id, text=text, book_id=book_id)

    def create_citation(self, book_id, cites_id):
        """
        Create a CITES relationship from one book to another.
        """
        query = """
        MATCH (b1:Book {id: $book_id}), (b2:Book {id: $cites_id})
        CREATE (b1)-[:CITES]->(b2)
        """
        with self.driver.session() as session:
            session.run(query, book_id=book_id, cites_id=cites_id)


# Example usage
if __name__ == "__main__":
    # query web page with sql alchemy
    from inference.db.sqldb import Webpage, WebpageLink, Book, BookCite, \
        BookDocument, engine
    from sqlalchemy.orm import sessionmaker
    
    # Define session for SQLAlchemy
    Session = sessionmaker(bind=engine)
    session = Session()
    
    webpages = session.query(Webpage).all()
    for webpage in webpages:
        # print(webpage.id, webpage.text, webpage.domain, webpage.title)
        links = session.query(WebpageLink).filter(WebpageLink.webpage_id == webpage.id).all()
        for link in links:
            print(link)
    # # Connect to Neo4j
    # neo4j_client = Neo4jClient(uri="bolt://localhost:7687", user="neo4j", password="password")

    # # Creating Webpage nodes
    # neo4j_client.create_webpage(
    #     id=1,
    #     url="https://example.com",
    #     text="Example webpage content",
    #     links=["https://link1.com", "https://link2.com"],
    #     domain="example.com",
    #     title="Example Webpage"
    # )

    # # Creating Book nodes
    # neo4j_client.create_book(id=1, title="First Book")
    # neo4j_client.create_book(id=2, title="Second Book")

    # # Creating Document nodes belonging to a book
    # neo4j_client.create_book_document(id="1_1", text="First document text", book_id=1)
    # neo4j_client.create_book_document(id="1_2", text="Second document text", book_id=1)

    # # Creating Citation relationships
    # neo4j_client.create_citation(book_id=1, cites_id=2)

    # # Close connection
    # neo4j_client.close()
