import json
import torch
from transformers import AutoTokenizer, pipeline, AutoModelForCausalLM
from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings

LLM_MODEL_NAME = "meta-llama/Llama-3.2-1B-Instruct"
model = AutoModelForCausalLM.from_pretrained(LLM_MODEL_NAME)
tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL_NAME)
text_generation_pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_length=1024,
        device=0 if torch.cuda.is_available() else -1)
text_splitter = SemanticChunker(HuggingFaceEmbeddings(model_name="BAAI/bge-m3"))


if __name__ == "__main__":
    from dataset.raft.generate_question_answer_set import generate_question_answer_set
    print(tokenizer("What is the capital of France?", return_tensors="pt"))
    chunks = ""
    with open("sample.txt", "r") as file:
        chunks = file.read()
    chunks = text_splitter.create_documents([chunks])
    num_chunks = len(chunks)
    idx = 0
    q_a_set = []
    for chunk in chunks:
        if len(chunk.page_content) > 800:
            parts = text_splitter.split_text(chunk.page_content)
            for part in parts:
                j_array = generate_question_answer_set(part)
                q_a_set.extend(j_array)
            continue
        j_array = generate_question_answer_set(chunk.page_content)
        q_a_set.extend(j_array)
    with open("qa_set.json", "w") as file:
        json.dump(q_a_set, file)
