# A program that models a bank account, with classes for the account, the customer,and the bank.

class Account:
    def __init__(self, account_number, balance=0):
        self.account_number = account_number
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount #self.balance = self.balance + amount
            print(f"Deposited: {amount}. New balance: {self.balance}")
        else:
            print("Invalid deposit amount.")

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f"Withdrawn: {amount}. New balance: {self.balance}")
        else:
            print("Invalid withdrawal amount or insufficient funds.")

    def get_balance(self):
        return self.balance


class Customer:
    def __init__(self, name, customer_id):
        self.name = name
        self.customer_id = customer_id
        self.accounts = []

    def add_account(self, account):
        self.accounts.append(account)
        print(
            f"Account {account.account_number} added for customer {self.name}.")

    def list_accounts(self):
        for account in self.accounts:
            print(
                f"Account Number: {account.account_number}, Balance: {account.balance}")


class Bank:
    def __init__(self, name):
        self.name = name
        self.customers = []

    def add_customer(self, customer):
        self.customers.append(customer)
        print(f"Customer {customer.name} added to {self.name}.")

    def list_customers(self):
        print(f"Customers of {self.name}:")
        for customer in self.customers:
            print(
                f"Name: {customer.name}, Customer ID: {customer.customer_id}")

# Create a bank
my_bank = Bank("My Bank")

# Create customers
customer1 = Customer("Alice", "C001")
customer2 = Customer("Bob", "C002")

# Add customers to the bank
my_bank.add_customer(customer1)
my_bank.add_customer(customer2)

# Create accounts for the customers
account1 = Account("A101", 1000)
account2 = Account("A102", 500)

# Add accounts to customers
customer1.add_account(account1)
customer2.add_account(account2)

# Perform operations
print("\n-- Banking Operations --")
account1.deposit(200)  # Deposit to Alice's account
account1.withdraw(300)  # Withdraw from Alice's account
print(f"Alice's account balance: {account1.get_balance()}")
account2.deposit(100)  # Deposit to Bob's account
account2.withdraw(700)  # Attempt to withdraw more than balance
# List customers and accounts
print("\n-- Bank Details --")
my_bank.list_customers()
print("\n-- Customer Accounts --")
customer1.list_accounts()
customer2.list_accounts()
