import json
import re
import scrapy
from scrapy.crawler import CrawlerProcess
import html2text
from bs4 import BeautifulSoup


## TODO scrapy-splash to render JS content
class DomainSpider(scrapy.Spider):
    name = "domain_spider"
    start_urls = ["https://www.healthline.com/", "https://www.cdc.gov/", "https://www.who.int/", "https://www.npr.org/", "https://www.ama-assn.org/"]
    visited_urls = set()  # To track visited URLs

    def parse(self, response):
        document_transformer = html2text.HTML2Text()
        document_transformer.ignore_links = True
        document_transformer.ignore_image = True
        soup = BeautifulSoup(response.text, 'html.parser')
        main_content = soup.body
        for tag in main_content.find_all(['header', 'footer']):
            tag.decompose()
        # Extract text from main content
        document = document_transformer.handle(str(main_content))
        # document = re.sub(r'Skip to main content\s*\n', '', document)
        # document = re.sub(r'Skip directly to site content Skip directly to search\n', '', document)
        document = re.sub(r'^[^\n]*\b[^\s]*\.(?:png|jpg|svg)\b[^\n]{0,50}\n?', '', document, flags=re.MULTILINE)
        document = re.sub(r'\b(?:https?://[^\s]{1,100})\b\s*$', '', document, flags=re.MULTILINE)
        document = re.sub(r'\s*\*\s*[^{1,10}]+\s*\n?', '', document)
        document = re.sub(r'\(\s*(https?://[^\s)]+)\s*\n?\)', '', document)
        document = re.sub(r'\n\s*\n', '\n', document).strip()
        yield {'url': response.url, 'text': document}
        with open("dataset/raw_dataset/scraper/extracted_text.json", "a") as f:
            f.write(json.dumps({'url': response.url, 'text': document}) + ",")
        # Extract and follow links
        hrefs = response.css('a::attr(href)').getall()
        for href in hrefs:
            full_url = response.urljoin(href)
            if full_url not in self.visited_urls and full_url.startswith("https://www.healthline.com") or full_url.startswith("https://www.cdc.gov") or full_url.startswith("https://www.who.int") or full_url.startswith("https://www.npr.org") or full_url.startswith("https://www.ama-assn.org"):
                self.visited_urls.add(full_url)
                yield scrapy.Request(full_url, callback=self.parse)
        with open("dataset/raw_dataset/scraper/visited_urls.txt", "w") as f:
            f.write("\n".join(self.visited_urls))


if __name__ == "__main__":
    # Run the spider
    with open("dataset/raw_dataset/scraper/extracted_text.json", "a") as f:
        f.seek(0)
        f.truncate()
        f.write("[")
    process = CrawlerProcess()
    process.crawl(DomainSpider)
    process.start()
    with open("dataset/raw_dataset/scraper/extracted_text.json", "a") as f:
        f.write("]")
