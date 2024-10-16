import os


if __name__ == "__main__":
    visited_urls_file = "dataset/raw_dataset/scraper/visited_urls.txt"
    if os.path.exists(visited_urls_file):
        with open(visited_urls_file, "r") as f:
            visited_urls = f.read().splitlines()
            # check for duplicates
            print(len(visited_urls))
            print(len(set(visited_urls)))
            if len(visited_urls) != len(set(visited_urls)):
                print("Duplicates found!")
            else:
                print("No duplicates found.")