import json
import os
import random


def process_json_files(raft_dir):
    rafts_list = os.listdir(raft_dir)
    random.shuffle(rafts_list)
    for file in rafts_list:
        if file.endswith('.json'):
            filepath = os.path.join(raft_dir, file)
            print(f"Processing file: {filepath}")
            with open(filepath, 'r+') as raft_file:
                data = json.load(raft_file)
                if "raft" not in data.keys():
                    os.remove(filepath)
                    continue
                raft = data["raft"]
                for entry in raft:
                    if "oracle_input" in entry.keys():
                        entry = entry.pop("oracle_input")
                with open("dataset/train_dataset_book/" + file, "w") as f:
                    json.dump(data['raft'], f, indent=4)
                # raft_file.seek(0)
                # raft_file.truncate()
                # json.dump(data, raft_file, indent=4)


if __name__ == "__main__":
    raft_dir = "dataset/raw_dataset/dataset_book"
    process_json_files(raft_dir)
