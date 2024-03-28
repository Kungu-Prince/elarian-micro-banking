from pymongo import MongoClient


# Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://KunguPrince:0987654321qweasd@cluster0.9bns4v3.mongodb.net/")
db = client.get_database("banking_app")

# Define schema for the Users collection
users_collection = db["users"]
users_schema = {
    "name": str,
    "phone_number": str,
    "pin": str,  # Assuming PIN is stored as a string for simplicity
    # Add other fields as needed
}

# Define schema for the Transactions collection
transactions_collection = db["transactions"]
transactions_schema = {
    "user_id": str,
    "transaction_type": str,
    "amount": float,
    "timestamp": str,  # Assuming timestamp is stored as a string for simplicity
    # Add other fields as needed
}

# Define schema for the Loans collection
loans_collection = db["loans"]
loans_schema = {
    "user_id": str,
    "amount": float,
    "purpose": str,
    "status": str,
    "start_date": str,
    "due_date": str,
    "qualification_questionnaire": {
        "name": str,
        "id_number": str,
        "email": str,
        "income": float,
        "loan_amount": float,
        "use_of_funds": str,
        "guarantors": [],  # List of guarantors (if applicable)
        # Add other fields as needed
    }
}
sacco_collection = db["sacco"]
sacco_schema = {
    "name": str,
    "id_number": str,
    "email": str,
    "income": float,
    # Add other fields as needed
    }
