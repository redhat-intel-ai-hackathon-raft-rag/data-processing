from raft.raft import DocType
import json
import PyPDF2


def data_to_chunks(file_path: str,
                   doc_type: DocType,
                   text_field_name: str = None) -> list:
    if doc_type == "pdf":
        return _pdf_to_chunks(file_path)
    if doc_type == "json":
        return _json_to_chunks(file_path, text_field_name)
    if doc_type == "txt":
        return _text_to_chunks(file_path)


def _text_to_chunks(file_path):
    with open(file_path, 'r') as f:
        text = f.read()
    return text


def _pdf_to_chunks(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text


def _json_to_chunks(file_path, text_field_name=None):
    if text_field_name is None:
        raise "text_field_name is required for json data"
    with open(file_path, 'r') as f:
        data = json.load(f)
    text = data[text_field_name]
    return text


if __name__ == "__main__":
    pdf_path = "United_States_PDF.pdf"
    text_path = "United_States_TXT.txt"
    json_path = "United_States_JSON.json"
    chunk_size = 1000
    chunks = data_to_chunks(pdf_path, DocType.PDF)
    print(chunks)
    chunks = data_to_chunks(text_path, DocType.TXT)
    print(chunks)
    chunks = data_to_chunks(json_path, DocType.JSON, "text")
    print(chunks)
