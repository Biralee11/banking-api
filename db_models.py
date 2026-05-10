from database import Base
from sqlalchemy import Column, String, Float, Integer, ForeignKey
from savings_account import SavingsAccount
from current_account import CurrentAccount
from strategies import SimpleInterestStrategy, CompoundInterestStrategy

class SavingsAccountModel(Base):
    __tablename__ = "savings_accounts"
    account_holder = Column(String, nullable=False) 
    account_number = Column(String, primary_key=True)
    balance = Column(Float, nullable=False)
    email = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    interest_rate = Column(Float, nullable=False)
    interest_strategy = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    def to_entity(self):
        if self.interest_strategy == "SimpleInterestStrategy":
            interest_strategy = SimpleInterestStrategy()
        elif self.interest_strategy == "CompoundInterestStrategy":
            interest_strategy = CompoundInterestStrategy()
        return SavingsAccount(self.account_holder, self.account_number, self.balance, self.email, self.phone_number, self.interest_rate, interest_strategy)

class CurrentAccountModel(Base):
    __tablename__ = "current_accounts"
    account_holder = Column(String, nullable=False) 
    account_number = Column(String, primary_key=True)
    balance = Column(Float, nullable=False)
    email = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    overdraft_limit = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    def to_entity(self):
        return CurrentAccount(self.account_holder, self.account_number, self.balance, self.email, self.phone_number, self.overdraft_limit)

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)