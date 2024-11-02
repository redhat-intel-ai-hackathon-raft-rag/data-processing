import json
import os
from llmmodel import text_generation_pipeline


def get_medical_topics():
    medical_topics = []
    start_urls = []
    for root, dirs, files in os.walk("dataset/raw_dataset/dataset_web/"):
        for file in files:
            if file.endswith(".json"):
                print(os.path.join(root, file))
                try:
                    with open(os.path.join(root, file), "r+") as f:
                        json_data = json.load(f)
                        topics = []
                        for item in json_data:
                            for key in item.keys():
                                if key == "topics":
                                    topics.extend([topic["topic"] for topic in item[key]])
                        medical_topics.extend(topics)
                except Exception as e:
                    print(e)
    medical_topics = list(set(medical_topics))
    with open("dataset/knowledge_graph/medical_topics.txt", "w") as f:
        for topic in medical_topics:
            f.write(topic + "\n")
    refined_medical_topics = []
    for i, topic in enumerate(medical_topics):
        if i % 20 == 19 or i == len(medical_topics) - 1:
            messages = [
                {
                    "role": "system",
                    "content": """
                        You will be asked to select the medical topics from the topics provided.
                        Instructions:
                        - One topic per line
                        - Not including incorrect words in English
                        """
                },
                {
                    "role": "system",
                    "content":
                        """
                        - Include only the medical topics in your response
                        """
                },
                {"role": "user", "content": f"## Topics:\n {"\n".join(medical_topics[i - 19:i + 1])}"},
            ]
            topics = text_generation_pipeline(messages)
            try:
                topics = topics.choices[0].message.content
            except Exception:
                try:
                    topics = topics[0]["generated_text"][3]["content"]
                except Exception:
                    topics = topics.message.content[0].text
            print(topics)
            topics = topics.split("\n")
            refined_medical_topics.extend(topics)
    refined_medical_topics = list(set(refined_medical_topics))
    with open("dataset/knowledge_graph/refined_medical_topics.txt", "w") as f:
        for topic in refined_medical_topics:
            f.write(topic + "\n")
    # for topic in medical_topics:
    #     start_urls.append(f"https://www.semanticscholar.org/search?q={topic}&sort=influence")
    #     start_urls.append(f"https://www.semanticscholar.org/search?q={topic}&sort=relevance")
    #     start_urls.append(f"https://www.semanticscholar.org/search?q={topic}&sort=total-citations")
    # return start_urls


if __name__ == "__main__":
    print(get_medical_topics())
    # with open("dataset/raw_dataset/dataset_web/extracted_text_20241021_105748.json", "r+") as f:
    #     json_data = json.load(f)
    #     fixed_data = []
    #     for item in json_data:
    #         j = {}
    #         for key in item.keys():
    #             j[key] = item[key]
    #         j["topics"] = []
    #         j["topics"] = item["topics"]["topics"]
    #         fixed_data.append(j)
    #     print(fixed_data)
    #     f.seek(0)
    #     f.truncate()
    #     json.dump(fixed_data, f, ensure_ascii=False, indent=4)
