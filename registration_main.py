from fastapi import FastAPI
from registration_user_controller import router as user_router

# Initialize FastAPI app
app = FastAPI()

# Include the user controller
app.include_router(user_router)
@app.get("/")
def home():
    return {"message": "API is running!"}
