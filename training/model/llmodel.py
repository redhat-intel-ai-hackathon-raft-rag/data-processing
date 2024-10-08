import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# Load LLaMA 3.2 model and tokenizer for both QQ and QA
LLM_MODEL_NAME = "meta-llama/Meta-Llama-3-8B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(LLM_MODEL_NAME)
question_answering_pipeline = pipeline(
        "question-answering",
        model=LLM_MODEL_NAME,
        device=0 if torch.cuda.is_available() else -1)
