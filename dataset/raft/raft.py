from argparse import ArgumentParser
from datetime import datetime
import json

from dataset.raft.chunks_to_dataset import chunks_to_dataset
from dataset.raft.data_to_chunks import data_to_chunks


def raft():
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
    argparser = ArgumentParser()
    argparser.add_argument("--file_path", type=str, required=True)
    argparser.add_argument("--doc_type", type=str, required=True)
    argparser.add_argument("--chunk_size", type=int, default=512)
    argparser.add_argument("--text_field_name", type=str, default=None)
    args = argparser.parse_args()
    chunks = data_to_chunks(
        args.file_path,
        args.doc_type,
        args.chunk_size,
        args.text_field_name
    )
    dataset = chunks_to_dataset(chunks)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    with open(f"dataset/generated_dataset_{timestamp}.json", "w") as file:
        json.dump(dataset, file)
