import sqlite3
import hashlib

# This is the users' database management module
# Uncomment lines at the bottom of this file to edit the users' database.

conn = sqlite3.connect("../data/users.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
''')

conn.commit()

def hash_password(password):
    """Hashes the password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, password):
    """Adds a new user with a hashed password to the database."""
    try:
        password_hash = hash_password(password)
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        conn.commit()
        print("User added successfully!")
    except sqlite3.IntegrityError:
        print("Error: Username already exists.")

def print_users():
    """Prints all users in the database."""
    for row in cursor.execute("SELECT * FROM users"):
        print(row)

def remove_user(username):
    """Removes a user from the database."""
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    print("User removed successfully!")

# uncomment lines below & modify parameters & run the program to edit users

# add_user("admin", "admin")
# remove_user("admin")
# print_users()

conn.close()
