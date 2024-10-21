-- Initialize PostgreSQL tables

-- All tables will have the following common columns:
-- - created_at: non-nullable, UNIX timestamp
-- - updated_at: nullable, UNIX timestamp
-- - deleted_at: nullable, UNIX timestamp

-- Webpages Table
CREATE TABLE webpages (
    id SERIAL PRIMARY KEY,  -- Primary key
    url TEXT NOT NULL,  -- Non-null URL
    text TEXT NOT NULL,  -- Non-null text content
    links TEXT[] NOT NULL,  -- Non-null list of links (array of URLs)
    domain TEXT NOT NULL,  -- Non-null domain
    title TEXT,  -- Nullable title of the webpage
    created_at BIGINT NOT NULL,  -- UNIX timestamp for creation
    updated_at BIGINT,  -- UNIX timestamp for updates (nullable)
    deleted_at BIGINT  -- UNIX timestamp for soft deletion (nullable)
);

-- Webpages Links Table
CREATE TABLE webpages_links (
    id SERIAL PRIMARY KEY,  -- Primary key
    link TEXT NOT NULL,  -- Non-null link (URL)
    webpage_id INTEGER NOT NULL REFERENCES webpages(id) ON DELETE CASCADE,  -- Foreign key to the webpages table
    created_at BIGINT NOT NULL,  -- UNIX timestamp for creation
    updated_at BIGINT,  -- UNIX timestamp for updates (nullable)
    deleted_at BIGINT  -- UNIX timestamp for soft deletion (nullable)
);

-- Books Table
CREATE TABLE books (
    id SERIAL PRIMARY KEY,  -- Primary key
    title TEXT,  -- Nullable book title
    created_at BIGINT NOT NULL,  -- UNIX timestamp for creation
    updated_at BIGINT,  -- UNIX timestamp for updates (nullable)
    deleted_at BIGINT  -- UNIX timestamp for soft deletion (nullable)
);

-- Books Cites Table
CREATE TABLE books_cites (
    id SERIAL PRIMARY KEY,  -- Primary key
    cite_id INTEGER NOT NULL REFERENCES books(id) ON DELETE CASCADE,  -- Foreign key to the books table (the cited book)
    book_id INTEGER NOT NULL REFERENCES books(id) ON DELETE CASCADE,  -- Foreign key to the books table (the citing book)
    created_at BIGINT NOT NULL,  -- UNIX timestamp for creation
    updated_at BIGINT,  -- UNIX timestamp for updates (nullable)
    deleted_at BIGINT  -- UNIX timestamp for soft deletion (nullable)
);

-- Books Documents Table
CREATE TABLE books_documents (
    id TEXT PRIMARY KEY,  -- Primary key (each document has a composite ID)
    text TEXT NOT NULL,  -- Non-null text content of the document
    book_id INTEGER NOT NULL REFERENCES books(id) ON DELETE CASCADE,  -- Foreign key to the books table
    created_at BIGINT NOT NULL,  -- UNIX timestamp for creation
    updated_at BIGINT,  -- UNIX timestamp for updates (nullable)
    deleted_at BIGINT  -- UNIX timestamp for soft deletion (nullable)
);

-- Add any additional indexes if necessary for optimization, such as for frequently queried columns like `created_at` or `webpage_id`.
