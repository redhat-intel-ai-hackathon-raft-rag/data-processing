from datetime import datetime
import os
import json
from sqlalchemy.exc import IntegrityError
from sqldb import Webpage, WebpageLink, Book, BookCite, BookDocument, create_engine, sessionmaker

# Define session for SQLAlchemy
engine = create_engine('postgresql://user:password@localhost/dbname')
Session = sessionmaker(bind=engine)
session = Session()

# Load Webpages Data
webpages_dir = 'dataset/raw_dataset/scraper/'


def current_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


for file in os.listdir(webpages_dir):
    if file.startswith("extracted") and file.endswith(".json"):
        with open(os.path.join(webpages_dir, file), 'r') as f:
            data = json.load(f)
            for item in data:
                # Extract webpage data
                url = item.get('url')
                text = item.get('text')
                links = item.get('links', [])
                domain = item.get('domain')
                title = item.get('title')

                # Create webpage row
                webpage = Webpage(
                    url=url,
                    text=text,
                    links=links,
                    domain=domain,
                    title=title,
                    created_at=current_timestamp()
                )

                try:
                    session.add(webpage)
                    session.flush()  # Get the ID of the inserted webpage

                    # Add links to webpages_links table
                    for link in links:
                        webpage_link = WebpageLink(
                            link=link,
                            webpage_id=webpage.id,
                            created_at=current_timestamp()
                        )
                        session.add(webpage_link)

                    session.commit()
                except IntegrityError:
                    session.rollback()
                    print(f"Failed to insert webpage: {url}")

# Load Books Data
books_dir = 'dataset/raw_dataset/pdf2jsondata/'

for file in os.listdir(books_dir):
    if file.startswith("extracted") and file.endswith(".json"):
        with open(os.path.join(books_dir, file), 'r') as f:
            data = json.load(f)

            # Extract book and its documents
            book_info = data.get("book")
            book_id = book_info.get("id")
            title = book_info.get("title")
            cites = book_info.get("cites", [])

            # Create book row
            book = Book(
                id=book_id,
                title=title,
                created_at=current_timestamp()
            )
            
            try:
                session.add(book)
                session.flush()  # Get the ID of the inserted book

                # Create book citations
                for cited_book_id in cites:
                    book_cite = BookCite(
                        cite_id=cited_book_id,
                        book_id=book.id,
                        created_at=current_timestamp()
                    )
                    session.add(book_cite)

                # Insert documents related to the book
                documents = data.get("documents", [])
                for i, doc in enumerate(documents):
                    doc_text = doc.get("text")
                    doc_id = f"{book_id}_{i+1}"  # Composite ID for each document

                    book_doc = BookDocument(
                        id=doc_id,
                        text=doc_text,
                        book_id=book.id,
                        created_at=current_timestamp()
                    )
                    session.add(book_doc)

                session.commit()
            except IntegrityError:
                session.rollback()
                print(f"Failed to insert book: {book_id}")
