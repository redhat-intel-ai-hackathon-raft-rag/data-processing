import json
import os
import re
import random
from dataset.raft.chunks_to_dataset import chunks_to_dataset
from llmmodel import text_generation_pipeline
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=500)


def text_to_json(text):
    title_and_authors = extract_title_and_authors(text)
    rafts = extract_rafts(text)
    references = extract_references(text)
    return {
        "title_and_authors": title_and_authors,
        "raft": rafts,
        "references": references
    }


def _json_process(output):
    try:
        output = json.loads(output)
    except Exception:
        # remove any characters before the first "{"
        output = re.sub(r".*{", "{", output)
        # remove any characters after the last "}"
        output = re.sub(r"}.*", "}", output)
        # remove the word "json" from the output
        output = re.sub(r"json", "", output)
        # remove the word ``` from the output
        output = re.sub(r"```", "", output)
        # remove unnecessary spaces
        output = re.sub(r"\s+", " ", output)
        try:
            output = json.loads(output)
        except Exception:
            # find }{ and replace with },{
            output = re.sub(r"}{", "},{", output)
            # find } { and replace with },{
            output = re.sub(r"} {", "},{", output)
            # find " " and replace with ","
            output = re.sub(r"\" \"", "\",\"", output)
            try:
                output = json.loads(output)
            except Exception:
                try:
                    output = re.sub(r"([a-zA-Z0-9]+):", r'"\1":', output)
                    output = re.sub(r"([a-zA-Z0-9]+),", r'"\1",', output)
                    output = re.sub(r"([a-zA-Z0-9]+)}", r'"\1"}', output)
                    output = re.sub(r"({[a-zA-Z0-9]+)", r'{"\1"', output)
                    output = json.loads(output)
                except Exception:
                    try:
                        # remove the last line of the text
                        output = re.sub(r".*\n", "", output)
                        # remove the last delimiter
                        output = re.sub(r",", "", output)
                        output = json.loads(output)
                    except Exception:
                        print(output)
    if isinstance(output, str):
        output = json.loads(output)
    return output


def extract_title_and_authors(text):
    # first 15000 characters
    if len(text) > 15000:
        first_15000 = text[:15000]
    else:
        first_15000 = text
    messages = [
        {
            "role": "system",
            "content": """You will be asked to extract author names and titles
                author names: Names of the authors of the source.
                title: Title of the source.

                Only generate json data as following output format:
                {
                    "title": "title",
                    "author_names": ["author1", "author2"]
                }
                Don't generate two or more titles
                """
        },
        {
            "role": "system",
            "content": "Only generate a title and author names as json"
        },
        {
            "role": "user",
            "content": "Extract author names and titles based on the following text: " + first_15000
        }
    ]
    is_processed = False
    while not is_processed:
        questions = text_generation_pipeline(messages)
        try:
            try:
                # gemini
                questions = questions.choices[0].message.content
                print("gemini generated questions")
            except Exception:
                try:
                    # local or openai
                    questions = questions[0]["generated_text"][3]["content"]
                    print("local or openai generated questions")
                except Exception:
                    # cohere
                    questions = questions.message.content[0].text
                    print("cohere generated questions")
            questions = _json_process(questions)
            is_processed = True
        except Exception as e:
            print(e)
            print(e.__traceback__.tb_lineno)
            continue
    return questions


def extract_rafts(text):
    chunks = []
    if len(text) > 15000:
        chunks = text_splitter.split_text(text)
    else:
        chunks.append(text)
    rafts = []
    for chunk in chunks:
        try:
            dataset = chunks_to_dataset(chunk)
            rafts.extend(dataset)
        except Exception as e:
            print(chunk[:100] if len(chunk) > 100 else chunk)
            print(e)
            continue
    return rafts

    # chunks = []
    # if len(text) > 15000:
    #     chunks = text_splitter.split_text(text)
    # else:
    #     chunks.append(text)
    # raftss_list = []
    # for chunk in chunks:
    #     messages = [
    #             {
    #                 "role": "system",
    #                 "content": """You will be asked to extract problem, cited words, answer, and reasonings
    #                     - problem: Generate the most important questions from the text.
    #                     - cited words: Words or phrases that are directly quoted from a source with references to answer the problem.
    #                     - answer: The response in the text to the problem.
    #                     - reasonings: The reasonings or justifications in the text for the answer based on the cited words.
                        
    #                     Don't cite Figure or Table captions as cited words.

    #                     Only generate json data as following output format:
    #                     [
    #                         {
    #                             "problem": "problem1",
    #                             "cited_words": ["word1", "word2"],
    #                             "answer": "answer1",
    #                             "reasonings": ["reasoning1", "reasoning2"]
    #                         },
    #                     ]
    #                     field name should be enclosed in double quotes
    #                     """
    #             },
    #             {
    #                 "role": "user",
    #                 "content": "Extract problem, cited words, answer, and reasonings based on the following text: " + chunk
    #             }
    #     ]
    #     is_processed = False
    #     while not is_processed:
    #         rafts = text_generation_pipeline(messages)
    #         try:
    #             try:
    #                 # gemini
    #                 rafts = rafts.choices[0].message.content
    #                 print("gemini generated author names and titles")
    #             except Exception:
    #                 try:
    #                     # local or openai
    #                     rafts = rafts[0]["generated_text"][2]["content"]
    #                     print("local or openai generated author names and titles")
    #                 except Exception:
    #                     # cohere
    #                     rafts = rafts.message.content[0].text
    #                     print("cohere generated author names and titles")
    #             raftss_list.extend(_json_process(rafts))
    #             raftss_list = [
    #                 item for item in raftss_list
    #                 if "problem" in item["problem"]
    #                 or "questions" in item["problem"]
    #                 or "purpose" in item["problem"]
    #                 or "objective" in item["problem"]
    #                 or "aim" in item["problem"]
    #                 or "study" in item["problem"]
    #                 or "discussed" in item["problem"]
    #                 or "Source" in item["problem"]
    #                 or "source" in item["problem"]
    #                 or "research" in item["problem"]
    #                 or "text" in item["problem"]
    #                 or "paper" in item["problem"]
    #                 or "article" in item["problem"]
    #                 or "book" in item["problem"]
    #                 or "Text" in item["problem"]
    #             ]
    #             if len(raftss_list) == 0:
    #                 raise Exception("No problem, cited words, answer, and reasonings found")
    #             is_processed = True
    #         except Exception as e:
    #             print(e)
    # return raftss_list


def extract_references(text):
    if len(text) > 15000:
        last_15000 = text[-15000:]
    else:
        last_15000 = text
    messages = [{
                "role": "system",
                "content": """You will be asked to extract references
                    references: References are the sources of information that are cited in the text.
                    The section of the document that lists the references is typically titled "References."
                    at the end of the document.

                    Only generate json data as following output format:
                    [
                        {
                            "authors": ["author1", "author2"],
                            "title": "title1"
                        },
                        {
                            "authors": ["author1", "author2"],
                            "title": "title1"
                        }
                    ]
                    """
                },
                {
                    "role": "user",
                    "content": "Extract references based on the following text: " + last_15000
                }]
    is_processed = False
    while not is_processed:
        references = text_generation_pipeline(messages)
        try:
            try:
                # gemini
                references = references.choices[0].message.content
                print("gemini generated references")
            except Exception:
                try:
                    # local or openai
                    references = references[0]["generated_text"][3]["content"]
                    print("local or openai generated references")
                except Exception:
                    # cohere
                    references = references.message.content[0].text
                    print("cohere generated references")
            references = _json_process(references)
            is_processed = True
        except Exception as e:
            print(e)
            continue
    return references


if __name__ == '__main__':
    pdf_texts_dir = 'dataset/raw_dataset/pdf_texts'
    pdf_texts_files = os.listdir(pdf_texts_dir)
    random.shuffle(pdf_texts_files)
    os.makedirs('dataset/raw_dataset/pdf2jsondata', exist_ok=True)
    for pdf_text_file in pdf_texts_files:
        try:
            text = ""
            with open(os.path.join(pdf_texts_dir, pdf_text_file), 'r', encoding='utf-8') as f:
                text = f.read()
            text_json = text_to_json(text)
            title = pdf_text_file.split(".json")[0]
            if text_json["title_and_authors"].get("titles", None) is not None:
                title = text_json["title_and_authors"]["titles"]
            with open(f'dataset/raw_dataset/pdf2jsondata/{title}.json', 'w', encoding='utf-8') as f:
                json.dump(text_json, f, ensure_ascii=False, indent=4)
                os.remove(os.path.join(pdf_texts_dir, pdf_text_file))
        except Exception as e:
            print(f"Error in {pdf_text_file}: {e}")
            print(f"Error in Line: {e.__traceback__.tb_lineno}")
            continue
