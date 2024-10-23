import os
import random
import time
from dotenv import load_dotenv
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
from vertexai.language_models import TextEmbeddingInput
from openai import OpenAI
from gcloud_conf import geminiclient, refresh_client, embedding_model, TaskType
import cohere
load_dotenv()


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
openaiclient = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

cohereclient = cohere.ClientV2(os.getenv("COHERE_API_KEY"))


def embedding_pipeline(texts: list[str], task_type: TaskType):
    inputs = [TextEmbeddingInput(text, task_type) for text in texts]
    return embedding_model.get_embeddings(inputs)


def text_generation_pipeline(messages):
    is_response_generated = False
    while not is_response_generated:
        try:
            response = geminiclient.chat.completions.create(
                model="google/gemini-1.5-flash-002",
                messages=messages,
                stream=False
            )
            is_response_generated = True
        except Exception as e:
            if "invalid" in str(e).lower():
                refresh_client()
                try:
                    response = geminiclient.chat.completions.create(
                        model="google/gemini-1.5-flash-002",
                        messages=messages,
                        stream=False
                    )
                    is_response_generated = True
                except Exception:
                    try:
                        response = openaiclient.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=messages,
                            stream=False
                        )
                        is_response_generated = True
                    except Exception:
                        cohere_message = []
                        for message in messages:
                            if 'context' in message:
                                cohere_message.append({
                                    "role": message["role"],
                                    "content": message["content"] +
                                                "\n" +
                                                "Context: " +
                                                message["context"]
                                })
                            else:
                                cohere_message.append(message)
                        try:
                            response = cohereclient.chat(
                                model="command-r-08-2024",
                                messages=cohere_message
                            )
                            is_response_generated = True
                        except Exception:
                            continue
            elif "RESOURCE_EXHAUSTED" in str(e):
                try:
                    response = openaiclient.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=messages,
                        stream=False
                    )
                    is_response_generated = True
                except Exception:
                    cohere_message = []
                    for message in messages:
                        if 'context' in message:
                            cohere_message.append({
                                "role": message["role"],
                                "content": message["content"] +
                                            "\n" +
                                            "Context: " +
                                            message["context"]
                            })
                        else:
                            cohere_message.append(message)
                    try:
                        response = cohereclient.chat(
                            model="command-r-08-2024",
                            messages=cohere_message
                        )
                        is_response_generated = True
                    except Exception:
                        continue
            else:
                raise e
        random_num = random.randint(5, 60)
        time.sleep(random_num)
    return response


# import json
# import torch
# from transformers import AutoTokenizer, pipeline, AutoModelForCausalLM
# from langchain_huggingface import HuggingFaceEmbeddings
# from sentence_transformers import SentenceTransformer
# from langchain_text_splitters import CharacterTextSplitter
# from langchain_text_splitters import TokenTextSplitter
# from transformers import GPT2TokenizerFast
# from FlagEmbedding import BGEM3FlagModel


# LLM_MODEL_NAME = "meta-llama/Llama-3.2-1B-Instruct"
# model = AutoModelForCausalLM.from_pretrained(LLM_MODEL_NAME)
# tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL_NAME)
# text_generation_pipeline = pipeline(
#         "text-generation",
#         model=model,
#         tokenizer=tokenizer,
#         max_length=1024,
#         device=0 if torch.cuda.is_available() else -1)
# text_splitter = SemanticChunker(HuggingFaceEmbeddings(model_name="BAAI/bge-m3"))
# text_splitter = TokenTextSplitter(chunk_size=100, chunk_overlap=10)
# text_splitter = CharacterTextSplitter.from_huggingface_tokenizer(
#     GPT2TokenizerFast.from_pretrained("gpt2"), chunk_size=100, chunk_overlap=20
# )
# topic_model = SentenceTransformer('all-MiniLM-L6-v2')
# topic_model = SentenceTransformer("BAAI/bge-m3")
# ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", aggregation_strategy="simple")
# bge_model = BGEM3FlagModel('BAAI/bge-m3',  use_fp16=True)

if __name__ == "__main__":
    print(len(embedding_pipeline(["Hello, world!", "Goodbye, world!"], TaskType.RETRIEVAL_QUERY)[1].values))
