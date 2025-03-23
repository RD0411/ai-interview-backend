import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Firebase credentials path from environment
cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

if not cred_path:
    raise ValueError("Firebase credentials not found. Set GOOGLE_APPLICATION_CREDENTIALS in .env.")

# Initialize Firebase
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

collection_name = "users"  # Firestore collection

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
        return {"error": str(e)}
