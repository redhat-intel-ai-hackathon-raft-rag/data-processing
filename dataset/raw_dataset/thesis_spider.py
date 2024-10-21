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
        published_years = [str(year) for year in range(2020, 2024)]
        query_strings = []
        for i in range(len(published_years)):
            query_string = f"&termtype_{i+1}=year&termval_{i+1}={published_years[i]}"
            query_strings.append(query_string)
        start_urls.append(f"https://annas-archive.org/search?index=journals&page=1&q={topic}&acc=aa_scidb&src=lgli&sort=newest&lang=en" + "".join(query_strings))
    return start_urls


async def scrape_links(page, url):
    await page.goto(url)
    content = await page.content()
    soup = BeautifulSoup(content, 'html.parser')
    main_content = soup.find('main')
    links = main_content.find_all('a')
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
    async with async_playwright() as playwright:
        start_urls = load_start_urls()
        for url in start_urls:
            try:
                browser = await playwright.chromium.launch(headless=True, slow_mo=1000)
                page = await login(browser, login_url)
                file_pages = await scrape_links(page, url)
                for file_page in file_pages:
                    await scrape_file_page(page, file_page)
                with open("dataset/raw_dataset/thesis/visited_urls.txt", "a") as f:
                    f.write(url + "\n")
            except Exception as e:
                print(e)
            finally:
                if browser is not None:
                    await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
