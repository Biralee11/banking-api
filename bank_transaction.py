class BankTransaction:
    def __init__(self, account, transaction_type):# transaction_type takes a string e.g deposit, withdraw, e.t.c
        self.account = account
        self.transaction_type = transaction_type
    def __enter__(self):
        print(f"Opening transaction - {self.transaction_type} for {self.account.account_holder}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):      
        print(f"Closing transaction - {self.transaction_type} for {self.account.account_holder}")