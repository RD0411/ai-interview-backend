from fastapi import APIRouter, HTTPException
from registration_user_queries import create_user
from pydantic import BaseModel, EmailStr
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK with credentials (ensure your service account JSON file path is correct)
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)

# Define a Pydantic model for request validation
class User(BaseModel):
    email: EmailStr
    name: str
    password: str
    phone: str
    photo: str

# Initialize Firestore client after initializing Firebase app
router = APIRouter()
db = firestore.client()

@router.post("/register")
async def register_user(user: User):
    """
    Registers a new user and stores data in Firestore.

    :param user: User data validated by Pydantic
    :return: JSON response with success or error message
    """
    try:
        user_data = user.dict()  # Convert Pydantic model to dictionary
        result = create_user(db, user_data)  # Pass Firestore client and user data

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return {"message": "User registered successfully", "user_id": result["id"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
