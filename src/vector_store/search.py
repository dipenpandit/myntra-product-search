from .embeddings import get_model
from .qdrant_service import get_client, get_query_filters
from config import COLLECTION_NAME

model = get_model()
client = get_client()
# perform the vector search in qdrant
def search(query, model=model, client=client, collection_name=COLLECTION_NAME):
    query_filter = get_query_filters(query)
    xq = model.encode(query)
    search_results = client.search(
        collection_name = collection_name,
        query_vector = xq,
        query_filter = query_filter,
        limit = 5
    )
    return search_results