# 🧠 RAG Document AI API (FastAPI + MongoDB + Google Gemini)

This is a FastAPI backend for a Retrieval-Augmented Generation (RAG) system that:
- Accepts PDF/DOCX/TXT files from users
- Splits and embeds them using Google Gemini embeddings
- Stores embeddings in MongoDB
- Allows querying documents using Google Gemini LLM
- Uses JWT authentication for secure, user-specific access

---

## 🚀 Tech Stack

| Layer           | Tech                                 |
|----------------|--------------------------------------|
| Backend         | FastAPI                              |
| Embeddings      | Google Generative AI (Gemini)        |
| LLM             | Gemini-Pro via LangChain             |
| Vector Store    | FAISS (rebuilt in-memory from MongoDB) |
| Database        | MongoDB / MongoDB Atlas              |
| Auth            | JWT (via `python-jose`)              |

---

## ⚙️ Setup & Run

### 1. Clone the Repo

git clone https://github.com/your-username/rag-doc-ai-api.git
cd rag-doc-ai-api

### 2. Create and activate virtual environment

python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

### 3. Install requirements

pip install -r requirements.txt

### 4. Create a env file

MONGODB_URL=mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority
JWT_SECRET=your_super_secret_key
GOOGLE_API_KEY=your_google_gemini_api_key
DB_USERNAME=your_mongodb_username
DB_PASSWORD=db_password

### 5. Run the app
fastapi dev app/main.py

## Routes

### 1. POST: user/register
EXAMPLE BODY : 
{
  "firstName": "John",
  "lastName": "Doe",
  "email": "john@example.com",
  "password": "secure123"
}

### 2. POST: user/login
EXAMPLE BODY :
{
  "email": "john@example.com",
  "password": "secure123"
}


### 3. POST : documents/upload

Headers:Authorization: Bearer <JWT_TOKEN>
Content-Type: multipart/form-data
files: One or more .pdf, .docx, or .txt files

### 4. POST : document/ask

Headers:Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
BODY: {
  "question": "What is the warranty policy in the uploaded documents?"
}

## MONGODB STRUCTURE VIEW

### users

Stores user info + embeddingsProcessed: [doc_mapper_id]

### docs_to_embeddings_mapper

Maps doc uploads to embedding IDs

### embeddings

Stores each chunk, text, vector, and metadata

## SECURITY NOTES

JWT is used to protect all upload and query routes
Embeddings are user-specific and isolated
Passwords are hashed using bcrypt

## TEST CASES
pytest --cov=app tests/
coverage html  # View coverage in htmlcov/index.html



