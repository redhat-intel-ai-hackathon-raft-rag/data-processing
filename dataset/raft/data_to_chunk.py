from raft.raft import DocType
import json
import PyPDF2


def data_to_chunk(file_path: str, doc_type: DocType,
                  chunk_size: int = 512,
                  text_field_name: str = None):
    if doc_type == "pdf":
        return _text_to_chunk(
            _pdf_to_text(file_path), chunk_size)
    if doc_type == "json":
        return _text_to_chunk(
            _json_to_text(file_path, text_field_name), chunk_size)
    if doc_type == "txt":
        return _text_to_chunk(file_path, chunk_size)


def _text_to_chunk(data, chunk_size):
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]


def _pdf_to_text(file_path=None, chunk_size=512):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text


def _json_to_text(file_path=None, text_field_name=None, chunk_size=512):
    if text_field_name is None:
        raise "text_field_name is required for json data"
    with open(file_path, 'r') as f:
        data = json.load(f)
    text = data[text_field_name]
    return text

if __name__ == "__main__":
    pdf_path = "United_States_PDF.pdf"
    text = _pdf_to_text(pdf_path)
    print(text)
    chunk_size = 1000
    chunks = _text_to_chunk(text, chunk_size)
    print(chunks)
