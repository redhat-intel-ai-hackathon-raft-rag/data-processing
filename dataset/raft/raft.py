from argparse import ArgumentParser
from datetime import datetime
import json

from dataset.raft.chunks_to_dataset import chunks_to_dataset
from dataset.raft.data_to_chunks import data_to_chunks


def raft(args):
    """
    1. Split the Text into Chunks: Divide the entire book or article
       into manageable chunks for easier processing.
    2. Generate Questions from Each Chunk:
       For each chunk, identify a golden document and formulate questions
       based on the content of that document.
    3. Create Answers: Using one of the generated questions
       and the corresponding golden document,
       create a Chain-of-Thought style answer.
    4. Construct Question-Answer Pairs:
        For PP fraction of the data:
            Format:
            {
                q:question+golden document+other chunks (distractors),
                a:answer from step 3
            }
        For (1−P)(1−P) fraction of the data:
            Format:
            {
                q:question+other chunks (distractors),
                a:answer from step 3
            }
    """
    file_name = args.file_path.split("/")[-1].split(".")[0]
    if args.doc_type not in ["pdf", "json", "json_array", "txt"]:
        raise ValueError("doc_type should be one of pdf, json, txt")
    if args.doc_type in ["json", "json_array"] and args.text_field_name is None:
        raise ValueError("text_field_name is required for json data")
    if args.doc_type in ["json"]:
        with open(args.file_path, "r") as f:
            data = f.read(1)
            if data.startswith("["):
                args.doc_type = "json_array"
    if args.doc_type not in ["json_array"]:
        combined_data = {}
        chunks = data_to_chunks(
            args.file_path,
            args.doc_type,
            args.text_field_name
        )
        if args.doc_type in ["json"]:
            with open(f"{args.file_path}", "r") as f:
                data = json.load(f)
            for key in data.keys():
                combined_data[key] = data[key]
            if "raft" not in data.keys():
                dataset = chunks_to_dataset(chunks)
                combined_data["raft"] = dataset
            with open(f"{args.output_folder}/raft_{file_name}.json", "w") as f:
                json.dump(combined_data, f, indent=4)
        else:
            dataset = chunks_to_dataset(chunks)
            with open(f"{args.output_folder}/raft_{file_name}.json", "w") as f:
                json.dump(dataset, f, indent=4)
    if args.doc_type in ["json_array"]:
        with open(args.file_path, "r") as f:
            data = json.load(f)
        combined_data = []
        for i, item in enumerate(data):
            # if item contains ['raft'] key, skip
            try:
                if "raft" in item.keys():
                    combined_data.append(item)
                    continue
                dataset = chunks_to_dataset(item[args.text_field_name])
                if len(dataset) == 0:
                    combined_data.append(item)
                    continue
                with open(f"{args.output_folder}/{i}_raft_{file_name}.json", "w") as f:
                    json.dump(dataset, f, indent=4)
                item["raft"] = dataset
                combined_data.append(item)
            except Exception as e:
                print(f"Error in processing data {i}: {e}")
                combined_data.append(item)
        with open(f"{args.file_path}", "r+") as f:
            f.seek(0)
            f.truncate()
            json.dump(combined_data, f, indent=4)


if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument("--doc_type", type=str, required=True)
    argparser.add_argument("--text_field_name", type=str, default=None)
    argparser.add_argument("--file_path", type=str, required=True)
    argparser.add_argument("--output_folder", type=str, required=True)
    args = argparser.parse_args()
    raft(args)
