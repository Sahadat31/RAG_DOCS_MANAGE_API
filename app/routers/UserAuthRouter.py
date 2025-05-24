from fastapi import APIRouter, HTTPException
from services.authentication.auth_services import hash_password, verify_password, create_access_token
from schema.user_model import UserCreate, UserLogin
from config.db import client

db = client["rag_docs_db"]
user_col = db["users"]

router = APIRouter()

@router.post("/register")
async def register(user: UserCreate):
    existing = user_col.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)
    result = user_col.insert_one({
        "firstName": user.firstName,
        "lastName": user.lastName,
        "email": user.email,
        "password": hashed_pw,
        "embeddingsProcessed": []
    })
    token = create_access_token({"sub": str(result.inserted_id), "email": user.email})
    return {"message": "User registered", "user_id": str(result.inserted_id), "access_token": token}

@router.post("/login")
async def login(credentials: UserLogin):
    user = user_col.find_one({"email": credentials.email})
    if not user or not verify_password(credentials.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user["_id"]), "email": user["email"]})
    return {"access_token": token, "token_type": "bearer"}
