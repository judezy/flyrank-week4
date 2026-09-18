import os
from fastapi import FastAPI, Body, HTTPException, status, Header
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# initialise supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Server running and connected to Supabase!"}

@app.post("/auth/signup", status_code=status.HTTP_201_CREATED)
def signup(payload: dict = Body(...)):
    email = payload.get("email")
    password = payload.get("password")

    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Email and password are required."}
        )

    try:
        response = supabase.auth.sign_up({"email": email, "password": password})
        return {"message": "User signed up successfully.", "data": response}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": str(e)}
        )

@app.post("/auth/login", status_code=status.HTTP_200_OK)
def login(payload: dict = Body(...)):
    email = payload.get("email")
    password = payload.get("password")

    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Email and password are required."}
        )

    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Invalid login credentials."}
        )

@app.get("/public/info", status_code=status.HTTP_200_OK)
def public_info():
    return {"message": "Welcome stranger! This info is public."}

@app.get("/protected/profile")
def protected_profile(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = {"error": "Access token required"}
        )

    token = authorization.split(" ")[1]

    return {"message": "Access granted"}

