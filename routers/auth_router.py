from fastapi import APIRouter, Depends, HTTPException
from schemas import RegisterRequest, LoginRequest
from database import SessionLocal
from models import UserModel
from auth import hash_password, verify_password, create_access_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/auth/register")
def register(request: RegisterRequest, db = Depends(get_db)):
    if db.query(UserModel).filter(UserModel.username == request.username).first():
        raise HTTPException(status_code=409, detail="Username already taken")
    if db.query(UserModel).filter(UserModel.email == request.email).first():
        raise HTTPException(status_code=409, detail="Email already registered")
    password = hash_password(request.password)
    user = UserModel(username=request.username, email=request.email, password=password,role="User")
    db.add(user)
    db.commit()
    return {"message": "Registration successful", "username": request.username, "email": request.email}

@router.post("/auth/login")
def login(request: LoginRequest, db = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == request.email).first()   
    if not user or verify_password(request.password, user.password) == False:
        raise HTTPException(status_code=401, detail="Login failed, Invalid email or password")
    return create_access_token(data={"sub": user.email, "role": user.role})