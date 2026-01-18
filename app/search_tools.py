def vector_search(query, embedding_model, vindex, k=None):
    query_embedding = embedding_model.encode(
        query,
        normalize_embeddings=True
    )

    if k is None:
        return vindex.search(query_embedding)
    else:
        return vindex.search(query_embedding, num_results=k)
    
### Define the search tool for Pydantic AI
def make_vector_search_tool(embedding_model, vindex):
    def vector_search(query: str, k: int = 5):
        """
        Search completed Kaggle competitions using vector similarity.
        """
        query_embedding = embedding_model.encode(
            query,
            normalize_embeddings=True
        )
        return vindex.search(query_embedding, num_results=k)

    return vector_search

# def vector_search(query, embedding_model, vindex, k: int | None = 5):
#     """
#     Search completed Kaggle competitions using vector similarity.
#     """
#     query_embedding = embedding_model.encode(
#         query,
#         normalize_embeddings=True
#     )

#     if k is None:
#         return vindex.search(query_embedding)
#     return vindex.search(query_embedding, num_results=k)