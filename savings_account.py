from bank_account import BankAccount
from strategies import SimpleInterestStrategy, CompoundInterestStrategy

class SavingsAccount(BankAccount):
    account_type = "savings"
    def __init__(self, account_holder, account_number, balance, email, phone_number, interest_rate, interest_strategy):
        super().__init__(account_holder, account_number, balance, email, phone_number)
        self.interest_rate = interest_rate
        self.interest_strategy = interest_strategy

    def __str__(self):
        return f"Account Holder: {self.account_holder}\nAccount Number: {self.account_number}\nBalance: £{self.balance}\nEmail: {self.email}\nPhone Number: {self.phone_number}\nInterest Rate: {self.interest_rate * 100}%\nInterest Strategy: {type(self.interest_strategy).__name__}\nAccount Type: {self.account_type}"
    
    def to_dict(self):
        return {"account_holder": self.account_holder, "account_number": self.account_number, "balance": self.balance, "email": self.email, "phone_number": self.phone_number, "interest_rate": self.interest_rate, "interest_strategy": type(self.interest_strategy).__name__, "account_type": self.account_type}

    @classmethod
    def from_dict(cls, dict_account):
        account_holder = dict_account["account_holder"]
        account_number = dict_account["account_number"]
        balance = dict_account["balance"]
        email = dict_account["email"]
        phone_number = dict_account["phone_number"]
        interest_rate = dict_account["interest_rate"]
        if dict_account["interest_strategy"] == "SimpleInterestStrategy":
            interest_strategy = SimpleInterestStrategy()
        elif dict_account["interest_strategy"] == "CompoundInterestStrategy":
            interest_strategy = CompoundInterestStrategy()
        return cls(account_holder, account_number, balance, email, phone_number, interest_rate, interest_strategy)
    
    def apply_interest(self, periods=1):
        self.balance = self.interest_strategy.calculate(self.balance, self.interest_rate, periods)