from llmodel import question_answering_pipeline


def generate_answer_llm(question: str, context: str) -> str:
    """
    Uses a llm model to generate an answer
    to the given question based on the context, utilizing the GPU if available.
    """
    result = question_answering_pipeline(question=question, context=context)
    return result['answer']


if __name__ == "__main__":
    print(generate_answer_llm(
        "What is the capital of France?",
        "The capital of France is Paris."))
