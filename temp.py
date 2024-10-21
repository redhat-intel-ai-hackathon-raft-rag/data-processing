import re
import time
import PyPDF2
from llmmodel import text_generation_pipeline, text_splitter

if __name__ == "__main__":
    with open("/home/eichiuehara/Downloads/2403.20327v1.pdf", "rb") as f:
        text = ""
        reader = PyPDF2.PdfReader(f)
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()
        chunks = text_splitter.create_documents([text])
        num_chunks = len(chunks)
        for idx, chunk in enumerate(chunks):
            # remove short chunks
            if len(chunk.page_content) < 100:
                continue
            # split the chunk into parts
            messages = [
                {
                    "role": "user",
                    "content": "Summarize the following text: " + chunk.page_content
                }
            ]
            result = text_generation_pipeline(messages)
            try:
                summary = result[0]["generated_text"][1]["content"]
                print(summary)
            except Exception:
                summary = result.choices[0].message.content
                print(summary)
