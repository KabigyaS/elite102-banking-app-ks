import sqlite3

# Connect to a database file (creates it if it does not exist)
conn = sqlite3.connect('banking_app.db')
cursor = conn.cursor()

# Create a table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY,
        name TEXT,
        balance REAL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id INTEGER,
        type TEXT,
        amount REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (account_id) REFERENCES accounts(id)
    )
''')



# FUNCTIONS
def create(name, amount):
    cursor.execute("SELECT id FROM accounts WHERE name = ?", (name,))
    existing = cursor.fetchone()

    if existing:
        print("Error: Account name already exists.")
        return None
    
    cursor.execute(
            "INSERT INTO accounts (name, balance) VALUES (?, ?)", (name, amount)
        )
    conn.commit()
    current_id = cursor.lastrowid
    print(f"Account created for {name} (ID: {current_id}) with balance ${amount:.2f}")
    return current_id

def check_balance(current_id):
    cursor.execute("SELECT balance FROM accounts where id = ?",(current_id,))  
    result = cursor.fetchone()

    if result:
        balance = result[0]
        print("Your Balance is", balance)
        return balance
    else:
        print("Account not found.")
        return None

def deposit(current_id, amount):
    if amount <= 0:
        print("Error: Deposit amount must be positive.")
        return
    cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, current_id))
    cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (?, 'deposit', ?)", (current_id, amount))
    conn.commit()
    print(f"Deposited ${amount:.2f}. New balance: ${check_balance(current_id):.2f}")

    

def withdraw(current_id, amount):
    if amount <= 0:
        print("Error: Deposit amount must be positive.")
        return
    balance = check_balance(current_id)
    if amount > balance:
        print(f"Not Enough Balance. Balance: ${balance:.2f}, Requested: ${amount:.2f}")
        return
    cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, current_id))
    cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (?, 'WithDraw', ?)", (current_id, amount))
    conn.commit()
    print(f"Withdrawed ${amount:.2f}. New balance: ${check_balance(current_id):.2f}")

def check_transactions(current_id):
    cursor.execute("SELECT * FROM transactions WHERE account_id= ?", (current_id,))
    rows = cursor.fetchall()

    if not rows:
        print("No accounts found or transactions found.")
    else:
        for row in rows:
            print(row)

def list_accounts():
    cursor.execute("SELECT name FROM accounts")
    rows = cursor.fetchall()

    if not rows:
        print("No accounts found.")
    else:
        for row in rows:
            print(f"Accounts: {row[0]}")



print("\n=== Welcome to the Banking System ===")
current_id = None
name = None

while True:
    print("\n0. Login")
    print("1. Create Account")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Check Balance")
    print("5. Check Transactions")
    print("6. List Accounts")
    print("7. Exit")


    try:
        option = int(input("Choose option: "))
        if option == 0:
            name = input("Enter name: ")

            cursor.execute("SELECT id FROM accounts WHERE name = ?", (name,))
            result = cursor.fetchone()

            if result:
                current_id = result[0]
                print(f"Logged in as {name} (ID: {current_id})")
            else:
                print("Account not found.")
                current_id = None

        elif option == 1:
            name = input("Enter new account name: ")
            amount = float(input("Initial deposit: "))
            current_id = create(name, amount)
            

        elif option == 2:
            if current_id == None:
                print("Create a Account or Account not found")
                continue
            amount = float(input("Deposit amount: "))
            deposit(current_id, amount)

        elif option == 3:
            if current_id == None:
                print("Create a Account or Account not found")
                continue
            amount = float(input("Withdraw amount: "))
            withdraw(current_id, amount)

        elif option == 4:
            if current_id == None:
                print("Create a Account or Account not found")
                continue
            check_balance(current_id)

        elif option == 5:
            if current_id == None:
                print("Create a Account or Account not found")
                continue
            check_transactions(current_id)

        elif option == 7:
            print("Goodbye!")
            break

        elif option == 6:
            list_accounts()
    
        else:
            print("Invalid option.")

    except ValueError:
        print("Invalid input.")


# Always close when done
conn.close()