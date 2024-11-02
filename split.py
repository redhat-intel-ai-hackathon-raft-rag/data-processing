import json
import os
import random


def process_webpages(webpages_dir, prev_ver_dir, temp_file):
    print(temp_file)
    webpages_list = os.listdir(webpages_dir)
    random.shuffle(webpages_list)
    for file in webpages_list:
        filepath = os.path.join(webpages_dir, file)
        with open(filepath, 'r+') as webpage_file:
            try:
                data = json.load(webpage_file)
                if len(data) > 3:
                    print(f"Slicing file: {filepath}")
                    if not filepath.endswith('.json'):
                        continue
                    filepath_without_extension = filepath.split(".json")[0]
                    new_data = []
                    for i in range(len(data)):
                        new_data.append(data[i])
                        if len(new_data) == 3:
                            with open(f"{filepath_without_extension}\
                                        _{i-2}_{i}_.json", 'w') as f:
                                json.dump(new_data, f, indent=4)
                            new_data = []
                        if i == len(data) - 1 and len(new_data) > 0:
                            with open(f"{filepath_without_extension}\
                                    _last.json", 'w') as f:
                                json.dump(new_data, f, indent=4)
                    os.remove(filepath)
            except Exception as e:
                print(f"Error loading file {filepath}: {e}")
                print(f"Error on line: {e.__traceback__.tb_lineno}")
                continue


if __name__ == "__main__":
    webpages_dir = 'dataset/raw_dataset/dataset_web/'
    prev_ver_dir = 'dataset/raw_dataset/old_dataset_web/'
    raft_generated_dir = 'dataset/train_dataset_web/'
    random_num = random.randint(0, 1000000)
    print(f"Random number: {random_num}")
    temp_file = str(f"temp/temp_{random_num}.txt")
    with open(temp_file, 'w') as f:
        f.write("")
    process_webpages(webpages_dir, prev_ver_dir, temp_file)
