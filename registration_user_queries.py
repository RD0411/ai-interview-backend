import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Get Firebase credentials from environment
cred_json = os.getenv("FIREBASE_CREDENTIALS")
if not cred_json:
    raise ValueError("Firebase credentials not found. Set FIREBASE_CREDENTIALS in .env.")
try:
    # Convert the credentials JSON string to a dictionary
    cred_dict = json.loads(cred_json)
    cred = credentials.Certificate(cred_dict)  # Load Firebase credentials
except json.JSONDecodeError:
    raise ValueError("Invalid JSON format in FIREBASE_CREDENTIALS.")

# Initialize Firebase app
try:
    firebase_admin.initialize_app(cred)
except Exception as e:
    raise RuntimeError(f"Failed to initialize Firebase app: {e}")

# Firestore client
db = firestore.client()

# Firestore collection name
collection_name = "users"

def create_user(user_data):
    """Stores user data in Firestore with a unique email and returns the generated user ID."""
    try:
        # Get all existing user documents
        users_ref = db.collection(collection_name).get()

        # Extract existing user IDs and emails
        existing_ids = [int(user.id) for user in users_ref if user.id.isdigit()]
        existing_emails = {user.to_dict().get("email") for user in users_ref}

        # Check if email is already registered
        if user_data["email"] in existing_emails:
            return {"error": "Email already registered. Please use a different email."}

        # Find the next available user ID (starting from 1000)
        new_user_id = max(existing_ids, default=999) + 1  

        if new_user_id > 9999:
            return {"error": "User limit exceeded (ID cannot exceed 9999)"}

        # Convert user ID to a string
        user_id = str(new_user_id)

        # Store data in Firestore under users -> user_id -> {user data}
        user_ref = db.collection(collection_name).document(user_id)
        user_ref.set(user_data)

        return {"id": user_id, "data": user_data}

    except Exception as e:
        # Log the error and return a user-friendly message
        return {"error": f"An error occurred while creating the user: {str(e)}"}