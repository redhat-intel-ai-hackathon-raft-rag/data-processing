import os
from playwright.async_api import async_playwright
import asyncio
import re
from bs4 import BeautifulSoup


def load_start_urls():
    medical_topics = []
    start_urls = []
    with open("dataset/knowledge_graph/refined_medical_topics.txt", "r") as f:
        medical_topics = f.read().splitlines()
    for topic in medical_topics:
        if topic == "":
            continue
        # remove any extra + signs
        topic = re.sub(r"\++", " ", topic)
        topic = re.sub(r"\s+", "+", topic)
        published_years = [str(year) for year in range(2015, 2024)]
        for i in range(len(published_years)):
            query_string = f"&termtype_1=year&termval_1={published_years[i]}"
            start_urls.append(f"https://annas-archive.org/search?index=journals&page=1&q={topic}&acc=aa_scidb&src=lgli&sort=newest&lang=en" + query_string)
    return start_urls


async def scrape_links(page, url):
    print(f"Scraping links from {url}")
    await page.goto(url)
    content = await page.content()
    soup = BeautifulSoup(content, 'html.parser')
    # main_content = soup.find('main')
    links = soup.find_all('a')
    new_links = []
    for link in links:
        if link.get('href') is not None and link.get('class') is not None and 'js-vim-focus' in link.get('class'):
            new_links.append(link.get('href'))
    file_pages = []
    for link in new_links:
        if "/md5" in link:
            file_pages.append("https://annas-archive.org" + link)
    return file_pages


async def login(browser, url):
    print(f"Logging in to {url}")
    page = await browser.new_page()
    await page.goto(url)
    return page

async def scrape_file_page(page, url):
    print(f"Scraping file page {url}")
    await page.goto(url)
    content = await page.content()
    soup = BeautifulSoup(content, 'html.parser')
    links = soup.find_all('a')
    links = [link.get('href') for link in links]
    for link in links:
        if link is not None:
            if link.startswith("https://annas-archive.org/scidb") or link.startswith("/scidb"):
                if link == "/scidb":
                    continue
                if link.startswith("/scidb"):
                    link = "https://annas-archive.org" + link
                await page.goto(link)
                break
    await page.wait_for_selector('button[type="submit"]')
    await page.click('button[type="submit"]')
    async def handle_download(download):
        # Save the PDF to a specific location
        print(f"Starting download: {download.suggested_filename}")
        await download.save_as(f"./dataset/raw_dataset/thesis/{download.suggested_filename}")
        print(f"Download finished: {download.suggested_filename}")
    page.on("download", handle_download)
    await page.click('a[href$=".pdf"]')  # Modify the selector as per your case
    await page.wait_for_timeout(1000)


async def main():
    login_url = "https://annas-archive.org"
    while True:
        async with async_playwright() as playwright:
            start_urls = load_start_urls()
            browser = await playwright.chromium.launch(headless=True, slow_mo=1000)
            for url in start_urls:
                try:
                    if os.path.exists("dataset/raw_dataset/thesis/visited_urls.txt"):
                        with open("dataset/raw_dataset/thesis/visited_urls.txt", "r") as f:
                            visited_urls = f.read().splitlines()
                        if url in visited_urls:
                            continue
                    else:
                        with open("dataset/raw_dataset/thesis/visited_urls.txt", "w") as f:
                            f.write("")
                    page = await login(browser, login_url)
                    file_pages = await scrape_links(page, url)
                    for file_page in file_pages:
                        await scrape_file_page(page, file_page)
                    with open("dataset/raw_dataset/thesis/visited_urls.txt", "a") as f:
                        f.write(url + "\n")
                except Exception as e:
                    print(e)
            browser.close()

if __name__ == "__main__":
    asyncio.run(main(), debug=True)
