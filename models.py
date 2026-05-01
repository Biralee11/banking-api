from pydantic import BaseModel
from typing import Optional

class CreateSavingsAccountRequest(BaseModel):
    account_holder: str
    balance: float
    email: str
    phone_number: str
    interest_rate: float
    interest_strategy: str

class CreateCurrentAccountRequest(BaseModel):
    account_holder: str
    balance: float
    email: str
    phone_number: str
    overdraft_limit: float

class DepositRequest(BaseModel):
    deposit_amount: float

class WithdrawRequest(BaseModel):
    withdraw_amount: float

class TransferRequest(BaseModel):
    sender_account_number: str
    receiver_account_number: str
    transfer_amount: float

class UpdateAccountRequest(BaseModel):
    account_holder: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None