from datetime import datetime
import os
import json
from urllib.parse import urlparse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from inference.db.sqldb import Webpage, WebpageLink, Book, BookCite, \
                  BookDocument, engine

# Define session for SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()

# Load Webpages Data
webpages_dir = 'dataset/raw_dataset/scraper/'


def current_timestamp():
    # utc unix timestamp
    return datetime.now().timestamp()


for file in os.listdir(webpages_dir):
    if file.startswith("extracted") and file.endswith(".json"):
        with open(os.path.join(webpages_dir, file), 'r+') as f:
            print(f"Processing file: {os.path.join(webpages_dir, file)}")
            data = json.load(f)
            new_data = []
            for item in data:
                # Extract webpage data
                url = item.get('url')
                text = item.get('text')
                links = item.get('links', [])
                parsed_url = urlparse(url)
                domain_parts = parsed_url.netloc.split('.')
                if len(domain_parts) >= 2:
                    domain = '.'.join(domain_parts[-2:])
                else:
                    domain = parsed_url.netloc
                try:
                    title = item.get('title')
                except Exception:
                    title = None

                # Create webpage row
                webpage = Webpage(
                    id=url,
                    text=text,
                    domain=domain,
                    title=title,
                    created_at=current_timestamp()
                )

                try:
                    session.add(webpage)
                    session.flush()  # Get the ID of the inserted webpage

                    # Add links to webpages_links table
                    if links is None:
                        for link in links:
                            webpage_link = WebpageLink(
                                link=link,
                                webpage_id=webpage.id,
                                created_at=current_timestamp()
                            )
                            session.add(webpage_link)

                    session.commit()
                    new_data.append(item)
                except IntegrityError as e:
                    session.rollback()
                    if "duplicate key value violates unique constraint" in str(e) and \
                            "webpages_pkey" in str(e):
                        print(f"Webpage already exists: {url}")
                    else:
                        new_data.append(item)
                    print(e)
                    print(f"Failed to insert webpage: {os.path.join(webpages_dir, file)}")
            f.seek(0)
            f.truncate()
            json.dump(new_data, f, indent=4)

# # Load Books Data
# books_dir = 'dataset/raw_dataset/pdf2jsondata/'

# for file in os.listdir(books_dir):
#     if file.startswith("extracted") and file.endswith(".json"):
#         with open(os.path.join(books_dir, file), 'r') as f:
#             data = json.load(f)

#             # Extract book and its documents
#             book_info = data.get("book")
#             book_id = book_info.get("id")
#             title = book_info.get("title")
#             cites = book_info.get("cites", [])

#             # Create book row
#             book = Book(
#                 id=book_id,
#                 title=title,
#                 created_at=current_timestamp()
#             )
#             try:
#                 session.add(book)
#                 session.flush()  # Get the ID of the inserted book

#                 # Create book citations
#                 for cited_book_id in cites:
#                     book_cite = BookCite(
#                         cite_id=cited_book_id,
#                         book_id=book.id,
#                         created_at=current_timestamp()
#                     )
#                     session.add(book_cite)

#                 # Insert documents related to the book
#                 documents = data.get("documents", [])
#                 for i, doc in enumerate(documents):
#                     doc_text = doc.get("text")
#                     # Composite ID for each document
#                     doc_id = f"{book_id}_{i+1}"

#                     book_doc = BookDocument(
#                         id=doc_id,
#                         text=doc_text,
#                         book_id=book.id,
#                         created_at=current_timestamp()
#                     )
#                     session.add(book_doc)

#                 session.commit()
#             except IntegrityError:
#                 session.rollback()
#                 print(f"Failed to insert book: {book_id}")
