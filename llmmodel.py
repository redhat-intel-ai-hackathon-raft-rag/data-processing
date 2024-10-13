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


def generate_question_answer_set(chunk: str):
    j_array = []
    messages = [
            {
                "role": "system",
                "content": """
                    You will be asked to generate questions.
                    Instructions:
                    - Generate one question per line
                    - Generate only questions
                    - Questions should be succinct
                    - Questions should be complete sentences
                    - Questions should be self-contained
                    - Questions should be answerable
                    - Questions should be specific
                    """
            },
            {
                "role": "system",
                "content":
                    """
                    - The questions should be able to be answered in a few words or less.
                    - Include only the questions in your response.
                    """
            },
            {"role": "user", "content": "Generate questions based on the following text: " + chunk}
    ]
    questions = text_generation_pipeline(messages)
    try:
        questions = questions[0]["generated_text"][3]["content"].split("\n")
        for question in questions:
            question = question.replace("Generate questions based on the following text:", "")
            try:
                messages = [
                    {
                        "role": "system",
                        "content": """
                        You will be asked to generate an answer.
                        Instructions:
                        - Provide a concise answer to the question.
                        - Provide a summary of how you reached your answer.
                        - Answer should be calm and authoritative.
                        """
                    },
                    {
                        "role": "user",
                        "content": question,
                        "context": chunk
                    }]
                answer = text_generation_pipeline(messages)
                answer = answer[0]["generated_text"][2]["content"]
                j = {
                    "question": question,
                    "answer": answer
                }
                j_array.append(j)
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
    return j_array


if __name__ == "__main__":
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
