from qdrant_client import models

QDRANT_URL = "https://63ed5e76-957a-4631-9c5b-31ddf74939bb.eu-west-2-0.aws.cloud.qdrant.io:6333"
COLLECTION_NAME = "myntra_products"  # using local memory as the database
VECTOR_SIZE = 384
DISTANCE = models.Distance.COSINE
DATA_PATH = "src/data/myntra_products_with_embeddings.joblib"
