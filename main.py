from fastapi import FastAPI
from routers import accounts_router, auth_router, user_router

app = FastAPI()
app.include_router(accounts_router.router)
app.include_router(auth_router.router)
app.include_router(user_router.router)

@app.get("/")
def root():
    return{"message": "Banking API is running"}