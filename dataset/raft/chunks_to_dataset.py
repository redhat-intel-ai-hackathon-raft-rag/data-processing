import random
from typing import List
from dataset.raft.distructors_generator import distructors_generator
from dataset.raft.generate_question_answer_set import generate_question_answer_set
from llmmodel import text_splitter


def chunks_to_dataset(chunks: str, distuctor_only_dataset_ratio=0.2) -> List[dict]:
    chunks = text_splitter.create_documents([chunks])
    num_chunks = len(chunks)
    idx = 0
    dataset = []
    for chunk in chunks:
        if len(chunk.page_content) > 800:
            parts = text_splitter.split_text(chunk.page_content)
            for part in parts:
                j_array = generate_question_answer_set(part)
                for j in j_array:
                    d = {
                        "instruction": j["question"],
                        "input": chunk.page_content,
                        "chosen": j["answer"],
                        "rejected": ""
                    }
                    dataset.append(d)
            continue
        j_array = generate_question_answer_set(chunk.page_content)
        for j in j_array:
            dice = random.randint(0, 1)
            if dice > distuctor_only_dataset_ratio and num_chunks > 1:
                d = {
                    "instruction": j["question"],
                    "input": "\n".join(str(d) for d in distructors_generator(chunks, idx, num_distructors=3)),
                    "output": j["answer"]
                }
            elif dice <= distuctor_only_dataset_ratio and num_chunks > 1:
                d = {
                    "instruction": j["question"],
                    "input": "\n".join(str(d) for d in distructors_generator(chunks, idx, num_distructors=3)),
                    "output": j["answer"]
                }
            else:
                d = {
                    "instruction": j["question"],
                    "input": chunk.page_content,
                    "output": j["answer"]
                }
            dataset.append(d)
        idx += 1
    return dataset
