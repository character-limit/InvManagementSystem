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
        inventory_page(1)
    elif choice == "2":
        User.current = None #log out
        title_page()
    else:
        menu_page()

def inventory_page(page):
    items = Item.load_items()   #reload items 
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== Inventory ===\n\n")

    # display in table.
    print_table(page, items)

    choice = input("\n 1: Back to Menu   2: Next Page   3: Previous Page   4: Search   5: Edit Table\nOption: ")

    if choice == "1":
        menu_page()
    elif choice == "2":
        inventory_page(page+1 if (page*15)<len(items) else page)
    elif choice == "3":
        inventory_page(page-1 if page >1 else 1)
    elif choice == "4":
        inventory_search(1) #default page to 1
    elif choice == "5":
        print("")
    else:
        inventory_page(page)

def print_table(page, items):

    lb = ((page)*15)-15 #get lower bound for items to display on page
    ub = lb +15         #get upper bound for items to display on page

    print(f'{"Name":<40} {"Quantity":<15} {"Location":<25} {"Last Modified By":<25} {"Last Modified ":<25}')#header
    print("-"*130)#separator
    for i in items[lb:ub]:  #slice items according to above
        print(f"{i.name:<40} {i.quantity:<15} {i.location:<25} {User.find_user(i.lastModifiedUID).firstName:<25} {i.lastModifiedDate:<25}")

    print(f"[Page: {page} of {((len(items)-1)//15)+1}]")

def inventory_search(page):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== Inventory Search ===\n")
    query = input("Enter search term: ").lower() #case insensitive

    items = Item.load_items()
    results = [item for item in items if query in item.name.lower() or query in item.location.lower()] #check against name and loci

    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"=== Search: '{query}' ===\n")

    if results:
        print_table(page, results)

        choice = input("\n 1: Back to Inventory   2: Next Page   3: Previous Page   4: Edit Search\nOption: ")

        if choice == "1":
            inventory_page(1)
        elif choice == "2":
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"=== Search: '{query}' ===\n")
            print_table((page+1 if (page*15)<len(results) else page), results)
            choice = input("\n 1: Back to Inventory   2: Next Page   3: Previous Page   4: Edit Search\nOption: ")
        elif choice == "3":
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"=== Search: '{query}' ===\n")
            print_table((page-1 if page >1 else 1), results)
            choice = input("\n 1: Back to Inventory   2: Next Page   3: Previous Page   4: Edit Search\nOption: ")
        elif choice == "4":
            inventory_search(1) 
    else:
        print("No items found matching your search.")

    input("\nPress Enter to return to Inventory...")
    inventory_page(1)

if __name__ == "__main__":
    title_page()
