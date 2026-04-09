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

# Insert data
cursor.execute("INSERT INTO accounts VALUES (1, 'Maria', 500.00)")
conn.commit()   # IMPORTANT: saves your changes!

# Query data
cursor.execute("SELECT * FROM accounts")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Always close when done
conn.close()