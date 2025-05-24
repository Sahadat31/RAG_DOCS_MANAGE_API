from fastapi import APIRouter, UploadFile, File, Body, Depends
from typing import List
from services.file_upload import file_loader,embedder
from services.ask_query import question
from services.authentication.protectRoutes import get_current_user

router = APIRouter()

@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...), user: dict = Depends(get_current_user)):

    chunks = []
    for file in files:
        contents = await file.read()
        chunks.extend(file_loader.load_and_chunk_documents(file.filename, contents))

    embedder.generate_and_store_embeddings(chunks,user)
    return {"message": f"{len(files)} file(s) processed successfully", "chunks": len(chunks), "user": user}

@router.post("/ask")
async def ask_question(data: dict = Body(...), user: dict = Depends(get_current_user)):
    query = data.get("question")
    if not question:
        return {"error": "Missing question in request body."}
    answer = question.answer_query(query, user["sub"])
    return {"answer": answer}