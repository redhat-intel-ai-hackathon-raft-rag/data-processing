## TODO underconstruction

## this is example code for loading data from external sources

from llama_index.core import download_loader
from llama_index.readers.google import GoogleDocsReader


loader = GoogleDocsReader()
documents = loader.load_data(document_ids=[...])