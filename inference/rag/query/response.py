## TODO underconstruction

from llama_index.core.data_structs import Node
from llama_index.core.schema import NodeWithScore
from llama_index.core import get_response_synthesizer


response_synthesizer = get_response_synthesizer(response_mode="compact")


def synthesize_response(query_text: str, nodes: NodeWithScore):
    messages = [
        {
            "role": "system",
            "content": ""
        },
        {
            "role": "system",
            "content": " ".join([node.node.text for node in nodes]),
        },
        {
            "role": "user",
            "content": "query_text"
        }
    ]
    return response_synthesizer(messages)


if __name__ == "__main__":
    query_text = "What is the capital of France?"
    nodes = [NodeWithScore(Node(text="Paris"), 0.9)]
    response = synthesize_response(query_text, nodes)
    print(response)
