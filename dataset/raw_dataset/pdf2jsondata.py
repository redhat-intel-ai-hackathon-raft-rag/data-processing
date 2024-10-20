import os
import re
import PyPDF2
import json
from llmmodel import text_splitter, bge_model
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

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
        json.dump(data, json_file, ensure_ascii=False, indent=4)

threshold = 0.3
def split_chunks_by_meaningful_sentences(text):
    chunks = []
    current_chunk = []
    text = re.sub(r"(\w+)\.\s+", r"\1. ", text)
    text = re.sub(r"\b(e\.g\.|i\.e\.)\b", r"\1", text)
    sentences = nltk.sent_tokenize(text)
    print(len(sentences))
    # preprocessed_sentences = [preprocess_sentence(sentence) for sentence in sentences]
    # for i, sentence in enumerate(preprocessed_sentences):
    for i, sentence in enumerate(sentences):
        print(sentence)
        if i == 0:
            current_chunk.append(sentence)
        else:
            try:
                current = " ".join(current_chunk)
                preprocessed_current = preprocess_sentence(current)
                preprocessed_sentence = preprocess_sentence(sentence)
                similarity = bge_model.compute_score([preprocessed_current, preprocessed_sentence])
                if similarity['colbert+sparse+dense'] > threshold:
                    current_chunk.append(sentence)
                else:
                    print(similarity)
                    chunks.append(current_chunk)
                    current_chunk = [sentence]
            except Exception as e:
                print(e)      
                current_chunk.append(sentence)
        chunks.append(current_chunk)
    final_chunks = []
    for chunk in chunks:
        if len(chunk) == 1 and len(chunk[0]) < 100:
            continue
        if len(chunk) == 1 and len(chunk[0]) > 100:
            final_chunks.append(chunk[0])
            continue
        docs = text_splitter.split_text(" ".join(chunk))
        for doc in docs:
            if len(doc.page_content) > 2000:
                final_chunks.extend(text_splitter.split_text(doc.page_content))
            else:
                final_chunks.append(doc.page_content)
    return final_chunks


lemmatizer = WordNetLemmatizer()
def preprocess_sentence(sentence):
    stop_words = set(stopwords.words('english'))
    words = [word.lower() for word in sentence.split()]
    words = [word for word in words if word not in stop_words]
    words = [lemmatizer.lemmatize(word) for word in words]
    return ' '.join(words)


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
