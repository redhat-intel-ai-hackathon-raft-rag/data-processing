import torch
from llmodel import model, tokenizer


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


def generate_questions_llm(chunk: str, x: int = 5) -> list[str]:
    """
    Uses a llm model to generate `x` questions
    based on the given text chunk
    """
    input_text = f"Generate questions based on the following text: {chunk}"
    inputs = tokenizer(input_text, return_tensors="pt",
                       truncation=True, padding="longest").to(device)
    outputs = model.generate(
        inputs.input_ids,
        max_length=64,
        num_beams=x,  # Using beam search with `x` beams
        num_return_sequences=x  # Returning `x` sequences
    )
    questions = [
        tokenizer.decode(output, skip_special_tokens=True)
        for output in outputs
    ]
    return questions


if __name__ == "__main__":
    print(generate_questions_llm("What is the capital of France?", 1))
