from abc import ABCMeta, abstractmethod
from typing import Optional
from descriptors import BalanceDescriptor
from mixins import LogMixin


# Metaclass that enforces all account classes must define a 'currency' class attribute.
# Inherits from ABCMeta to remain compatible with Python's Abstract Base Class system.
# __new__ intercepts class creation and raises an error if 'currency' is missing on the base class.
class AccountMeta(ABCMeta):
    def __new__(cls, name, bases, dct):
        if bases == () and "currency" not in dct:
            raise AttributeError('missing attribute "currency"')      
        return super().__new__(cls, name, bases, dct)

class BankAccount(LogMixin, metaclass=AccountMeta):
    currency = "GBP"
    balance = BalanceDescriptor()
    def __init__(self, account_holder, account_number, balance, email, phone_number):
        self.account_holder = account_holder
        self.account_number = account_number
        self._balance = balance
        self.email = email
        self.phone_number = phone_number
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self, message):
        for observer in self.observers:
            observer.update(message)
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def to_dict(self):
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, dict_account):
        pass

    def deposit(self, amount: float) -> Optional[bool]:
        if amount <= 0:
            return False
        else:
            self.balance = self.balance + amount
            self.notify_observers(f"Deposit of £{amount} made, balance is now £{self.balance}")
            return True
    
    def withdraw(self, amount: float) -> Optional[bool]:
        if amount > self.balance:
            return False
        elif amount <= 0:
            return False
        else:
            self.balance = self.balance - amount
            self.notify_observers(f"Withdrawal of £{amount} made, balance is now £{self.balance}")
            return True