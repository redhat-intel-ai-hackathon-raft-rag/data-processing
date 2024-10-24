import json
import os
from llmmodel import text_splitter, text_generation_pipeline


def text_to_json(text):
    title_and_authors = extract_title_and_authors(text)
    cited_words_and_reasoning = extract_cited_words_and_reasoning(text)
    references = extract_references(text)
    return {
        "title_and_authors": title_and_authors,
        "cited_words_and_reasoning": cited_words_and_reasoning,
        "references": references
    }


def extract_title_and_authors(text):
    # first 20000 characters
    if len(text) > 20000:
        first_20000 = text[:20000]
    else:
        first_20000 = text
        messages = [
            {
                "role": "system",
                "message": """You will be asked to extract author names and titles
                    author names: Names of the authors of the source.
                    titles: Titles of the source.
                    Only generate following output format:
                    Output format:
                    {
                        "author_names": ["author1", "author2"],
                        "titles": "title1",
                    }
                    """
            },
            {
                "role": "system",
                "message": "Only generate cited words and reasoning as json"
            },
            {
                "role": "user",
                "message": "Extract author names and titles based on the following text: " + first_20000
            }]
    questions = text_generation_pipeline(messages)
    try:
        try:
            # gemini
            questions = questions.choices[0].message.content.split("\n")
            print("gemini generated questions")
        except Exception:
            try:
                # local or openai
                questions = questions[0]["generated_text"][3]["content"].split("\n")
                print("local or openai generated questions")
            except Exception:
                # cohere
                questions = questions.message.content[0].text.split("\n")
                print("cohere generated questions")
        print(questions)
    except Exception as e:
        print(e)
    return questions


def extract_cited_words_and_reasoning(text):
    chunks = []
    if len(text) > 20000:
        chunks = text_splitter.split_text(text)
    else:
        chunks.append(text)
    cited_words_and_reasonings_list = []
    for chunk in chunks:
        messages = [
                {
                    "role": "system",
                    "message": """You will be asked to extract cited words and reasoning
                        cited words: Words or phrases that are directly quoted from a source.
                        reasoning: The explanation or justification for the cited words.

                        Indentifiers for cited words are as follows:
                        - Quotation Marks: Use quotation marks to indicate direct quotes (e.g., "quoted text").
                        - Italics: Sometimes, cited words or titles are italicized.
                        - Footnotes/Endnotes: References can be numbered and detailed at the bottom of the page or at the end of the document.
                        - Parenthetical References: Include citations in parentheses, usually with author and year (e.g., (Author, Year)).
                        - Inline Citations: Mention the source directly in the text, often with an accompanying reference list.
                        
                        Only generate following output format:
                        Output format:
                        {
                            "cited_words": ["word1", "word2"],
                            "reasoning": {
                                "word1": "reasoning1",
                                "word2": "reasoning2"
                            }
                        }
                        """
                },
                {
                    "role": "system",
                    "message": "Only generate cited words and reasoning as json"
                },
                {
                    "role": "user",
                    "message": "Extract cited words and reasoning based on the following text: " + chunk
                }
        ]
        cited_words_and_reasoning = text_generation_pipeline(messages)
        try:
            try:
                # gemini
                cited_words_and_reasoning = cited_words_and_reasoning.choices[0].message.content.split("\n")
                print("gemini generated author names and titles")
            except Exception:
                try:
                    # local or openai
                    cited_words_and_reasoning = cited_words_and_reasoning[0]["generated_text"][3]["content"].split("\n")
                    print("local or openai generated author names and titles")
                except Exception:
                    # cohere
                    cited_words_and_reasoning = cited_words_and_reasoning.message.content[0].text.split("\n")
                    print("cohere generated author names and titles")
            cited_words_and_reasonings_list.append(cited_words_and_reasoning)
        except Exception as e:
            print(e)
    return cited_words_and_reasonings_list


def extract_references(text):
    if len(text) > 20000:
        last_20000 = text[-20000:]
    else:
        last_20000 = text
    messages = [{
                "role": "system",
                "message": """You will be asked to extract references
                    references: References are the sources of information that are cited in the text.
                    The section of the document that lists the references is typically titled "References."
                    at the end of the document.

                    Only generate following output format:
                    Output format:
                    {
                        "references1": {
                            "authors": ["author1", "author2"],
                            "titles": "title1"
                        },
                        "references2": {
                            "authors": ["author1", "author2"],
                            "titles": "title1"
                        }
                    }
                    """
                },
                {
                    "role": "system",
                    "message": "Only generate references as json"
                },
                {
                    "role": "user",
                    "message": "Extract cited words and reasoning based on the following text: " + last_20000
                }]
    references = text_generation_pipeline(messages)
    try:
        try:
            # gemini
            references = references.choices[0].message.content.split("\n")
            print("gemini generated references")
        except Exception:
            try:
                # local or openai
                references = references[0]["generated_text"][3]["content"].split("\n")
                print("local or openai generated references")
            except Exception:
                # cohere
                references = references.message.content[0].text.split("\n")
                print("cohere generated references")
        print(references)
    except Exception as e:
        print(e)
    return references


if __name__ == '__main__':
    pdf_texts_dir = 'dataset/raw_dataset/pdf_texts'
    pdf_texts_list = os.listdir(pdf_texts_dir)
    os.makedirs('dataset/raw_dataset/pdf2jsondata', exist_ok=True)
    for text in pdf_texts_list:
        try:
            text_json = text_to_json(os.path.join(pdf_texts_dir, text))
            with open(f'dataset/raw_dataset/pdf2jsondata/{text}.json', 'w', encoding='utf-8') as f:
                json.dump(text_json, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error in {text}: {e}")
            continue
