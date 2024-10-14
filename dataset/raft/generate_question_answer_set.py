from llmmodel import text_generation_pipeline


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
                ## generate Chain-of-Thought style answer
                messages = [
                    {
                        "role": "system",
                        "content": """
                        You will be asked to generate an answer.
                        Instructions:
                        - Question: Present the question or problem clearly.
                        - Context/Information: Include any relevant information or context that will aid in reasoning.
                        - Reasoning Steps: Outline the logical steps taken to arrive at the answer. This might include:
                            Analyzing the question.
                            Identifying relevant facts or information from the context.
                            Performing calculations or comparisons if necessary.
                            Drawing conclusions based on the analysis.
                        - Answer: Present the final answer, clearly stated. Answer should be calm and authoritative.
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
