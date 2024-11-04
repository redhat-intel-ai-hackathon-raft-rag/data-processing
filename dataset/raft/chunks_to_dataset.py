import random
from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter
from dataset.raft.distructors_generator import distructors_generator
from dataset.raft.generate_question_answer_set import generate_question_answer_set
from llmmodel import percentile_chunker
text_splitter = RecursiveCharacterTextSplitter(chunk_size=7500, chunk_overlap=750)


def chunks_to_dataset(chunks: str, distuctor_only_dataset_ratio=0.2) -> List[dict]:
    if len(chunks) > 7500:
        try:
            chunks = text_splitter.split_text(chunks)
        except Exception:
            print(chunks)
            raise
    else:
        chunks = [chunks]    
    num_chunks = len(chunks)
    idx = 0
    dataset = []
    print(f"Number of chunks: {num_chunks}")
    for chunk in chunks:
        if len(chunk) > 7500:
            print(f"Chunk too long: {len(chunk)}")
            parts = percentile_chunker.split_text(chunk)
            for part in parts:
                j_array = generate_question_answer_set(part)
                for j in j_array:
                    dice = random.randint(0, 1)
                    if dice > distuctor_only_dataset_ratio and num_chunks > 1:
                        d = {
                            "input": j["question"],
                            "instruction": "\n".join(str(d) for d in distructors_generator(chunks, idx, num_distructors=3)) + "\n" + part,
                            "oracle_context": part,
                            "output": j["answer"]
                        }
                    elif dice <= distuctor_only_dataset_ratio and num_chunks > 1:
                        d = {
                            "input": j["question"],
                            "instruction": "\n".join(str(d) for d in distructors_generator(chunks, idx, num_distructors=3)),
                            "oracle_context": part,
                            "output": j["answer"]
                        }
                    else:
                        d = {
                            "input": j["question"],
                            "instruction": part,
                            "oracle_context": part,
                            "output": j["answer"]
                        }
                    dataset.append(d)
            continue
        j_array = generate_question_answer_set(chunk)
        for j in j_array:
            dice = random.randint(0, 1)
            if dice > distuctor_only_dataset_ratio and num_chunks > 1:
                d = {
                    "input": j["question"],
                    "instruction": "\n".join(str(d) for d in distructors_generator(chunks, idx, num_distructors=3)) + "\n" + chunk,
                    "oracle_context": chunk,
                    "output": j["answer"]
                }
            elif dice <= distuctor_only_dataset_ratio and num_chunks > 1:
                d = {
                    "input": j["question"],
                    "instruction": "\n".join(str(d) for d in distructors_generator(chunks, idx, num_distructors=3)),
                    "oracle_context": chunk,
                    "output": j["answer"]
                }
            else:
                d = {
                    "input": j["question"],
                    "instruction": chunk,
                    "oracle_context": chunk,
                    "output": j["answer"]
                }
            dataset.append(d)
        idx += 1
    return dataset
