import scrapy
import json
import html2text
from bs4 import BeautifulSoup
import os
import time
import threading
import re


class DomainSpider(scrapy.Spider):
    name = "domain_spider"
    start_urls = [
        "https://www.healthline.com/",
        "https://www.cdc.gov/",
        "https://www.who.int/",
        "https://www.npr.org/",
        "https://www.ama-assn.org/"
    ]
    visited_urls_file = "dataset/raw_dataset/scraper/visited_urls.txt"
    data_file = "dataset/raw_dataset/scraper/extracted_text.json"
    interval = 60  # 1 minute

    def __init__(self, *args, **kwargs):
        super(DomainSpider, self).__init__(*args, **kwargs)
        self.visited_urls = self.load_visited_urls()
        self.start_time = time.time()
        self.file_lock = threading.Lock()
        self.current_file = self.get_new_file()

    def load_visited_urls(self):
        if os.path.exists(self.visited_urls_file):
            with open(self.visited_urls_file, "r") as f:
                return set(f.read().splitlines())
        return set()

    def get_new_file(self):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        new_file = f"dataset/raw_dataset/scraper/extracted_text_{timestamp}.json"
        with open(new_file, "w") as f:
            f.write("[\n")
        return new_file

    def parse(self, response):
        document_transformer = html2text.HTML2Text()
        document_transformer.ignore_links = True
        document_transformer.ignore_images = True
        continue_crawl = True
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            main_content = soup.body
        except Exception:
            continue_crawl = False
        links = response.css('a::attr(href)').getall()
        link_list = [response.urljoin(link) for link in links]
        if continue_crawl:
            for tag in main_content.find_all(['header', 'footer']):
                tag.decompose()
            document = document_transformer.handle(str(main_content))
            document = self.clean_document(document)
            data_entry = {
                "url": response.url,
                "text": document,
                "links": link_list
            }
            self.write_to_file(data_entry)

        # Append the current URL to the visited set and file
        self.visited_urls.add(response.url)
        self.save_visited_url(response.url)

        # Check if it's time to create a new file
        if time.time() - self.start_time >= self.interval:
            self.close()
            self.current_file = self.get_new_file()
            self.start_time = time.time()

        # Extract and follow links
        for full_url in link_list:
            if full_url not in self.visited_urls and self.is_valid_url(full_url):
                yield scrapy.Request(full_url, callback=self.parse)

    def clean_document(self, document):
        # Clean the document text
        document = re.sub(r'^[^\n]*\b[^\s]*\.(?:png|jpg|svg)\b[^\n]{0,50}\n?', '', document, flags=re.MULTILINE)
        document = re.sub(r'\b(?:https?://[^\s]{1,100})\b\s*$', '', document, flags=re.MULTILINE)
        document = re.sub(r'\s*\*\s*[^{1,10}]+\s*\n?', '', document)
        document = re.sub(r'\(\s*(https?://[^\s)]+)\s*\n?\)', '', document)
        document = re.sub(r'\n\s*\n', '\n', document).strip()
        return document

    def write_to_file(self, data_entry):
        with self.file_lock, open(self.current_file, "a") as f:
            f.write(json.dumps(data_entry) + ",\n")

    def save_visited_url(self, url):
        with open(self.visited_urls_file, "a") as f:
            f.write(url + "\n")

    def is_valid_url(self, url):
        return any(url.startswith(prefix) for prefix in self.start_urls)

    def close(self):
        with open(self.current_file, "r+") as f:
            f.seek(0, os.SEEK_END)
            if f.tell() > 0:
                f.seek(f.tell() - 2, os.SEEK_SET)
                last_char = f.read(1)
                if last_char == ",":
                    f.seek(f.tell() - 1, os.SEEK_SET)
                    f.truncate()
            f.write("]")

if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess()
    process.crawl(DomainSpider)
    process.start()
