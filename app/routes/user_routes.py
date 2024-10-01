from fastapi import APIRouter, Response, status
from db.supabase import create_supabase_client
from app.models import User
#fn dependencies
import bcrypt

# Initialize supabase client
supabase = create_supabase_client()

# Initialize the router object
router = APIRouter()

def user_exists(key: str = "email", value: str = None):
    user = supabase.from_("users").select("*").eq(key, value).execute()
    return len(user.data) > 0

# POST NEW USER
@router.post("/")
def create_user(user: User, response: Response):
    try:
        # Convert email to lowercase
        user_email = user.email.lower()
        # Hash password
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bytes(bcrypt.gensalt()))

        # Check if user already exists
        if user_exists(value=user_email):
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"message": "User already exists"}

        # Add user to users table
        user = supabase.from_("users")\
            .insert({"first_name": user.first_name, "last_name": user.last_name, "password": str(hashed_password), "email": user_email, })\
            .execute()

        # Check if user was added
        if user:
            return {"message": "User created successfully"}
        else:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"message": "User creation failed"}
    except Exception as e:
        print("Error: ", e)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "User creation failed"}