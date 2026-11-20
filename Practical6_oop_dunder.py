"""
Practical 6: OOP Design & Dunder Methods
Course: MCA Semester I - Python & Relational Programming (Unit II / CO2)
Student: Sahil Surendra Shirke

================================================================================
CLASS DESIGN NOTES
================================================================================
1. BankAccount Class:
   - Fields:
       * holder (str): Account holder's full name (must be non-empty).
       * account_number (str): Unique account identifier.
       * _balance (float): Encapsulated internal balance (single leading underscore
         signals internal use; exposed safely via read-only @property `balance`
         and `get_balance()`).
   - Public Methods:
       * deposit(amount), withdraw(amount), get_balance(), transfer_to(other, amount)
       * Dunder methods: __init__, __str__, __repr__, __add__
   - Validation Rules:
       * Account holder name cannot be blank/whitespace.
       * Opening balance cannot be negative.
       * Deposit, withdrawal, and transfer amounts must be strictly positive (> 0).
       * Withdrawals and transfers cannot exceed the current available balance.
       * Direct assignment to `account.balance` raises AttributeError (read-only property).
   - Why Operator Overload (__add__) is Appropriate:
       * Overloading `+` (`account1 + account2`) returns a float representing the
         combined liquidity of two accounts without mutating either object or
         fabricating a synthetic account number/holder identity.

2. Extension Task 4 Explanation (Why `account1 + account2` must not mutate accounts):
   - In Python, the `+` operator represents a pure binary expression (like `a + b`),
     not an in-place state mutation (which belongs to `+=`). Silently transferring
     or altering balances during `account1 + account2` would violate user expectations,
     create accounting discrepancies, and break referential transparency when
     evaluating combined totals.
================================================================================
"""


class BankAccount:
    """Represents an encapsulated bank account with validated transactions and dunder methods."""

    def __init__(self, holder, account_number, opening_balance=0.0):
        if not holder or not str(holder).strip():
            raise ValueError("Account holder cannot be blank")
        if opening_balance < 0:
            raise ValueError("Opening balance cannot be negative")

        self.holder = str(holder).strip()
        self.account_number = str(account_number).strip()
        self._balance = float(opening_balance)

    # Extension Task 2: Read-only property preventing direct assignment
    @property
    def balance(self):
        """Read-only access to the encapsulated account balance."""
        return self._balance

    def get_balance(self):
        """Explicit getter method for the account balance."""
        return self._balance

    def deposit(self, amount):
        """Adds a positive amount to the account balance."""
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self._balance += float(amount)

    def withdraw(self, amount):
        """Deducts a positive amount if sufficient funds exist."""
        if amount <= 0:
            raise ValueError("Withdrawal must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= float(amount)

    # Extension Task 1: Safe inter-account transfer
    def transfer_to(self, other_account, amount):
        """Validates and transfers funds atomically to another BankAccount."""
        if not isinstance(other_account, BankAccount):
            raise TypeError("Target must be a BankAccount instance")
        if other_account is self:
            raise ValueError("Cannot transfer to the same account")
        # Withdraw validates amount > 0 and sufficient balance before depositing
        self.withdraw(amount)
        other_account.deposit(amount)

    def __str__(self):
        """Human-readable display for end users."""
        return f"BankAccount({self.holder}, balance={self._balance:.2f})"

    def __repr__(self):
        """Unambiguous developer-oriented representation."""
        return (
            f"BankAccount(holder={self.holder!r}, "
            f"account_number={self.account_number!r}, "
            f"opening_balance={self._balance!r})"
        )

    def __add__(self, other):
        """Returns the combined balance of two BankAccount objects without mutation."""
        if not isinstance(other, BankAccount):
            return NotImplemented
        return self._balance + other._balance


# Extension Task 3: Student class applying the same OOP & dunder principles
class Student:
    """Represents an MCA student with encapsulated marks and readable/developer representations."""

    def __init__(self, name, roll_number, marks):
        if not name or not str(name).strip():
            raise ValueError("Student name cannot be blank")
        if not (0 <= marks <= 100):
            raise ValueError("Marks must be between 0 and 100")

        self.name = str(name).strip()
        self.roll_number = str(roll_number).strip()
        self._marks = float(marks)

    @property
    def marks(self):
        return self._marks

    def __str__(self):
        return f"Student: {self.name} (Roll No: {self.roll_number}) - Marks: {self._marks:.1f}/100"

    def __repr__(self):
        return (
            f"Student(name={self.name!r}, "
            f"roll_number={self.roll_number!r}, "
            f"marks={self._marks!r})"
        )


def main():
    print("=== 1. Account Creation & Normal Transactions ===")
    account1 = BankAccount("Asha", "BA101", 1500)
    account2 = BankAccount("Kabir", "BA102", 500)
    print(f"Initial Account 1: {account1}")
    print(f"Initial Account 2: {account2}")

    account1.deposit(250)
    print(f"After depositing 250 to Asha: {account1.get_balance()}")

    account2.withdraw(100)
    print(f"After withdrawing 100 from Kabir: {account2.get_balance()}")

    print("\n=== 2. __str__, __repr__, and Operator Overload (+) ===")
    print("print(account1) ->", account1)
    print("repr(account1)  ->", repr(account1))
    print("account1 + account2 (combined balance) ->", account1 + account2)

    print("\n=== 3. Extension 1: Validated Transfer Between Accounts ===")
    account1.transfer_to(account2, 300)
    print(f"After transferring 300 from Asha to Kabir:")
    print(" ", account1)
    print(" ", account2)

    print("\n=== 4. Invalid Operations & Encapsulation Checks ===")
    # Invalid operation 1: Overdraft withdrawal
    try:
        account2.withdraw(5000)
    except ValueError as err:
        print(f"Caught expected error (overdraft): {err}")

    # Invalid operation 2: Non-positive deposit
    try:
        account1.deposit(-50)
    except ValueError as err:
        print(f"Caught expected error (negative deposit): {err}")

    # Extension 2 check: Direct balance mutation blocked by read-only @property
    try:
        account1.balance = 999999
    except AttributeError as err:
        print(f"Caught expected encapsulation error (direct assignment): {err}")

    print("\n=== 5. Extension 3: Student Class (__str__ & __repr__) ===")
    student = Student("Sahil Surendra Shirke", "MCA-2026-09", 88.5)
    print("print(student) ->", student)
    print("repr(student)  ->", repr(student))


if __name__ == "__main__":
    main()
