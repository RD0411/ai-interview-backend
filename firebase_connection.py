import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import json


def initialize_firestore():
    """
    Initializes and returns the Firestore client after loading environment variables and Firebase credentials.
    """
    # Load environment variables
    print("Loading environment variables...")
    load_dotenv()

    # Get Firebase credentials from environment
    print("Fetching Firebase credentials...")
    cred_json = os.getenv("FIREBASE_CREDENTIALS")
    if not cred_json:
        raise ValueError("Firebase credentials not found. Set FIREBASE_CREDENTIALS in .env.")
    
    try:
        print("Parsing Firebase credentials JSON...")
        # Convert the credentials JSON string to a dictionary
        cred_dict = json.loads(cred_json)
        cred = credentials.Certificate(cred_dict)  # Load Firebase credentials
        print("Firebase credentials parsed successfully.")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format in FIREBASE_CREDENTIALS.")

    # Initialize Firebase app
    try:
        print("Initializing Firebase app...")
        firebase_admin.initialize_app(cred)
        print("Firebase app initialized successfully.")
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Firebase app: {e}")

    # Create and return Firestore client
    print("Creating Firestore client...")
    db = firestore.client()
    return db
