# MCA Semester I - Practical 6: OOP Design & Dunder Methods
**Course:** Python & Relational Programming (Unit II / CO2)  
**Student:** Sahil Surendra Shirke  

## Class Design Summary (`BankAccount`)
- **Encapsulated State:** `holder`, `account_number`, and `_balance` (protected behind a read-only `@property` `balance` and `get_balance()`).
- **Validated Methods:** `deposit(amount)`, `withdraw(amount)`, and `transfer_to(other_account, amount)` enforce positive amounts, non-blank holder names, and sufficient funds before mutating state.
- **Dunder Methods:** `__init__`, `__str__`, `__repr__`, and `__add__`.

## Extension Task 4: Why `account1 + account2` Must Not Mutate Accounts
The binary `+` operator in Python evaluates an expression and returns a new value without side effects (unlike `+=`). Silently modifying either account's `_balance` during addition would cause unintended financial state changes and violate referential transparency.

## Oral Justification (Viva Reference)
1. **Why overload `+` this way?**
   - Returning `self._balance + other._balance` (a `float`) gives `account1 + account2` an unambiguous meaning (total combined balance) without inventing a fake account number or guessing which holder owns a merged `BankAccount` object.
2. **Difference between `__str__` and `__repr__`:**
   - `__str__` is designed for **end users** (`print(obj)`), prioritizing clean readability (`BankAccount(Asha, balance=1450.00)`).
   - `__repr__` is designed for **developers and debugging** (`repr(obj)`), providing an unambiguous string that ideally resembles valid Python constructor syntax (`BankAccount(holder='Asha', account_number='BA101', opening_balance=1450.0)`).
