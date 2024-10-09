## TODO underconstruction

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from training.model.llmodel import LLM_MODEL_NAME
def get_embedding(text):
    pass
## TODO use hugging face api directly if the results are the same
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline


if __name__ == "__main__":
    print(get_embedding("What is the revenue growth for IBM in 2007?"))