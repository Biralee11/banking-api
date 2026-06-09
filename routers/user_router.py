from fastapi import APIRouter, Depends, HTTPException
from schemas import UpdateEmailRequest, UpdatePasswordRequest
from database import SessionLocal
from models import UserModel
from auth import hash_password, verify_password, get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/user/me")
def view_profile(db = Depends(get_db), current_user = Depends(get_current_user)):
    user = db.query(UserModel).filter(UserModel.email == current_user["sub"]).first()
    return{"Username": user.username, "Email": user.email}

@router.put("/user/me")
def update_email(request: UpdateEmailRequest, db = Depends(get_db), current_user = Depends(get_current_user)):
    user = db.query(UserModel).filter(UserModel.email == current_user["sub"]).first()
    if user.email != request.email:
        user.email = request.email
    else:
        raise HTTPException(status_code=409, detail="Email already in use")
    db.commit()
    return {"message": "Email updated successfully"}

@router.put("/user/me/password")
def update_password(request: UpdatePasswordRequest, db = Depends(get_db), current_user = Depends(get_current_user)):
    user = db.query(UserModel).filter(UserModel.email == current_user["sub"]).first()
    if verify_password(request.password, user.password) == False:
        password = hash_password(request.password)
        user.password = password
    else:
        raise HTTPException(status_code=409, detail="New password must be different from current password")
    db.commit()
    return {"message": "Password updated successfully"}