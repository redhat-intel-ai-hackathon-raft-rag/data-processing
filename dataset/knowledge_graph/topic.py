import json
import os
import re

from dataset.knowledge_graph.const import country_names
from dataset.knowledge_graph.const import country_names_with_government
from dataset.knowledge_graph.const import abbreviations_of_country
from llmmodel import text_generation_pipeline

def generate_topic(text: str):
        messages = [
            {
                "role": "system",
                "content": """
                    You will be asked to generate topics and proper_nouns.
                    Instruction:
                    - Topics should be unified words to construct a graph
                    - Lower score for proper nouns
                    - Significantly Higher score for medical topics
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
                    - Include only the topics and proper_nouns in your response.
                    - Topics should be the words appeared in the text
                    - Significantly Higher score for medical topics
                    - Significantly Higher score for health topics
                    - Only output at most the top 5 topics
                    """
            },
            {"role": "user", "content": "Generate topics based on the following text: " + text}
        ]
        topics = text_generation_pipeline(messages)
        try:
            topics = topics[0]["generated_text"][3]["content"]
            print(topics)
            try:
                topics = json.loads(topics)
            except Exception:
                topics = re.sub(r".*?({)", "{", topics)
                topics = re.sub(r"(}).*", "}", topics)
                # remove the word "json" from the output
                topics = re.sub(r"json", "", topics)
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
            return topics
        except Exception as e:
            raise e


if __name__ == "__main__":
    processing_complete = False
    while not processing_complete:
        processing_failed_count = 0
        for root, dirs, files in os.walk("dataset/raw_dataset/scraper/"):
            for file in files:
                if file.endswith(".json"):
                    print(os.path.join(root, file))
                    with open(os.path.join(root, file), "r+") as f:
                        try:
                            j_array = []
                            data = json.load(f)
                            for item in data:
                                if "topics" not in item.keys() or (item["topics"] is None):
                                    j = {}
                                    for key in item.keys():
                                        j[key] = item[key]
                                        if key == "text":
                                            try:
                                                j["topics"] = generate_topic(item[key])
                                            except Exception as e:
                                                print(e)
                                                processing_failed_count += 1
                                                j_array.append(j)
                            f.seek(0)
                            f.truncate()
                            json.dump(j_array, f, indent=4)
                        except Exception as e:
                            print(e)
                            # remove the content after the last "]"
                            read = f.read()
                            read = re.sub(r"\].*", "]", read)
                            # remove the "[]" i.e. empty list at the end
                            read = re.sub(r"\[\]", "", read)
                            # add the content back
                            f.write(read)
                            processing_failed_count += 1
        if processing_failed_count == 0:
            processing_complete = True
