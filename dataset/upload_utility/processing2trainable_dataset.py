import json
import os
import random


def train_data_from_book_dataset(dataset_dir, train_dataset_dir):
    os.makedirs(train_dataset_dir, exist_ok=True)
    rafts_list = os.listdir(dataset_dir)
    random.shuffle(rafts_list)
    for file in rafts_list:
        if file.endswith('.json'):
            filepath = os.path.join(dataset_dir, file)
            print(f"Processing file: {filepath}")
            with open(filepath, 'r+') as raft_file:
                data = json.load(raft_file)
                if "raft" not in data.keys():
                    continue
                raft = data["raft"]
                for entry in raft:
                    if isinstance(entry, str):
                        # os.remove(filepath)
                        print(entry)
                        continue
                    if "oracle_context" in entry.keys():
                        entry.pop("oracle_context")
                with open(train_dataset_dir + "/" + file, "w") as f:
                    json.dump(data['raft'], f, indent=4)


def train_data_from_web_dataset(dataset_dir, train_dataset_dir):
    os.makedirs(train_dataset_dir, exist_ok=True)
    rafts_list = os.listdir(dataset_dir)
    random.shuffle(rafts_list)
    for file in rafts_list:
        if file.endswith('.json'):
            filepath = os.path.join(dataset_dir, file)
            print(f"Processing file: {filepath}")
            with open(filepath, 'r+') as raft_file:
                data = json.load(raft_file)
                for item in data:
                    if "raft" not in item.keys():
                        continue
                    raft = item["raft"]
                    for entry in raft:
                        if "oracle_context" in entry.keys():
                            entry.pop("oracle_context")
                rafts = [item["raft"] for item in data if "raft" in item.keys()]
                rafts = [raft for item in rafts for raft in item]
                if len(rafts) > 0:
                    with open(train_dataset_dir + "/" + file, "w") as f:
                        json.dump(rafts, f, indent=4)


if __name__ == "__main__":
    book_dataset_dir = "dataset/raw_dataset/dataset_book"
    web_dataset_dir = "dataset/raw_dataset/dataset_web"
    book_train_dataset_dir = "dataset/train_dataset_book"
    web_train_dataset_dir = "dataset/train_dataset_web"
    # train_data_from_book_dataset(book_dataset_dir, book_train_dataset_dir)
    train_data_from_web_dataset(web_dataset_dir, web_train_dataset_dir)
