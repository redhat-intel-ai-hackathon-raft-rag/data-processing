import json
from datasets import load_from_disk


dataset = load_from_disk("dataset/raw_dataset/iCliniq_data_hf_dataset/train")
qa_json_arr = []
for row in dataset:
    j = {
        "question": row['input'],
        "answer": row['answer_icliniq']
    }
    qa_json_arr.append(j)
dataset = load_from_disk("dataset/raw_dataset/health_care_magic_hf_dataset/train")
for row in dataset:
    j = {
        "question": row['input'],
        "answer": row['output']
    }
    qa_json_arr.append(j)

with open('dataset/raw_dataset/qa.json', 'w') as f:
    json.dump(qa_json_arr, f)
