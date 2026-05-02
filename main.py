from fastapi import FastAPI, HTTPException
from savings_account import SavingsAccount
from current_account import CurrentAccount
from random import randint
from models import CreateSavingsAccountRequest, CreateCurrentAccountRequest, DepositRequest, WithdrawRequest, TransferRequest, UpdateAccountRequest
from strategies import SimpleInterestStrategy, CompoundInterestStrategy
from exceptions import InvalidAmountError, InsufficientFundsError

app = FastAPI()

accounts = []

@app.get("/")
def root():
    return{"message": "Banking API is running"}

@app.post("/accounts/savings")
def create_savings_account(request: CreateSavingsAccountRequest): 
    while True:
        account_number = str(randint(0, 99999999)).zfill(8)
        if account_number not in [account.account_number for account in accounts]:
            break
    if request.interest_strategy == "SimpleInterestStrategy":
        interest_strategy = SimpleInterestStrategy()
    elif request.interest_strategy == "CompoundInterestStrategy":
        interest_strategy = CompoundInterestStrategy()
    account = SavingsAccount(request.account_holder, account_number, request.balance, request.email, request.phone_number, request.interest_rate, interest_strategy)
    accounts.append(account)
    return account.to_dict()

@app.post("/accounts/current")
def create_current_account(request: CreateCurrentAccountRequest):  
    while True:
        account_number = str(randint(0, 99999999)).zfill(8)
        if account_number not in [account.account_number for account in accounts]:
            break
    account = CurrentAccount(request.account_holder, account_number, request.balance, request.email, request.phone_number, request.overdraft_limit)
    accounts.append(account)
    return account.to_dict()

@app.get("/accounts")
def get_all_accounts():
    return [account.to_dict() for account in accounts]

@app.get("/accounts/{account_number}")
def get_account(account_number: str):
    for account in accounts:
        if account_number == account.account_number:
            return account.to_dict()
    raise HTTPException(status_code=404, detail="Account not found")

@app.post("/accounts/{account_number}/deposit")
def deposit(request: DepositRequest, account_number: str):
    for account in accounts:
        if account_number == account.account_number:
            try:
                account.deposit(request.deposit_amount)
            except InvalidAmountError:
                raise HTTPException(status_code=400, detail="Deposit amount must be greater than zero")
            return account.to_dict()
    raise HTTPException(status_code=404, detail="Account not found")

@app.post("/accounts/{account_number}/withdraw")
def withdraw(request: WithdrawRequest, account_number: str):
    for account in accounts:
        if account_number == account.account_number:
            try:
                account.withdraw(request.withdraw_amount)
            except InvalidAmountError:
                raise HTTPException(status_code=400, detail="Withdraw amount must be greater than zero")
            except InsufficientFundsError:
                raise HTTPException(status_code=400, detail="Withdraw amount must be less than or equal to balance")
            return account.to_dict()
    raise HTTPException(status_code=404, detail="Account not found")

@app.post("/transfer")
def transfer(request: TransferRequest):
    sender_account_found = False
    receiver_account_found = False
    for account in accounts:
        if request.sender_account_number == account.account_number:
            sender_account_found = True
            sender_account = account
        elif request.receiver_account_number == account.account_number:
            receiver_account_found = True
            receiver_account = account
    if sender_account_found == True and receiver_account_found == True:
        try:
           sender_account.withdraw(request.transfer_amount)
        except InvalidAmountError:
            raise HTTPException(status_code=400, detail="Withdraw amount must be greater than zero")
        except InsufficientFundsError:
            raise HTTPException(status_code=400, detail="Withdraw amount must be less than or equal to balance")
        receiver_account.deposit(request.transfer_amount)
        return sender_account.to_dict()
    else:
        raise HTTPException(status_code=404, detail="Account not found")

@app.put("/accounts/{account_number}")
def update_account(request: UpdateAccountRequest, account_number: str):
    for account in accounts:
        if account_number == account.account_number:
            if request.account_holder is not None:
                account.account_holder = request.account_holder
            if request.email is not None:
                account.email = request.email
            if request.phone_number is not None:
                account.phone_number = request.phone_number
            return account.to_dict()
    raise HTTPException(status_code=404, detail="Account not found")

@app.delete("/accounts/{account_number}")
def close_account(account_number: str):
    for account in accounts:
        if account_number == account.account_number:
           accounts.remove(account)
           return {"message": "Account closed successfully"}
    raise HTTPException(status_code=404, detail="Account not found")



#uvicorn main:app --reload
"""
{
  "account_holder": "Kcee Michael",
  "balance": 1400,
  "email": "kcee.michael@gmail.com",
  "phone_number": "07345789092",
  "interest_rate": 0.05,
  "interest_strategy": "SimpleInterestStrategy"
}
"""

"""
{
  "account_holder": "Fred Collins",
  "balance": 1500,
  "email": "fred.collins@gmail.com",
  "phone_number": "07325454582",
  "interest_rate": 0.05,
  "interest_strategy": "SimpleInterestStrategy"
}
"""