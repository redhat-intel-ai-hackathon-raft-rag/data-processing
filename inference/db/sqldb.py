from sqlalchemy import create_engine, Column, Integer, String, Text, \
    ForeignKey, BigInteger, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Create the base class
Base = declarative_base()


# Webpages Table
class Webpage(Base):
    __tablename__ = 'webpages'
    id = Column(Text, primary_key=True)
    # Non-null text content
    text = Column(Text, nullable=False)
    # Non-null domain
    domain = Column(Text, nullable=False)
    # Nullable title
    title = Column(Text)
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger)
    deleted_at = Column(BigInteger)

    # Relationship to the WebpageLinks class
    links_relation = relationship(
        "WebpageLink",
        back_populates="webpage"
    )


# Webpages Links Table
class WebpageLink(Base):
    __tablename__ = 'webpages_links'
    id = Column(Integer, primary_key=True)
    # Non-null link (URL)
    link = Column(Text, nullable=False)
    # Foreign key to the Webpage table
    webpage_id = Column(
        Text,
        ForeignKey('webpages.id', ondelete='CASCADE'),
        nullable=False
    )
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger)
    deleted_at = Column(BigInteger)

    # Relationship to the Webpage class
    webpage = relationship(
        "Webpage",
        back_populates="links_relation"
    )


# Books Table
class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    # Nullable book title
    title = Column(Text)
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger)
    deleted_at = Column(BigInteger)

    # Relationship to books cites and books documents
    cites_relation = relationship(
        "BookCite",
        foreign_keys='[BookCite.book_id]',
        back_populates="book"
    )
    cited_by_relation = relationship(
        "BookCite",
        foreign_keys='[BookCite.cite_id]',
        back_populates="cited_book"
    )
    documents_relation = relationship(
        "BookDocument",
        back_populates="book"
    )


# Books Cites Table
class BookCite(Base):
    __tablename__ = 'books_cites'

    id = Column(Integer, primary_key=True)  # Primary key
    # Foreign key to cited book
    cite_id = Column(
        Integer,
        ForeignKey('books.id', ondelete='CASCADE'),
        nullable=False
    )
    # Foreign key to citing book
    book_id = Column(
        Integer,
        ForeignKey('books.id', ondelete='CASCADE'),
        nullable=False
    )
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger)
    deleted_at = Column(BigInteger)

    # Relationship to the Book class (self-referencing)
    book = relationship(
        "Book",
        foreign_keys=[book_id],
        back_populates="cites_relation"
    )
    cited_book = relationship(
        "Book",
        foreign_keys=[cite_id],
        back_populates="cited_by_relation"
    )


# Books Documents Table
class BookDocument(Base):
    __tablename__ = 'books_documents'

    id = Column(String, primary_key=True)
    # Non-null document text
    text = Column(Text, nullable=False)
    # Foreign key to the Book table
    book_id = Column(
        Integer,
        ForeignKey('books.id', ondelete='CASCADE'),
        nullable=False
    )
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger)
    deleted_at = Column(BigInteger)

    # Relationship to the Book class
    book = relationship(
        "Book",
        back_populates="documents_relation"
    )


# Create an engine and bind the metadata
engine = create_engine('postgresql://postgres:postgres@localhost:5432/rag')

# Create all tables
Base.metadata.create_all(engine)
