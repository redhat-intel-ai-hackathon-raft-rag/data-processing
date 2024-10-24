from llmmodel import text_generation_pipeline
import time


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
                    - Generate at most 5 questions
                    - Questions should be complete sentences
                    - Questions should be answerable
                    - Questions should be specific
                    """
            },
            {
                "role": "system",
                "content":
                    """
                    - You should generate medical or health-related questions.
                    - Include only the questions in your response.
                    """
            },
            {"role": "user", "content": "Generate questions based on the following text: " + chunk}
    ]
    questions = text_generation_pipeline(messages)
    try:
        try:
            # gemini
            questions = questions.choices[0].message.content.split("\n")
        except Exception:
            try:
                # local or openai
                questions = questions[0]["generated_text"][3]["content"].split("\n")
            except Exception:
                # cohere
                questions = questions.message.content[0].text.split("\n")
        for question in questions:
            question = question.replace("Generate questions based on the following text:", "")
            if question == "" or question == " ":
                continue
            try:
                # generate Chain-of-Thought style answer
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
                        "role": "system",
                        "content":
                            """
                            - You should generate answer even if enough information is not provided.
                            - If there is not enough information to answer the question, you should state that.
                            """
                    },
                    {
                        "role": "user",
                        "content": question,
                        "context": chunk
                    }]
                answer = text_generation_pipeline(messages)
                try:
                    # gemini
                    answer = answer[0]["generated_text"][3]["content"]
                except Exception:
                    # local or openai
                    try:
                        answer = answer.choices[0].message.content
                    except Exception:
                        # cohere
                        answer = answer.message.content[0].text
                if question == "" or question == " " or question == "\n" or question is None:
                    raise Exception("Empty question")
                if answer == "" or answer == " " or answer == "\n" or answer is None:
                    raise Exception("Empty answer")
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
