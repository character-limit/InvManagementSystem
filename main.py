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

    

    if User.login(username, password) == True:
        menu_page()
    else:
        print("Incorrect login. Please try again.")
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

def menu_page():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"=== Main Menu ({User.current.username}) ===")
    print("1: View Inventory")
    print("2: Logout")
    choice = input("Select an option: ")

    if choice == "1":
        inventory_page()
    elif choice == "2":
        User.current = None #log out
        title_page()
    else:
        menu_page()

def inventory_page():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== Inventory ===\n\n")
    items = Item.load_items()

    # display in table.

    print(f'{"Name":<40} {"Quantity":<15} {"Location":<25} {"Last Modified By":<25} {"Last Modified ":<25}')
    print("-"*130)
    for i in items[0:15]:
        print(f"{i.name:<40} {i.quantity:<15} {i.location:<25} {User.find_user(i.lastModifiedUID).firstName:<25} {i.lastModifiedDate:<25}")

    print(f"[Page: 1 of {((len(items)-1)//15)+1}]")

    input("\n 1: Back to Menu   2: Next Page   3: Previous Page   4: Search   5: Edit Item\nOption: ")

if __name__ == "__main__":
    title_page()
