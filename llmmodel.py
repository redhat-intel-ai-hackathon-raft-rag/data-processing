import json
import os
import torch
from transformers import AutoTokenizer, pipeline, AutoModelForCausalLM
from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
from FlagEmbedding import BGEM3FlagModel
from gcloud_conf import geminiclient
from langchain_text_splitters import CharacterTextSplitter
from langchain_text_splitters import TokenTextSplitter
from transformers import GPT2TokenizerFast
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv()

LLM_MODEL_NAME = "meta-llama/Llama-3.2-1B-Instruct"
model = AutoModelForCausalLM.from_pretrained(LLM_MODEL_NAME)
tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL_NAME)
# text_generation_pipeline = pipeline(
#         "text-generation",
#         model=model,
#         tokenizer=tokenizer,
#         max_length=1024,
#         device=0 if torch.cuda.is_available() else -1)
# text_splitter = SemanticChunker(HuggingFaceEmbeddings(model_name="BAAI/bge-m3"))
text_splitter = SemanticChunker(OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=os.getenv("OPENAI_API_KEY")))
percentile_chunker = SemanticChunker(OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=os.getenv("OPENAI_API_KEY")),
    breakpoint_threshold_type="percentile"
)
gradient_chunker = SemanticChunker(OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=os.getenv("OPENAI_API_KEY")),
    breakpoint_threshold_type="gradient"
)
# text_splitter = TokenTextSplitter(chunk_size=100, chunk_overlap=10)
# text_splitter = CharacterTextSplitter.from_huggingface_tokenizer(
#     GPT2TokenizerFast.from_pretrained("gpt2"), chunk_size=100, chunk_overlap=20
# )
# topic_model = SentenceTransformer('all-MiniLM-L6-v2')
topic_model = SentenceTransformer("BAAI/bge-m3")
ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", aggregation_strategy="simple")
bge_model = BGEM3FlagModel('BAAI/bge-m3',  use_fp16=True)


def text_generation_pipeline(messages):
    response = geminiclient.chat.completions.create(
        model="google/gemini-1.5-flash-002",
        messages=messages,
        stream=False
    )
    print(response)
    return response


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
