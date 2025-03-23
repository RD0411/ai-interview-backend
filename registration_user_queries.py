from firebase_admin import credentials, firestore, initialize_app

# Initialize Firebase (only run once)
cred = credentials.Certificate("firebase_key.json")  # Path to service account JSON file
initialize_app(cred)
db = firestore.client()  # Firestore client
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

        # Find the next available user ID
        new_user_id = max(existing_ids, default=999) + 1  # Start from 1000

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
