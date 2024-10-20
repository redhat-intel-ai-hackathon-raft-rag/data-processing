import os
import re
import PyPDF2
import json
from dataset.raw_dataset.clean_document import clean_document
from llmmodel import text_splitter, percentile_chunker, gradient_chunker

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            text = ""
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                text += page.extract_text()
            del page
            del reader
            data = []
            chunks = split_chunks_by_meaningful_sentences(text)
            for chunk in chunks:
                data.append({"text": chunk})
            return data
    except Exception as e:
        print(e)
        return None


def write_to_json(data, output_path):
    with open(output_path, 'w') as json_file:
        json_file.seek(0)
        json_file.truncate()
        json.dump(data, json_file, ensure_ascii=False, indent=4)


def split_chunks_by_meaningful_sentences(text):
    text = clean_document(text)
    final_chunks = []
    chunks = [doc for doc in text_splitter.split_text(text)]
    final_chunks.extend(chunks)
    # print(len(chunks))
    for chunk in chunks:
        if len(chunk) < 100:
            continue
        if len(chunk) > 10000:
            docs = text_splitter.split_text(chunk)
            final_chunks.extend(docs)
    return final_chunks


def refine_json_data(json_path):
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
        for i in range(len(data)):
            try:
                data[i]["text"] = clean_document(data[i]["text"])
                text = data[i]["text"]
                if len(text) < 100:
                    data.pop(i)
                    continue
                if len(text) > 10000:
                    docs = percentile_chunker.split_text(text)
                    print(len(docs))
                    data.pop(i)
                    for doc in docs:
                        if len(doc) > 10000:
                            parts = gradient_chunker.split_text(text)
                            for part in parts:
                                data.append({"text": part})
                        else:
                            data.append({"text": doc})
            except IndexError:
                continue
    write_to_json(data, json_path)


if __name__ == "__main__":
    for root, dirs, files in os.walk("dataset/raw_dataset/pdf/"):
        for file in files:
            if file.endswith(".pdf"):
                print(os.path.join(root, file))
                pdf_path = os.path.join(root, file)  # Path to the PDF file
                output_path = pdf_path.replace(".pdf", ".json")
                output_path = output_path.replace("/pdf/", "/pdf2jsondata/extracted_text_")
                # if the output file does not exist, extract the text from the PDF and write it to a JSON file
                if not os.path.exists(output_path):
                    extracted_data = extract_text_from_pdf(pdf_path)
                    if extracted_data is not None:
                        write_to_json(extracted_data, output_path)
    for root, dirs, files in os.walk("dataset/raw_dataset/pdf2jsondata/"):
        for file in files:
            if file.endswith(".json"):
                print(os.path.join(root, file))
                json_path = os.path.join(root, file)  # Path to the JSON file
                refine_json_data(json_path)
