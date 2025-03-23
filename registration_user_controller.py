from fastapi import APIRouter
from registration_user_queries import create_user
from pydantic import BaseModel, EmailStr

# Define a Pydantic model for request validation
class User(BaseModel):
    email: EmailStr  # Ensures valid email format
    name: str
    password: str
    phone: str
    photo: str

router = APIRouter()

@router.post("/register")
async def register_user(user: User):
    """Registers a new user and stores data in Firestore."""
    return create_user(user.dict())
