from flask import Flask, request
from pymongo import MongoClient
import africastalking
import os
from database import users_collection, transactions_collection, loans_collection , sacco_collection

# Initialize Africa's Talking SDK
username = os.environ.get("AFRICASTALKING_USERNAME")
api_key = os.environ.get("AFRICASTALKING_API_KEY")
africastalking.initialize(username, api_key)
sms = africastalking.SMS

app = Flask(__name__)

# Connect to MongoDB Atlas
mongodb_uri = os.environ.get("MONGODB_URI")
client = MongoClient(mongodb_uri)
db = client.get_database("banking_app")
users_collection = db["users"]
loans_collection = db["loans"]
transactions_collection = db["transactions"]
sacco_collection = db["transactions"]

# Options for use of funds questionnaire
USE_OF_FUNDS_OPTIONS = [
    "School",
    "Business",
    "Hospital",
    "Investments",
    "Other"
]

@app.route("/ussd", methods=["POST"])
def ussd():
    try:
        session_id = request.form.get("sessionId")
        service_code = request.form.get("serviceCode")
        phone_number = request.form.get("phoneNumber")
        text = request.form.get("text")
        print(f"Received a request for session: {session_id}")  # Log the session ID
        response = ""
        parts = text.split("*")

        if text == "":
            # This is the first request
            response = "CON Welcome to Our Bank. Choose an option:\n1. Check Balance\n2. Transfer Money\n3. Withdraw\n4. Lipa na meBank\n5. Table banking\n6. Apply for Loan\n7. Enroll to SACCO"

        elif parts[0] == "1":
            # User wants to check balance
            response = "CON Enter your PIN to check balance:"

        elif parts[0] == "2":
            # User wants to transfer money
            if len(parts) == 1:
                response = "CON Choose transfer option:\n1. Bank\n2. Phone"
            elif len(parts) == 2:
                if parts[1] == "1":
                    response = "CON Enter recipient's bank account number:"
                elif parts[1] == "2":
                    response = "CON Enter recipient's phone number:"
            elif len(parts) == 3:
                response = "CON Enter amount to transfer:"
            elif len(parts) == 4:
                response = "CON Enter your PIN to confirm the transfer:"
            elif len(parts) == 5:
                # Verify PIN and proceed with transfer if PIN is correct
                if verify_pin(phone_number, parts[-1]):
                    # Proceed with transfer logic
                    response = f"END ${parts[3]} successfully transferred to account {parts[1]}"
                    # Send confirmation SMS
                    send_sms(phone_number, f"Your transfer of {parts[3]} has been successfully completed.")
                else:
                    response = "END Incorrect PIN. Transfer canceled."

        elif parts[0] == "3":
            # User wants to withdraw
            response = "CON Enter your PIN to confirm withdrawal:"

        elif parts[0] == "4":
            # User wants to use Lipa na meBank
            response = "CON Enter your PIN to confirm the transaction:"

        elif parts[0] == "5":
            # User wants to access Table banking
            if len(parts) == 1:
                response = "CON Enter your PIN to check balance:"
                
        elif parts[0] == "6":
            # User wants to apply for a loan
            if len(parts) == 1:
                response = "CON Enter your Name:"
            elif len(parts) == 2:
                response = "CON Enter your ID Number:"
            elif len(parts) == 3:
                response = "CON Enter your Email:"
            elif len(parts) == 4:
                response = "CON Enter your Income:"
            elif len(parts) == 5:
                response = "CON Enter the Loan Amount:"

        elif len(parts) == 6 and parts[0] == "6":
            # Process loan application
            name, id_number, email, income, loan_amount = parts[1:]
            response = "CON Select the purpose of the loan:"
            for index, purpose in enumerate(USE_OF_FUNDS_OPTIONS, start=1):
                response += f"\n{index}. {purpose}"
            response += "\n0. Other (Please specify)"

        elif len(parts) == 7 and parts[0] == "6":
            # Process selected purpose of the loan
            selected_option = int(parts[-1])
            if selected_option > 0 and selected_option <= len(USE_OF_FUNDS_OPTIONS):
                purpose = USE_OF_FUNDS_OPTIONS[selected_option - 1]
            else:
                purpose = parts[-1]  # User specified other purpose
            loan_data = {
                "name": name,
                "id_number": id_number,
                "email": email,
                "income": income,
                "loan_amount": loan_amount,
                "use_of_funds": purpose,
                "guarantors": [],
                "status": "pending"  # Initial status of loan application
            }
            loans_collection.insert_one(loan_data)
            response = "END Loan application submitted successfully. We'll get back to you soon."
        
        elif parts[0] == "7":
            if len(parts) == 1:
                # Ask for name
                response = "CON Enter your Name:"
            elif len(parts) == 2:
                # Ask for ID Number
                response = "CON Enter your ID Number:"
            elif len(parts) == 3:
                # Ask for Email
                response = "CON Enter your Email:"
            elif len(parts) == 4:
                # Ask for Income
                response = "CON Enter your Income:"

        elif len(parts) == 5 and parts[0] == "7":
            # Process SACCO enrollment
            name, id_number, email, income = parts[1:]
            sacco_data = {
                "name": name,
                "id_number": id_number,
                "email": email,
                "income": income,
                # Add more fields as needed
            }
            # Insert SACCO data into the database (You need to define the SACCO collection)
            sacco_collection.insert_one(sacco_data)
            response = "END Enrolled to SACCO successfully. Welcome aboard!"

        return response

    except Exception as e:
        print(f"An error occurred: {e}")
        return "END An error occurred. Please try again later."

def verify_pin(phone_number, pin):
    user = users_collection.find_one({"phone_number": phone_number})
    if user and user.get("pin") == pin:
        return True
    return False

def send_sms(phone_number, message):
    try:
        sms.send(message, [phone_number])
    except Exception as e:
        print(f"Failed to send SMS: {e}")

if __name__ == "__main__":
    app.run(debug=True)
