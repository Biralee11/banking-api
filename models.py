from pydantic import BaseModel, field_validator
from typing import Optional
import re
from strategies import SimpleInterestStrategy, CompoundInterestStrategy

class BaseAccountRequest(BaseModel):
    account_holder: str
    phone_number: str

    @field_validator("account_holder")
    @classmethod
    def validate_account_holder(cls, value):
        if re.search(r"^[a-zA-Z]+( [a-zA-Z]+)+$", value):
            return value
        else:
            raise ValueError("Invalid Name")
        
    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value):
        if re.search(r"^07\d{9}$", value):
            return value
        else:
            raise ValueError("Invalid Phone Number")

class CreateSavingsAccountRequest(BaseAccountRequest):
    balance: float
    interest_rate: float
    interest_strategy: str

    @field_validator("interest_rate")
    @classmethod
    def validate_interest_rate(cls, value):
        if value > 0:
            return value
        else:
            raise ValueError("Invalid Interest Rate")

    @field_validator("interest_strategy")
    @classmethod
    def validate_interest_strategy(cls, value):
        if value.lower() == "simple":
            return SimpleInterestStrategy()
        elif value.lower() == "compound":
            return CompoundInterestStrategy()
        else:
            raise ValueError("Invalid Interest strategy")

class CreateCurrentAccountRequest(BaseAccountRequest):
    balance: float
    overdraft_limit: float

    @field_validator("overdraft_limit")
    @classmethod
    def validate_overdraft_limit(cls, value):
        if value > 0:
            return value
        else:
            raise ValueError("Invalid Overdraft Limit")

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
    phone_number: Optional[str] = None

    @field_validator("account_holder")
    @classmethod
    def validate_account_holder(cls, value):
        if value is None:
            return None
        elif re.search(r"^[a-zA-Z]+( [a-zA-Z]+)+$", value):
            return value
        else:
            raise ValueError("Invalid Name")
        
    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value):
        if value is None:
            return None
        elif re.search(r"^07\d{9}$", value):
            return value
        else:
            raise ValueError("Invalid Phone Number")
        
class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, value):
        if re.search(r"^[a-zA-Z][a-zA-Z0-9]{5,7}$", value):
            return value
        else:
            raise ValueError("Invalid Username")
        
    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        if re.search(r"^[\w.]+@\w+(\.\w+)+$", value):
            return value
        else:
            raise ValueError("Invalid Email")
        
    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[^a-zA-Z0-9]", value):
            raise ValueError("Password must contain at least one special character")        
        if re.search(r"^[a-zA-Z].{7,11}$", value):
            return value
        else:
            raise ValueError("Invalid Password")

class LoginRequest(BaseModel):
    email: str
    password: str

class UpdateEmailRequest(BaseModel):
    email: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        if re.search(r"^[\w.]+@\w+(\.\w+)+$", value):
            return value
        else:
            raise ValueError("Invalid Email")

class UpdatePasswordRequest(BaseModel):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[^a-zA-Z0-9]", value):
            raise ValueError("Password must contain at least one special character")        
        if re.search(r"^[a-zA-Z].{7,11}$", value):
            return value
        else:
            raise ValueError("Invalid Password")