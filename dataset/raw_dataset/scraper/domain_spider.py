import json
import scrapy
from scrapy.crawler import CrawlerProcess

## TODO scrapy-splash to render JS content
class DomainSpider(scrapy.Spider):
    name = "domain_spider"
    start_urls = ["https://www.healthline.com/", "https://www.cdc.gov/", "https://www.who.int/", "https://www.npr.org/", "https://www.ama-assn.org/"]
    visited_urls = set()  # To track visited URLs

    def parse(self, response):
        # Extract text content
        page_text = response.xpath('//body//text()').getall()
        page_text = ' '.join(page_text).strip()
        yield {'url': response.url, 'text': page_text}
        with open("dataset/raw_dataset/scraper/extracted_text.json", "a") as f:
            f.write(json.dumps({'url': response.url, 'text': page_text}) + ",")
        # Extract and follow links
        hrefs = response.css('a::attr(href)').getall()
        for href in hrefs:
            full_url = response.urljoin(href)
            if full_url not in self.visited_urls and full_url.startswith("https://www.healthline.com"):
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
