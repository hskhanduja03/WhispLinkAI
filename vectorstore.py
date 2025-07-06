from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from embedder import embedding_model
import os
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")

def store_documents(docs, collection_name):
    vector_store = QdrantVectorStore.from_documents(
        documents=docs,
        embedding=embedding_model,
        collection_name=collection_name,
        url=QDRANT_URL,
    )

def get_retriever(collection_name):
    return QdrantVectorStore.from_existing_collection(
        collection_name=collection_name,
        url=QDRANT_URL,
        embedding=embedding_model
    ).as_retriever()
