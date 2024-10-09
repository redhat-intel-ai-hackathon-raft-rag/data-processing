## TODO underconstruction

from llama_index.core.data_structs import Node
from llama_index.core.schema import NodeWithScore
from llama_index.core import get_response_synthesizer


response_synthesizer = get_response_synthesizer(response_mode="compact")


def synthesize_response(query_text: str, nodes: NodeWithScore):
    response = response_synthesizer.synthesize(
        query_text, nodes=nodes
    )
    return response


if __name__ == "__main__":
    from loading_documents.documents import compose_documents
    from loading_documents.nodes import get_nodes_from_documents
    from query_node_preprocessor.node_processor import filter_nodes
    from query_node_preprocessor.rerank import rerank_processed_nodes
    query_text = "what is meaning of life"
    text_list = [
        "foo bar baz I'm really excited about foo bar baz",
        "I feel like a bird"
        ]
    documents = compose_documents(text_list)
    nodes = get_nodes_from_documents(documents)
    filtered_nodes = filter_nodes(nodes)
    reranked_nodes = rerank_processed_nodes(filter_nodes)
    response = synthesize_response(query_text, reranked_nodes)
