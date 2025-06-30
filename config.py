from qdrant_client import models

COLLECTION_NAME = "myntra_products"  # using local memory as the database
VECTOR_SIZE = 384
DISTANCE = models.Distance.COSINE
DATA_PATH = "src/data/myntra_products_with_embeddings.joblib"
