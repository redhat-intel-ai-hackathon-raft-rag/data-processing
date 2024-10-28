import json
import os
import re
import time

from dataset.knowledge_graph.const import country_names
from dataset.knowledge_graph.const import country_names_with_government
from dataset.knowledge_graph.const import abbreviations_of_country
from llmmodel import text_generation_pipeline, text_splitter, percentile_chunker

def generate_topic(text: str) -> list[dict]:
        messages = [
            {
                "role": "system",
                "content": """
                    You will be asked to generate topics and proper_nouns.
                    Instruction:
                    - Topics should be unified words to construct a graph
                    - Topics should be the words appeared in the text
                    - If the text have no relevant topics, return nothing
                    - Extract topics from the text as json format with score by each topic 
                    - Output should be in the following format without any additional information
                    sample output:
                    {
                        "topics": [
                            {"topic": "Apple", "score": 0.9},
                            {"topic": "startup", "score": 0.8},
                            {"topic": "U.K.", "score": 0.7}
                        ]
                    }
                    """
            },
            {
                "role": "system",
                "content":
                    """
                    - No words other than the json output
                    - Include only the topics in your response
                    - Topics should be the words appeared in the text
                    - Output at most the top 5 topics
                    - Significantly Higher score for medical topics
                    - Significantly Higher score for health topics
                    - Lower score for proper nouns
                    """
            },
            {"role": "user", "content": "Generate topics based on the following text: " + text}
        ]
        topics = text_generation_pipeline(messages)
        try:
            try:
                topics = topics.choices[0].message.content
            except Exception:
                try:
                    topics = topics[0]["generated_text"][3]["content"]
                except Exception:
                    topics = topics.message.content[0].text
            try:
                topics = json.loads(topics)
            except Exception:
                # remove any characters before the first "{"
                topics = re.sub(r".*{", "{", topics)
                # remove any characters after the last "}"
                topics = re.sub(r"}.*", "}", topics)
                # remove the word "json" from the output
                topics = re.sub(r"json", "", topics)
                # remove the word ``` from the output
                topics = re.sub(r"```", "", topics)
                # remove unnecessary spaces
                topics = re.sub(r"\s+", " ", topics)
                try:
                    topics = json.loads(topics)
                except Exception as e:
                    if "Expecting ',' delimiter" in str(e):
                        # find }{ and replace with },{
                        topics = re.sub(r"}{", "},{", topics)
                        # find } { and replace with },{
                        topics = re.sub(r"} {", "},{", topics)
                        try:
                            topics = json.loads(topics)
                        except Exception as e:
                            if e.__class__.__name__ == "JSONDecodeError":
                                try:
                                    topics = re.sub(r"([a-zA-Z0-9]+):", r'"\1":', topics)
                                    topics = re.sub(r"([a-zA-Z0-9]+),", r'"\1",', topics)
                                    topics = re.sub(r"([a-zA-Z0-9]+)}", r'"\1"}', topics)
                                    topics = re.sub(r"({[a-zA-Z0-9]+)", r'{"\1"', topics)
                                    topics = json.loads(topics)
                                except Exception as e:
                                    if e.__class__.__name__ == "JSONDecodeError":
                                        # remove the last line of the text
                                        topics = re.sub(r".*\n", "", topics)
                                        # remove the last delimiter
                                        topics = re.sub(r",", "", topics)
                                        topics = json.loads(topics)
            if topics is None or topics == {}:
                return topics
            for topic in topics["topics"]:
                if topic["topic"] in country_names or country_names_with_government or abbreviations_of_country:
                    topics["topics"].remove(topic)
                # remove topic which contains only digits or string of digits
                # try to convert to integer
                try:
                    digit = int(topic["topic"])
                    if digit.isdigit():
                        topics["topics"].remove(topic)
                except Exception:
                    pass
            # remove duplicate topics
            topics["topics"] = list({v['topic']: v for v in topics["topics"]}.values())
            return topics["topics"]
        except Exception as e:
            # the line where the error occurred
            print(e)
            print(e.__traceback__.tb_lineno)
            raise e

def handle_large_text(text: str):
    texts = []
    text_length = len(text)
    if text_length > 100000:
        try:
            chunks = text_splitter.split_text(text)
        except Exception:
            chunks = percentile_chunker.split_text(text)
        for chunk in chunks:
            temp_texts = handle_large_text(chunk)
            texts.extend(temp_texts)
    return texts


if __name__ == "__main__":
    while True:
        for root, dirs, files in os.walk("dataset/raw_dataset/scraper/"):
            for file in files:
                if file.endswith(".json"):
                    print(os.path.join(root, file))
                    with open(os.path.join(root, file), "r+") as f:
                        try:
                            j_array = []
                            data = json.load(f)
                            for item in data:
                                j = {}
                                for key in item.keys():
                                    j[key] = item[key]
                                if "topics" not in item.keys():
                                    try:
                                        j["topics"] = generate_topic(item["text"])
                                    except Exception as e:
                                        print(e)
                                        if "Request too large" in str(e):
                                            texts = handle_large_text(item["text"])
                                            temp_j_array = []
                                            for text in texts:
                                                try:
                                                    topics = generate_topic(text)
                                                    temp_j = {}
                                                    for key in j.keys():
                                                        temp_j[key] = j[key]
                                                    temp_j["topics"] = topics
                                                    temp_j_array.append(temp_j)
                                                    continue
                                                except Exception as e:
                                                    print(e.__traceback__.tb_lineno)
                                                    print(e)
                                j_array.append(j)
                            f.seek(0)
                            f.truncate()
                            json.dump(j_array, f, indent=4)
                        except Exception as e:
                            print(e)
