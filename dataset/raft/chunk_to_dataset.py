import random
from typing import List
from dataset.raft.generate_question_answer_set import generate_question_answer_set
from llmmodel import text_splitter


def chunks_to_dataset(chunks: List[str]):
    chunks = text_splitter.create_documents([chunks])
    num_chunks = len(chunks)
    idx = 0
    dataset = []
    ## TODO implement the distruction i.e. the rejection of the answer
    for chunk in chunks:
        if len(chunk.page_content) > 800:
            parts = text_splitter.split_text(chunk.page_content)
            for part in parts:
                j_array = generate_question_answer_set(part)
                for j in j_array:
                    d = {
                        "instruction": j["question"],
                        "input": chunk,
                        "chosen": j["answer"],
                        "rejected": ""
                    }
                    dataset.append(d)
            continue
        j_array = generate_question_answer_set(chunk.page_content)
        for j in j_array:
            d = {
                "instruction": j["question"],
                "input": chunk,
                "chosen": j["answer"],
                "rejected": ""
            }
            dataset.append(d)
    return dataset
