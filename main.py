from fastapi import FastAPI, HTTPException, Depends
from random import randint
from models import CreateSavingsAccountRequest, CreateCurrentAccountRequest, DepositRequest, WithdrawRequest, TransferRequest, UpdateAccountRequest
from exceptions import InvalidAmountError, InsufficientFundsError
from database import SessionLocal
from db_models import SavingsAccountModel, CurrentAccountModel, UserModel
from routers import auth_router, user_router
from auth import get_current_user

app = FastAPI()
app.include_router(auth_router.router)
app.include_router(user_router.router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return{"message": "Banking API is running"}

@app.post("/accounts/savings")
def create_savings_account(request: CreateSavingsAccountRequest, db = Depends(get_db), current_user = Depends(get_current_user)):
    user = db.query(UserModel).filter(UserModel.email == current_user["sub"]).first()
    while True:
        account_number = str(randint(0, 99999999)).zfill(8)
        if not db.query(SavingsAccountModel).filter(SavingsAccountModel.account_number == account_number).first() and not db.query(CurrentAccountModel).filter(CurrentAccountModel.account_number == account_number).first():
            break
    account_model = SavingsAccountModel(account_holder=request.account_holder, account_number=account_number, balance=request.balance, email=user.email, phone_number=request.phone_number, interest_rate=request.interest_rate, interest_strategy=type(request.interest_strategy).__name__, user_id=user.id)
    db.add(account_model)
    db.commit()
    db.refresh(account_model)
    return account_model.to_entity().to_dict()

@app.post("/accounts/current")
def create_current_account(request: CreateCurrentAccountRequest, db = Depends(get_db), current_user = Depends(get_current_user)):
    user = db.query(UserModel).filter(UserModel.email == current_user["sub"]).first()
    while True:
        account_number = str(randint(0, 99999999)).zfill(8)
        if not db.query(SavingsAccountModel).filter(SavingsAccountModel.account_number == account_number).first() and not db.query(CurrentAccountModel).filter(CurrentAccountModel.account_number == account_number).first():
            break
    account = CurrentAccountModel(account_holder=request.account_holder, account_number=account_number, balance=request.balance, email=user.email, phone_number=request.phone_number, overdraft_limit=request.overdraft_limit, user_id=user.id)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account.to_entity().to_dict()

@app.get("/accounts")
def get_all_accounts(db = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user["role"] != "Admin":
        raise HTTPException(status_code=403, detail="Access denied")
    accounts = db.query(SavingsAccountModel).all() + db.query(CurrentAccountModel).all()
    return [account.to_entity().to_dict() for account in accounts]

@app.get("/accounts/{account_number}")
def get_account(account_number: str, db = Depends(get_db), current_user = Depends(get_current_user)):
    savings_account_model = db.query(SavingsAccountModel).filter(SavingsAccountModel.account_number == account_number).first()
    current_account_model = db.query(CurrentAccountModel).filter(CurrentAccountModel.account_number == account_number).first()
    if savings_account_model is not None:
        account_model = savings_account_model 
    elif current_account_model is not None:
        account_model = current_account_model
    else:
        raise HTTPException(status_code=404, detail="Account not found")
    user = db.query(UserModel).filter(UserModel.email == current_user["sub"]).first()
    if user.id == account_model.user_id or current_user["role"] == "Admin":
        return account_model.to_entity().to_dict()
    else:
        raise HTTPException(status_code=403, detail="Access denied")
    

@app.post("/accounts/{account_number}/deposit")
def deposit(request: DepositRequest, account_number: str, db = Depends(get_db)):
    savings_account_model = db.query(SavingsAccountModel).filter(SavingsAccountModel.account_number == account_number).first()
    current_account_model = db.query(CurrentAccountModel).filter(CurrentAccountModel.account_number == account_number).first()
    if savings_account_model is not None:
        account_object = savings_account_model.to_entity()
        account_model = savings_account_model
    elif current_account_model is not None:
        account_object = current_account_model.to_entity()
        account_model = current_account_model
    else:
        raise HTTPException(status_code=404, detail="Account not found")
    try:
        account_object.deposit(request.deposit_amount)
        account_model.balance = account_object.balance
    except InvalidAmountError:
        raise HTTPException(status_code=400, detail="Deposit amount must be greater than zero")
    db.commit()
    return {"message": f"{request.deposit_amount} Deposited successfully"}

@app.post("/accounts/{account_number}/withdraw")
def withdraw(request: WithdrawRequest, account_number: str, db = Depends(get_db), current_user = Depends(get_current_user)):
    savings_account_model = db.query(SavingsAccountModel).filter(SavingsAccountModel.account_number == account_number).first()
    current_account_model = db.query(CurrentAccountModel).filter(CurrentAccountModel.account_number == account_number).first()
    if savings_account_model is not None:
        account_object = savings_account_model.to_entity()
        account_model = savings_account_model
    elif current_account_model is not None:
        account_object = current_account_model.to_entity()
        account_model = current_account_model
    else:
        raise HTTPException(status_code=404, detail="Account not found")
    
    user = db.query(UserModel).filter(UserModel.email == current_user["sub"]).first()
    if user.id == account_model.user_id or current_user["role"] == "Admin":
        try:
            account_object.withdraw(request.withdraw_amount)
            account_model.balance = account_object.balance
        except InvalidAmountError:
            raise HTTPException(status_code=400, detail="Withdraw amount must be greater than zero")
        except InsufficientFundsError:
            raise HTTPException(status_code=400, detail="Withdraw amount must be less than or equal to balance")
    else:
        raise HTTPException(status_code=403, detail="Access denied")
    db.commit()
    return account_object.to_dict()

@app.post("/transfer")
def transfer(request: TransferRequest, db = Depends(get_db), current_user = Depends(get_current_user)):
    sender_savings_account_model = db.query(SavingsAccountModel).filter(SavingsAccountModel.account_number == request.sender_account_number).first()
    sender_current_account_model = db.query(CurrentAccountModel).filter(CurrentAccountModel.account_number == request.sender_account_number).first()

    receiver_savings_account_model = db.query(SavingsAccountModel).filter(SavingsAccountModel.account_number == request.receiver_account_number).first()
    receiver_current_account_model = db.query(CurrentAccountModel).filter(CurrentAccountModel.account_number == request.receiver_account_number).first()

    if sender_savings_account_model is not None:
        sender_account_object = sender_savings_account_model.to_entity()
        sender_account_model = sender_savings_account_model
    elif sender_current_account_model is not None:
        sender_account_object = sender_current_account_model.to_entity()
        sender_account_model = sender_current_account_model
    else:
        raise HTTPException(status_code=404, detail="Account not found")

    if receiver_savings_account_model is not None:
        receiver_account_object = receiver_savings_account_model.to_entity()
        receiver_account_model = receiver_savings_account_model
    elif receiver_current_account_model is not None:
        receiver_account_object = receiver_current_account_model.to_entity()
        receiver_account_model = receiver_current_account_model
    else:
        raise HTTPException(status_code=404, detail="Account not found")
    
    user = db.query(UserModel).filter(UserModel.email == current_user["sub"]).first()
    if user.id == sender_account_model.user_id or current_user["role"] == "Admin":
        try:
           sender_account_object.withdraw(request.transfer_amount)
           sender_account_model.balance = sender_account_object.balance
        except InvalidAmountError:
            raise HTTPException(status_code=400, detail="Withdraw amount must be greater than zero")
        except InsufficientFundsError:
            raise HTTPException(status_code=400, detail="Withdraw amount must be less than or equal to balance")
        receiver_account_object.deposit(request.transfer_amount)
        receiver_account_model.balance = receiver_account_object.balance
    else:
        raise HTTPException(status_code=403, detail="Access denied")
    db.commit()
    return sender_account_object.to_dict()

@app.put("/accounts/{account_number}")
def update_account(request: UpdateAccountRequest, account_number: str, db = Depends(get_db), current_user = Depends(get_current_user)):
    savings_account_model = db.query(SavingsAccountModel).filter(SavingsAccountModel.account_number == account_number).first()
    current_account_model = db.query(CurrentAccountModel).filter(CurrentAccountModel.account_number == account_number).first()

    if savings_account_model is not None:
        account_model = savings_account_model
    elif current_account_model is not None:
        account_model = current_account_model
    else:
        raise HTTPException(status_code=404, detail="Account not found")
    
    user = db.query(UserModel).filter(UserModel.email == current_user["sub"]).first()
    if user.id == account_model.user_id or current_user["role"] == "Admin":
        if request.account_holder is not None:
            account_model.account_holder = request.account_holder
        if request.phone_number is not None:
            account_model.phone_number = request.phone_number
    else:
        raise HTTPException(status_code=403, detail="Access denied")
    db.commit()
    db.refresh(account_model)
    return account_model.to_entity().to_dict()

@app.delete("/accounts/{account_number}")
def close_account(account_number: str, db = Depends(get_db), current_user = Depends(get_current_user)):
    savings_account_model = db.query(SavingsAccountModel).filter(SavingsAccountModel.account_number == account_number).first()
    current_account_model = db.query(CurrentAccountModel).filter(CurrentAccountModel.account_number == account_number).first()

    if savings_account_model is not None:
        account_model = savings_account_model
    elif current_account_model is not None:
        account_model = current_account_model
    else:
        raise HTTPException(status_code=404, detail="Account not found")
    
    user = db.query(UserModel).filter(UserModel.email == current_user["sub"]).first()
    if user.id == account_model.user_id or current_user["role"] == "Admin":
        db.delete(account_model)
    else:
        raise HTTPException(status_code=403, detail="Access denied")
    db.commit()
    return {"message": "Account closed successfully"}