import os
import io
import PyPDF2
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.file']


def pdf_to_text(pdf_file):
    with open(pdf_file, 'rb') as file:
        text = ""
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()
        return text

if __name__ == '__main__':
    pdfs_dir = 'dataset/raw_dataset/thesis'
    pdfs_list = os.listdir(pdfs_dir)
    os.makedirs('dataset/raw_dataset/pdf_texts', exist_ok=True)
    for pdf in pdfs_list:
        try:
            text_content = pdf_to_text(os.path.join(pdfs_dir, pdf))
            with open(f'dataset/raw_dataset/pdf_texts/{pdf}.txt', 'w', encoding='utf-8') as f:
                f.write(text_content)
        except Exception as e:
            print(f"Error in {pdf}: {e}")
            continue
