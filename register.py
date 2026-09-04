import sqlite3
import bcrypt

DB_NAME = "users.db"


def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    with get_connection() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTs users (
                        username text PRIMARY KEY NOT NULL,
                        password BLOB NOT NULL,
                        email text NOT NULL,
                        name text NOT NULL,
                        lastname text NOT NULL
                        )
                        """)


def register_user(username, password, email, name, lastname):
    if not username.strip() or not password or not email:
        print("Username, password and email cannot be empty")
        return

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            print("User already exists")
            return
        cursor.execute("select * from users WHERE email = ?", (email,))
        if cursor.fetchone():
            print("This Email is already in use")
            return

        cursor.execute("INSERT INTO users (username, password, email, name, lastname) VALUES (?, ?, ?, ?, ?)",
                       (username, hashed, email, name, lastname))
        print("User created successfully")

def user_find(user):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (user,))
        row = cursor.fetchone()
    if row is not None:
        print(f"""We Found the user:
                Username: {row[0]}
                Email: {row[2]}
                Full Name: {row[4]}, {row[3]}""")
    else:
        print("User not found")

def login_check(username, password):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()

    if row is None:
        print("User not found")
    elif bcrypt.checkpw(password.encode(), row[0]):
        print("Login successful")
    else:
        print("Incorrect Password")




itson = True

while itson:
    init_db()
    print("""
    1.- Register a new user
    2.- Search for an existing user
    3.- Login to your account
    4.- Exit Program
    """)

    try:
        option = int(input("Select an option:"))
        if option == 1:
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            email = input("Enter your email: ")
            name = input("Enter your name: ")
            lastname = input("Enter your last name: ")
            register_user(username, password, email, name, lastname)
        elif option == 2:
            user = input("Enter your username to look up: ")
            user_find(user)
        elif option == 3:
            user = input("Enter your username: ")
            password = input("Enter your password: ")
            login_check(user, password)
        elif option == 4:
            print("Exiting Program")
            itson = False
            with get_connection() as conn:
                conn.close()
        else: print("Please enter an option from the list above")
    except ValueError:
        print("Please enter an option from the list above")






