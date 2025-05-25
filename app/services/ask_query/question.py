from dotenv import load_dotenv
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config.db import client
from bson import ObjectId

load_dotenv()
if client is None:
    raise RuntimeError("MongoDB client not initialized. Check environment variables.")
db = client["rag_docs_db"]
users_collection = db["users"]
docs_mapper_collection = db["docs_to_embeddings_mapper"]
embedded_collection = db["embeddings"]

def answer_query(question: str, user_id: str) -> str:
    
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    # find the user from user id
    current_user = users_collection.find_one({"_id": ObjectId(user_id)})
    processed_doc_ids = current_user.get("embeddingsProcessed",[])
    if not processed_doc_ids:
        return "No documents yet uploaded for this user"
    
    # get the embeddings based on doc id's -> embedded id's
    all_embedded_ids = []
    for doc_id in processed_doc_ids:
        doc = docs_mapper_collection.find_one({"_id": doc_id})
        # doc contains embeddings array
        if doc and "embeddings" in doc:
            all_embedded_ids.extend(doc["embeddings"])
    if not all_embedded_ids:
        return "No embeddings present to this user"
    
    # now fetch all the embedding chunks
    records = list(embedded_collection.find({"document_id": {"$in": all_embedded_ids}}))
    texts = [record["text"] for record in records]
    metadatas = [record.get("metadata",{}) for record in records]

    vectorstore = FAISS.from_texts(texts,embedding=embeddings,metadatas=metadatas)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2
    )
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=False
    )

    result = qa.invoke(question)
    return result
