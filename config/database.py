import os

from dotenv import load_dotenv
from pymongo import MongoClient

# Load variables from .env
load_dotenv()

# Get MongoDB connection details
MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# Check that environment variables exist
if not MONGODB_URI:
    raise ValueError("MONGODB_URI is missing from .env")

if not DATABASE_NAME:
    raise ValueError("DATABASE_NAME is missing from .env")

# Connect to MongoDB
client = MongoClient(MONGODB_URI)

# Select our database
db = client[DATABASE_NAME]

# Collections
users_collection = db["users"]
customers_collection = db["customers"]
vehicles_collection = db["vehicles"]
services_collection = db["services"]
spare_parts_collection = db["spare_parts"]
invoices_collection = db["invoices"]
inventory_transactions_collection = db[
    "inventory_transactions"
]

print("MongoDB configuration loaded successfully.")