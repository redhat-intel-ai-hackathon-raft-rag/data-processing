
from datetime import datetime
import json
import os
import random

from langchain_text_splitters import RecursiveCharacterTextSplitter
from dataset.knowledge_graph.topic import generate_topic
from dataset.raft.chunks_to_dataset import chunks_to_dataset

import os
import json
from datetime import datetime
from llmmodel import percentile_chunker
text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)


def process_webpages(webpages_dir, prev_ver_dir, raft_generated_dir, temp_file):
    webpages_list = os.listdir(webpages_dir)
    random.shuffle(webpages_list)
    backup_checkpoint = datetime.now().timestamp()
    for file in webpages_list:
        if file.endswith('.json'):
            filepath = os.path.join(webpages_dir, file)
            print(f"Processing file: {filepath}")

            with open(filepath, 'r+') as webpage_file:
                try:
                    data = json.load(webpage_file)
                    for item in data[:]:
                        try:
                            print(f"Processing item: {item['url']}")
                            # # 1. check duplicate urls
                            # with open(temp_file, 'r+') as temporary_file:
                            #     visited_urls = temporary_file.read().splitlines()
                            #     if item['url'] in visited_urls:
                            #         print(f"Skipping file: {item['url']} at {filepath}")
                            #         data = [item for item in data if item['url'] != item['url']]
                            #         updated = True
                            #         json.dump(j_array, f, indent=4)
                            #         backup_filepath = os.path.join(prev_ver_dir, f'{backup_checkpoint}_{file}')
                            #         with open(backup_filepath, 'w') as backup_file:
                            #             json.dump(data, backup_file, indent=4)
                            #         webpage_file.seek(0)  # Move pointer to the start of the file
                            #         webpage_file.truncate()  # Clear file contents
                            #         json.dump(data, webpage_file, indent=4)
                            #         print(f"Updated file: {filepath}")
                            #         continue
                            #     # Mark URL as visited
                            #     temporary_file.write(f"{item['url']}\n")

                            # 2. check topics
                            ## 2.1 add topics if not exists
                            if "topics" not in item:
                                try:
                                    if len(item['text']) > 10000:
                                        temp_topics = []
                                        texts = text_splitter.split_text(item['text'])
                                        for text in texts:
                                            temp_topics.extend(generate_topic(text))
                                        item['topics'] = temp_topics
                                    else:
                                        item['topics'] = generate_topic(item['text'])
                                    backup_filepath = os.path.join(prev_ver_dir, f'{backup_checkpoint}_{file}')
                                    with open(backup_filepath, 'w') as backup_file:
                                        json.dump(data, backup_file, indent=4)
                                    webpage_file.seek(0)  # Move pointer to the start of the file
                                    webpage_file.truncate()  # Clear file contents
                                    json.dump(data, webpage_file, indent=4)
                                    print(f"Updated file: {filepath}")
                                except Exception as e:
                                    print(f"Error generating topics for {item['url']}: {e}")

                            ## 2.2 remove topic where score < 0.5
                            if "topics" in item and item['topics']:
                                if any(topic.get('score', 0) < 0.5 for topic in item['topics']):
                                    item['topics'] = [topic for topic in item['topics'] if topic.get('score', 0) >= 0.5]
                                    print(f"Updated topics for {item['url']} (Removed low-scoring topics)")
                                    backup_filepath = os.path.join(prev_ver_dir, f'{backup_checkpoint}_{file}')
                                    with open(backup_filepath, 'w') as backup_file:
                                        json.dump(data, backup_file, indent=4)
                                    webpage_file.seek(0)  # Move pointer to the start of the file
                                    webpage_file.truncate()  # Clear file contents
                                    json.dump(data, webpage_file, indent=4)
                                    print(f"Updated file: {filepath}")

                            # ## 2.3 remove item where topics: None or []
                            # if not item.get('topics'):
                            #     data = [item for item in data if item.get('topics')]
                            #     print(f"Removing item: {item['url']} due to empty topics")
                            #     updated = True
                            #     backup_filepath = os.path.join(prev_ver_dir, f'{backup_checkpoint}_{file}')
                            #     with open(backup_filepath, 'w') as backup_file:
                            #         json.dump(data, backup_file, indent=4)
                            #     webpage_file.seek(0)  # Move pointer to the start of the file
                            #     webpage_file.truncate()  # Clear file contents
                            #     json.dump(data, webpage_file, indent=4)
                            #     print(f"Updated file: {filepath}")
                            #     continue
                            # # ## 2.4 add raft generated q,a if not exists raft key
                            if "raft" not in item:
                                dataset = chunks_to_dataset(item['text'])
                                item['raft'] = dataset
                                print(f"Added raft for {item['url']}")
                                raft_generated_file_path = os.path.join(raft_generated_dir, f"raft_{datetime.now().timestamp()}_{file}")
                                with open(raft_generated_file_path, "w") as f:
                                    j_array = []
                                    for _ in dataset:
                                        j = {
                                            "instruction": _['instruction'],
                                            "input": _['input'],
                                            "output": _['output']
                                        }
                                        j_array.append(j)
                                    json.dump(j_array, f, indent=4)
                                    backup_filepath = os.path.join(prev_ver_dir, f'{backup_checkpoint}_{file}')
                                    with open(backup_filepath, 'w') as backup_file:
                                        json.dump(data, backup_file, indent=4)
                                    webpage_file.seek(0)  # Move pointer to the start of the file
                                    webpage_file.truncate()  # Clear file contents
                                    json.dump(data, webpage_file, indent=4)
                                    print(f"Updated file: {filepath}")
                        except Exception as e:
                            print(f"Error processing item {item['url']}: {e}")
                            print(f"Error on line: {e.__traceback__.tb_lineno}")
                            continue
                except Exception as e:
                    print(f"Error loading file {filepath}: {e}")
                    # line no of error
                    print(f"Error on line: {e.__traceback__.tb_lineno}")
                    continue


if __name__ == "__main__":
    webpages_dir = 'dataset/raw_dataset/dataset_web/'
    prev_ver_dir = 'dataset/raw_dataset/old_dataset_web/'
    raft_generated_dir = 'dataset/train_dataset_web/'
    random_num = random.randint(0, 1000000)
    print(f"Random number: {random_num}")
    temp_file = str(f"temp/temp_{random_num}.txt")
    # with open(temp_file, 'w') as f:
    #     f.write("")
    process_webpages(webpages_dir, prev_ver_dir, raft_generated_dir, temp_file)
