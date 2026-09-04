import sqlite3


connection = sqlite3.connect("users.db")
cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTs users (
                        username text PRIMARY KEY NOT NULL,
                        password text NOT NULL,
                        email text NOT NULL,
                        name text NOT NULL,
                        lastname text NOT NULL
                        )
                        """)


def register_user(connection, username, password, email, name, lastname):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    namecheck = cursor.fetchone()

    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    emailcheck = cursor.fetchone()

    if namecheck is not None:
        print("User already exists")
    elif emailcheck is not None:
        print("This Email is already in use")
    else:
        query = "INSERT INTO users (username, password, email, name, lastname) VALUES (?, ?, ?, ?, ?)"
        try:
            with connection:
                connection.execute(query, (username, password, email, name, lastname))
        except Exception as e:
            print(e)

def user_find(connection, user):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (user,))
    userinfo = cursor.fetchone()
    if userinfo is not None:
        print(f"""We Found the user:
                Username: {userinfo[0]}
                Email: {userinfo[2]}
                Full Name: {userinfo[4]}, {userinfo[3]}""")
    else:
        print("User not found")

def login_check(connection, user, password):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (user,))
    usernamecheck = cursor.fetchone()
    if usernamecheck is None:
        print("User not found")
    else:
        if password == usernamecheck[1]:
            print("Login successful")
            print(usernamecheck)
        else:
            print("Incorrect Password")
            print(usernamecheck)



itson = True

while itson:
    print("""
    1.- Register a new user
    2.- Search for an existing user
    3.- Login to your account
    4.- Exit Program
    """)

    option = int(input("Select an option:"))
    if option == 1:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        email = input("Enter your email: ")
        name = input("Enter your name: ")
        lastname = input("Enter your last name: ")
        register_user(connection, username, password, email, name, lastname)
    elif option == 2:
        user = input("Enter your username to look up: ")
        user_find(connection, user)
    elif option == 3:
        user = input("Enter your username: ")
        password = input("Enter your password: ")
        login_check(connection, user, password)
    elif option == 4:
        print("Exiting Program")
        itson = False
        connection.close()
    else: print("Please enter an option from the list above")





