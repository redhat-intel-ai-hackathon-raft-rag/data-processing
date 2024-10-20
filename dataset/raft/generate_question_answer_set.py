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
    is_quota_limit = False
    while (not is_quota_limit):
        try:
            questions = text_generation_pipeline(messages)
            is_quota_limit = True
        except Exception as e:
            if "RESOURCE_EXHAUSTED" in str(e):
                is_quota_limit = False
                # wait for 5 seconds
                time.sleep(5)
            else:
                raise e
    try:
        try:
            # local or openai
            questions = questions[0]["generated_text"][2]["content"].split("\n")
        except Exception:
            # gemini
            questions = questions.choices[0].message.content.split("\n")
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
                        "role": "user",
                        "content": question,
                        "context": chunk
                    }]
                is_quota_limit = False
                while (not is_quota_limit):
                    try:
                        answer = text_generation_pipeline(messages)
                        is_quota_limit = True
                    except Exception as e:
                        if "RESOURCE_EXHAUSTED" in str(e):
                            is_quota_limit = False
                            # wait for 5 seconds
                            time.sleep(5)
                        else:
                            raise e
                try:
                    # local or openai
                    answer = answer[0]["generated_text"][2]["content"]
                except Exception:
                    # gemini
                    answer = answer.choices[0].message.content
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
