from qdrant_client import QdrantClient, models
from config import *
from qdrant_client.models import Filter, FieldCondition, MatchValue, Range
from src.vector_store.gemini_service import get_filters
import os
from dotenv import load_dotenv
load_dotenv()

def get_client():
    qdrant_client = QdrantClient(
        url=QDRANT_URL, 
        api_key=os.getenv("QDRANT_API_KEY"),
    )
    return qdrant_client


def create_collection_if_not_exists(client):
    try:
        client.get_collection(COLLECTION_NAME)
    except Exception:
        # Create collection
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=VECTOR_SIZE,
                distance=DISTANCE,
            ),
        )
        
        # Create payload indexes
        index_fields = [
            ("product_brand", "keyword"), # (field_name, field_schema)
            ("color", "keyword"),
            ("gender", "keyword"),
            ("price", "float")
        ]
        
        for field, schema in index_fields:
            client.create_payload_index(
                collection_name=COLLECTION_NAME,
                field_name=field,
                field_schema=schema
            )

def get_query_filters(query, get_filters=get_filters):
    filters = get_filters(query)  # using gemini
    # define conditions using each field conditions and then finally apply the filters
    conditions = []
    if filters["brand"] != "Not-Mentioned":
        conditions.append(FieldCondition(key="product_brand", match=MatchValue(value=filters["brand"])))
    if filters["color"] != "Not-Mentioned":
        conditions.append(FieldCondition(key="color", match=MatchValue(value=filters["color"])))
    if filters["gender"] != "Not-Mentioned":
        conditions.append(FieldCondition(key="gender", match=MatchValue(value=filters["gender"])))
    if filters["max_price"] or filters["min_price"]:
        price_range = Range()
        if filters["max_price"]:
            price_range.lte = filters["max_price"]
        if filters["min_price"]:
            price_range.gte = filters["min_price"]
        conditions.append(FieldCondition(key="price", range=price_range))

    query_filters = Filter(must=conditions)
    return query_filters



    





