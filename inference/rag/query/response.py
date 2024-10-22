## TODO underconstruction

from llama_index.core.data_structs import Node
from llama_index.core.schema import NodeWithScore
from llama_index.core import get_response_synthesizer


response_synthesizer = get_response_synthesizer(response_mode="compact")


def synthesize_response(query_text: str, nodes: NodeWithScore):
    pass


if __name__ == "__main__":
    pass
