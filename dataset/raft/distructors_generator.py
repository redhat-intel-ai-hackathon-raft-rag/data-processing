import random


def distructors_generator(chunks: list,
                          current_chunk_index: int,
                          num_distructors: int) -> list:
    """
    Generate a list of distructors for the raft system.
    distructors are the chunks that are not the current chunk
    """
    num_chunks = len(chunks)
    if num_chunks == 1:
        raise ValueError(
            "There is only one chunk, can't generate distructors")
    if num_distructors >= num_chunks:
        num_distructors = num_chunks - 1
    distructors = []
    for i in range(num_distructors):
        distructor_index = random.randint(0, num_chunks - 1)
        while distructor_index == current_chunk_index:
            distructor_index = random.randint(0, num_chunks - 1)
        distructors.append(chunks[distructor_index].page_content)
    return distructors
