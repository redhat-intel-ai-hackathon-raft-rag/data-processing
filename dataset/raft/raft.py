from argparse import ArgumentParser
from datetime import datetime
import json

from dataset.raft.chunks_to_dataset import chunks_to_dataset
from dataset.raft.data_to_chunks import data_to_chunks


def raft():
    argparser = ArgumentParser()
    argparser.add_argument("--file_path", type=str, required=True)
    argparser.add_argument("--doc_type", type=str, required=True)
    argparser.add_argument("--chunk_size", type=int, default=512)
    argparser.add_argument("--text_field_name", type=str, default=None)
    args = argparser.parse_args()
    chunks = data_to_chunks(args.file_path, args.doc_type, args.chunk_size, args.text_field_name)
    dataset = chunks_to_dataset(chunks)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    with open(f"dataset/generated_dataset_{timestamp}.json", "w") as file:
        json.dump(dataset, file)
