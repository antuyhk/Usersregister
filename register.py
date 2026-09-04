import sqlite3


connection = sqlite3.connect("users.db")
cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTs users (
                        username PRIMARY KEY NOT NULL,
                        password text NOT NULL,
                        email text NOT NULL,
                        name text NOT NULL,
                        lastname text NOT NULL
                        )
                        """)
connection.commit()
connection.close()

def register_user(connection, username, password, email, name, lastname):
    query = "INSERT INTO users (username, password, email, name, lastname) VALUES (?, ?, ?, ?, ?)"
    try:
        with connection:
            connection.execute(query, (username, password, email, name, lastname))
    except Exception as e:
        print(e)

itson = True

while itson:
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
            register_user(connection, username, password, email, name, lastname)
        elif option == 4:
            print("Exiting Program")
            itson = False
        else: print("Please enter an option from the list above")

    except:
        print("This is not a valid option")




