from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import FileUploadRouter,UserAuthRouter

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(FileUploadRouter.router, prefix="/documents")
app.include_router(UserAuthRouter.router, prefix="/user")

