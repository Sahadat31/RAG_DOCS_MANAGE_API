from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGOURL = os.getenv("MONGODB_URL")
MONGOURL=MONGOURL.replace("USER",os.getenv("DB_USERNAME"))
MONGOURL=MONGOURL.replace("PASSWORD",os.getenv("DB_PASSWORD"))
client = MongoClient(MONGOURL)