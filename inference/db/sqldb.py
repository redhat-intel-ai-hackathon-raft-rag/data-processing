from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, BigInteger, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Create the base class
Base = declarative_base()

# Webpages Table
class Webpage(Base):
    __tablename__ = 'webpages'
    id = Column(Text, primary_key=True)  # Primary key (URL)
    text = Column(Text, nullable=False)  # Non-null text content
    links = Column(ARRAY(Text), nullable=False)  # Non-null list of links (array of URLs)
    domain = Column(Text, nullable=False)  # Non-null domain
    title = Column(Text)  # Nullable title
    created_at = Column(BigInteger, nullable=False)  # Non-null creation timestamp
    updated_at = Column(BigInteger)  # Nullable updated timestamp
    deleted_at = Column(BigInteger)  # Nullable deleted timestamp

    # Relationship to the WebpageLinks class
    links_relation = relationship("WebpageLink", back_populates="webpage")

# Webpages Links Table
class WebpageLink(Base):
    __tablename__ = 'webpages_links'

    id = Column(Integer, primary_key=True)  # Primary key
    link = Column(Text, nullable=False)  # Non-null link (URL)
    webpage_id = Column(Integer, ForeignKey('webpages.id', ondelete='CASCADE'), nullable=False)  # Foreign key to the Webpage table
    created_at = Column(BigInteger, nullable=False)  # Non-null creation timestamp
    updated_at = Column(BigInteger)  # Nullable updated timestamp
    deleted_at = Column(BigInteger)  # Nullable deleted timestamp

    # Relationship to the Webpage class
    webpage = relationship("Webpage", back_populates="links_relation")

# Books Table
class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)  # Primary key
    title = Column(Text)  # Nullable book title
    created_at = Column(BigInteger, nullable=False)  # Non-null creation timestamp
    updated_at = Column(BigInteger)  # Nullable updated timestamp
    deleted_at = Column(BigInteger)  # Nullable deleted timestamp

    # Relationship to books cites and books documents
    cites_relation = relationship("BookCite", foreign_keys='[BookCite.book_id]', back_populates="book")
    cited_by_relation = relationship("BookCite", foreign_keys='[BookCite.cite_id]', back_populates="cited_book")
    documents_relation = relationship("BookDocument", back_populates="book")

# Books Cites Table
class BookCite(Base):
    __tablename__ = 'books_cites'

    id = Column(Integer, primary_key=True)  # Primary key
    cite_id = Column(Integer, ForeignKey('books.id', ondelete='CASCADE'), nullable=False)  # Foreign key to cited book
    book_id = Column(Integer, ForeignKey('books.id', ondelete='CASCADE'), nullable=False)  # Foreign key to citing book
    created_at = Column(BigInteger, nullable=False)  # Non-null creation timestamp
    updated_at = Column(BigInteger)  # Nullable updated timestamp
    deleted_at = Column(BigInteger)  # Nullable deleted timestamp

    # Relationship to the Book class (self-referencing)
    book = relationship("Book", foreign_keys=[book_id], back_populates="cites_relation")
    cited_book = relationship("Book", foreign_keys=[cite_id], back_populates="cited_by_relation")

# Books Documents Table
class BookDocument(Base):
    __tablename__ = 'books_documents'

    id = Column(String, primary_key=True)  # Primary key (composite ID)
    text = Column(Text, nullable=False)  # Non-null document text
    book_id = Column(Integer, ForeignKey('books.id', ondelete='CASCADE'), nullable=False)  # Foreign key to the Book table
    created_at = Column(BigInteger, nullable=False)  # Non-null creation timestamp
    updated_at = Column(BigInteger)  # Nullable updated timestamp
    deleted_at = Column(BigInteger)  # Nullable deleted timestamp

    # Relationship to the Book class
    book = relationship("Book", back_populates="documents_relation")

# Create an engine and bind the metadata
engine = create_engine('postgresql://username:password@localhost/dbname')

# Create all tables
Base.metadata.create_all(engine)
