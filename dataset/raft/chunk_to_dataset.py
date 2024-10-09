import random
from raft.generate_questions_llm import generate_questions_llm
from raft.generate_answer_llm import generate_answer_llm


def chunk_to_dataset(data_chunks):
    ## TODO data store to generate wrong question/answer pairs: documents in the same domain is preferable
    ## current implementation is generating wrong question/answer pairs from other chunk in the chunks
    dataset = []
    index = 0
    for chunk in data_chunks:
        questions = generate_questions_llm(chunk, 1)
        ## TODO pick data chuck other than chunk of current index
        wrong_chunk = data_chunks[]
        wrong_questions = generate_questions_llm(wrong_chunk, 1)
        for question in questions:
            d = {
                "instruction": "",
                "input": "",
                "chosen": "",
                "rejected": ""
            }
            d["instruction"] = question  ## i.e. question
            d["input"] = chunk
            d["chosen"] = generate_answer_llm(d["instruction"], d["input"])
            d["rejected"] = generate_answer_llm(wrong_questions[random.randint(0,len(wrong_questions))]), d['input']
    return dataset


if __name__ == "__main__":
    print(generate_questions_llm("What is the capital of France?", 1))
    print(generate_answer_llm("What is the capital of France?", "The capital of France is Paris."))
    data_chunks = ["What is the capital of France?", "The capital of France is Paris."]
    print(chunk_to_dataset(data_chunks))
