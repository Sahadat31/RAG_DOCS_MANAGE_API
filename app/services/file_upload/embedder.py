from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from concurrent.futures import ThreadPoolExecutor
from app.config.db import client
from datetime import datetime
from bson import ObjectId
import uuid
import os

load_dotenv()
key = os.getenv("GOOGLE_API_KEY")
if key:
    os.environ["GOOGLE_API_KEY"] = key


def generate_and_store_embeddings(chunks,user):
    if client is None:
        raise RuntimeError("MongoDB client not initialized. Check environment variables.")
    db = client["rag_docs_db"]
    embedded_collection = db["embeddings"]       # embeddings will have collection of all the embedded chunks
    docs_to_embeddings_collection = db["docs_to_embeddings_mapper"]    # it will have uploaded docs id - all embeddings mapper array
    user_collection = db["users"]       # contains all user data, also an array of embeddingsProcessed
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # Embed in parallel
    def embed_chunk(chunk):
        return embeddings.embed_query(chunk.page_content)

    print(f"Embedding {len(chunks)} chunks using multithreading...")

    with ThreadPoolExecutor(max_workers=8) as executor:
        vectors = list(executor.map(embed_chunk, chunks))

    records = []
    embedded_ids = []
    for i, chunk in enumerate(chunks):
        id = chunk.metadata.get("document_id", str(uuid.uuid4()))
        embedded_ids.append(id)
        record = {
            "document_id": id,
            "text": chunk.page_content,
            "embedding": vectors[i],
            "metadata": chunk.metadata,
        }
        records.append(record)
    
    # store the embedded chunks into database
    if records:
        embedded_collection.insert_many(records)
        print(f"✅ Inserted {len(records)} embeddings into MongoDB embeddings collection.")
        # create mapping for uploaded docs to embeddings
        data = {
            "embedding_count": len(records),
            "embeddings": embedded_ids,
            "timestamp": datetime.now(),
            "email": user["email"]
        }
        saved_data = docs_to_embeddings_collection.insert_one(data)
        print("Inserted mapping into docs to embedddings collection.",saved_data.inserted_id)
        # create user to docs id mapping
        result = user_collection.update_one(
            {"_id": ObjectId(user["sub"])},  
            {"$push": {"embeddingsProcessed": saved_data.inserted_id}}
        )
        if result.modified_count == 1:
            print(f"✅ Added embedding {saved_data.inserted_id} to user {user["sub"]}")
        else:
            print(f"⚠️ Failed to update user {user["sub"]}")
    else:
        print("⚠️ No records to insert.")
