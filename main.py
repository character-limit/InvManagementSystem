import csv, os
from datetime import datetime
from item import Item
from user import User

print("hello")

def main():
    """ items = Item.load_items()

    for i in items:
        print(i)


    temp = Item("testname", 40, "sotragename", "0005", datetime.now().strftime("%d/%m/%Y %H:%M"))

    items.append(temp)

    Item.write_items(items)

    for i in items:
        print(i)


    User.load_users()

    print(User.users)

    User.create_user(
        input ("first Name: "),
        input ("last Name: "),
        input ("user Name: "),
        input ("password: ")
    )

    print("yes")

    print("LOGIN")

    username = input("username: ")
    password = input("password: ")

    User.login(username, password) """

def title_page():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== Inventory Management System ===")
    print("1: Login")
    print("2: Create Account")
    print("3: Exit")
    choice = input("Select an option: ")

    if choice == "1":
        login_page()
    elif choice == "2":
        create_user_page()
    elif choice == "3":
        exit()
    else:
        title_page()

def login_page():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== Login ===")
    username = input("Username: ")
    password = input("Password: ")

    

    if User.login(username, password) == 1:
        menu_page()
    elif 2:
        print("Incorrect password. Please try again.")
        input("Press Enter to continue...")
        login_page()
    elif 3:
        print("Username not found. Please try again.")
        input("Press Enter to continue...")
        login_page()

def create_user_page(): ##ADD VALIDATION!!
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== Create Account ===")
    firstName = input("First Name: ")
    lastName = input("Last Name: ")
    username = input("Username: ")
    password = input("Password: ")

    User.create_user(firstName, lastName, username, password)
    title_page()


if __name__ == "__main__":
    title_page()
