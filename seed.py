from database import SessionLocal
from models import UserModel
from auth import hash_password

db = SessionLocal()
password = hash_password("B123456@")
user = UserModel(username="Bira", email="bira@gmail.com", password=password, role="Admin")
db.add(user)
db.commit()
print("Admin user created successfully")