import random
from typing import List
from dataset.raft.distructors_generator import distructors_generator
from dataset.raft.generate_question_answer_set import generate_question_answer_set
from llmmodel import text_splitter, percentile_chunker, gradient_chunker
    

def chunks_to_dataset(chunks: str, distuctor_only_dataset_ratio=0.2) -> List[dict]:
    if len(chunks) > 10000:
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
        if len(chunk) > 10000:
            print(f"Chunk too long: {len(chunk)}")
            parts = percentile_chunker.split_text(chunk)
            for part in parts:
                j_array = generate_question_answer_set(part)
                for j in j_array:
                    dice = random.randint(0, 1)
                    if dice > distuctor_only_dataset_ratio and num_chunks > 1:
                        d = {
                            "instruction": j["question"],
                            "input": "\n".join(str(d) for d in distructors_generator(chunks, idx, num_distructors=3)) + "\n" + part,
                            "oracle_input": part,
                            "output": j["answer"]
                        }
                    elif dice <= distuctor_only_dataset_ratio and num_chunks > 1:
                        d = {
                            "instruction": j["question"],
                            "input": "\n".join(str(d) for d in distructors_generator(chunks, idx, num_distructors=3)),
                            "oracle_input": part,
                            "output": j["answer"]
                        }
                    else:
                        d = {
                            "instruction": j["question"],
                            "input": part,
                            "oracle_input": part,
                            "output": j["answer"]
                        }
                    dataset.append(d)
            continue
        j_array = generate_question_answer_set(chunk)
        for j in j_array:
            dice = random.randint(0, 1)
            if dice > distuctor_only_dataset_ratio and num_chunks > 1:
                d = {
                    "instruction": j["question"],
                    "input": "\n".join(str(d) for d in distructors_generator(chunks, idx, num_distructors=3)) + "\n" + chunk,
                    "oracle_input": chunk,
                    "output": j["answer"]
                }
            elif dice <= distuctor_only_dataset_ratio and num_chunks > 1:
                d = {
                    "instruction": j["question"],
                    "input": "\n".join(str(d) for d in distructors_generator(chunks, idx, num_distructors=3)),
                    "oracle_input": chunk,
                    "output": j["answer"]
                }
            else:
                d = {
                    "instruction": j["question"],
                    "input": chunk,
                    "oracle_input": chunk,
                    "output": j["answer"]
                }
            dataset.append(d)
        idx += 1
    return dataset
