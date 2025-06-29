from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from .qdrant_service import get_client, create_collection_if_not_exists
from config import COLLECTION_NAME, DATA_PATH
from dotenv import load_dotenv
import joblib
from tqdm import tqdm
import os

# Load environment variables
load_dotenv()

BATCH_SIZE = 500

def index_products(df, batch_size=BATCH_SIZE):
    client = get_client()
    
    # First: Create collection and indexes
    create_collection_if_not_exists(client)
    
    total = len(df)

    for start in tqdm(range(0, total, batch_size), desc="Indexing Batches"):
        end = min(start + batch_size, total)
        batch = df.iloc[start:end]

        points = []
        for i, row in batch.iterrows():
            vector = row["DescriptionVector"].tolist()
            payload = {
                "product_name": row["ProductName"],
                "product_brand": row["ProductBrand"],
                "description": row["Description"],
                "gender": row["Gender"],
                "price": row["Price (INR)"],
                "color": row["PrimaryColor"],
            }
            points.append(PointStruct(id=i, vector=vector, payload=payload))

        client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )

if __name__ == "__main__":
    df = joblib.load(DATA_PATH)
    
    # Delete existing collection first to ensure clean rebuild
    print("Deleting existing collection...")
    client = get_client()
    try:
        client.delete_collection(COLLECTION_NAME)
        print(f"Deleted collection: {COLLECTION_NAME}")
    except Exception as e:
        print(f"Error deleting collection: {e}")
    
    # Now index with new schema
    index_products(df)