# Descriptor that controls read, write and delete access to the balance attribute.
# Used as a class attribute on BankAccount to intercept attribute access via __get__, __set__ and __delete__.
# Stores the actual value in obj._balance to separate the descriptor logic from the raw data.
class BalanceDescriptor():
    def __get__(self, obj, objtype):
        return obj._balance

    def __set__(self, obj, value):
        if not isinstance(value, (int, float)):
            print("Balance must be a number.")
            return
        if value >= 0:
            obj._balance = value
        else:
            print("Balance cannot be less than zero.")

    def __delete__(self, obj):
        print("Balance cannot be deleted")

# Overrides BalanceDescriptor behaviour for current accounts to allow negative balances within the overdraft limit.
# Reads the overdraft limit directly from the account instance via obj.overdraft_limit.
class CurrentAccountBalanceDescriptor():
    def __get__(self, obj, objtype):
        return obj._balance
    
    def __set__(self, obj, value):
        if not isinstance(value, (int, float)):
            print("Balance must be a number.")
            return
        if value >= (-obj.overdraft_limit):
            obj._balance = value
        else:
            print("Balance cannot be less than overdraft limit.")

    def __delete__(self, obj):
        print("Balance cannot be deleted")