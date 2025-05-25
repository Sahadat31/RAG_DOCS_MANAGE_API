from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = None
MONGOURL = os.getenv("MONGODB_URL", "")
DB_USER = os.getenv("DB_USERNAME", "")
DB_PASS = os.getenv("DB_PASSWORD", "")

if MONGOURL and DB_USER and DB_PASS:
    MONGOURL = MONGOURL.replace("USER", DB_USER).replace("PASSWORD", DB_PASS)
    client = MongoClient(MONGOURL)