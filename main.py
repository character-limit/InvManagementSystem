import csv, os
from datetime import datetime
from item import Item
from user import User


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
    username = input("Username: ").lower()
    password = input("Password: ")

    

    if User.login(username, password) == True:
        menu_page()
    else:
        print("Incorrect login. Please try again.")
        input("Press Enter to continue...")
        login_page()

def create_user_page():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== Create Account ===")

    while True:
        firstName = input("First Name: ").capitalize()
        if len(firstName) < 2 or len(firstName) > 30 or not all(i.isalpha() for i in firstName): #check length and string content
            os.system('cls' if os.name == 'nt' else 'clear') #clear display
            print("Invalid input.\n\n") #ask again
        else:
            break
    
    while True:
        lastName = input("Last Name: ").capitalize()
        if len(lastName) < 2 or len(lastName) > 30 or not all(i.isalpha() for i in lastName): #check length and string content
            os.system('cls' if os.name == 'nt' else 'clear') #clear display
            print("Invalid input.\n\n") #ask again
        else:
            break
    
    while True:
        username = input("Username: ").lower()
        if len(username) < 2 or len(username) > 30 or not all(i.isalnum() for i in username): #check length and string content
            os.system('cls' if os.name == 'nt' else 'clear') #clear display
            print("Invalid input - username must be alphanumeric\n\n") #ask again
        else:
            break

    while True:
        password = input("Password: ")
        if len(password) < 8 or len(password) > 30:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Invalid input - password must be 8-30 characters for security\n\n")
        else:
            break

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
    #Display inventory page, allow option seleciton adn page icnrementation/decremebnt

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
        inventory_search_page(1) #default page to 1
    elif choice == "5":
        edit_table_page()
    else:
        inventory_page(page)

def print_table(page, items):
    #Display all items in the list provided in param, and display in intervals of 15 according the the page no.

    lb = ((page)*15)-15 #get lower bound for items to display on page
    ub = lb +15         #get upper bound for items to display on page

    print(f'{"Name":<40} {"Quantity":<15} {"Location":<25} {"Last Modified By":<25} {"Last Modified ":<25}')#header
    print("-"*130)#separator

    for i in items[lb:ub]:  #slice items according to above
        print(f"{i.name:<40} {i.quantity:<15} {i.location:<25} {User.find_user(i.lastModifiedUID).firstName:<25} {i.lastModifiedDate:<25}")

    print(f"[Page: {page} of {((len(items)-1)//15)+1}]")

def inventory_search_page(page, query=None):#params: query optional, its for recursive calls when incrementing pages..ect
    #Print the page to request a search term, and then display results.

    if not query: 
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== Inventory Search ===\n")
        query = input("Enter search term: ").lower() #case insensitive

    items = Item.load_items()
    results = [item for item in items if query in item.name.lower() or query in item.location.lower()] #check against name and loci

    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"=== Search: '{query}' ===\n")

    if results:
        print_table(page, results) #print table, of results, according to page no

        choice = input("\n 1: Back to Inventory   2: Next Page   3: Previous Page   4: New Search\nOption: ") 

        if choice == "1":
            inventory_page(1) #ret to inv page

        elif choice == "2": #inc page
            inventory_search_page(page+1 if (page*15)<len(results) else page, query)

        elif choice == "3": #dec page
            inventory_search_page(page-1 if page >1 else 1, query)

        elif choice == "4":
            inventory_search_page(1)
        
    print("No items found matching your search.")
    input("\nPress Enter to return to Inventory...")
    inventory_page(1)

def edit_table_page():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== Edit Inventory Logs ===\n")

    choice = input("1: Add Item   \n2: Remove Item   \n3: Edit Item   \n4: Back to Inventory\n\nOption: ")

    if choice == "1":
        add_item_page()
    elif choice == "2":
        remove_item_page()
    elif choice == "3":
        edit_item_page()
    elif choice == "4":
        inventory_page(1)
    else:
        edit_table_page()

def add_item_page():
    #Page to input item name to be Added.
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== Add Item ===\n")

    name = ask_validate_name_input()   #function to validate name inputs for ITEM
    quantity = ask_validate_quantity_input()   #function to validate quantity inputs
    location = ask_validate_location_input()   #function to validate location inputs
    lastModifiedUID = User.current.UID
    lastModifiedDate = datetime.now().strftime("%d/%m/%Y %H:%M")

    Item.create_item(name, quantity, location, lastModifiedUID, lastModifiedDate)

    inventory_page(1)

def remove_item_page():
    #Page to input item name to be removed.
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== Remove Item ===\n")

    #search for items with name 

    query = input("\n\nSearch for item name: ").lower() #case insensitive

    items = Item.load_items()
    results = [item for item in items if query in item.name.lower() or query in item.location.lower()] #check against name and loci

    if not results: #None found, ret
        os.system('cls' if os.name == 'nt' else 'clear')
        print("No items found matching your search.")
        input("\nPress Enter to return to Inventory...")
        inventory_page(1)

    item = item_selector(results) #load table, with numbered input to select a specific item.

    if not item: #go back if asked
        inventory_page(1)
    
    Item.remove_item(item)
    inventory_page(1)

def edit_item_page():
    #Page to input item name to be edited.
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== Edit Item ===\n")

    #search for items with name 
    query = input("\n\nSearch for item name: ").lower() #case insensitive

    items = Item.load_items()   #re-read items to ensure latest ver is synced.
    results = [item for item in items if query in item.name.lower() or query in item.location.lower()] #check against name and loci, case insensitive

    if not results: #None found, return
        os.system('cls' if os.name == 'nt' else 'clear')#clear display
        print("No items found matching your search.") #error message
        input("\nPress Enter to return to Inventory...")
        inventory_page(1)

    item = item_selector(results) #load table, with numbered input to select a specific item.

    if not item: #go back if asked
        inventory_page(1) #page 1

    os.system('cls' if os.name == 'nt' else 'clear')    #clear display

    #output current item details
    print("Name: ", item.name)
    print("Quantity: ", item.quantity)
    print("Location: ", item.location)
    print("Last Modified By: ", User.find_user(item.lastModifiedUID).firstName)
    print("Last Modified Date: ", item.lastModifiedDate)

    #output options
    print("\n\n1: Name   2: Quantity   3: Location   4: Back To Inventory")
    choice = input("\nSelect field to edit: ")

    #parse choice to get new value inputted
    if choice == "1":
        item.name = ask_validate_name_input() #function to validate name inputs for ITEM
    elif choice == "2":
        item.quantity = ask_validate_quantity_input()   #function to validate quantity inputs
    elif choice == "3":
        item.location = ask_validate_location_input()   #function to validate location inputs
    elif choice == "4":
        inventory_page(1) #go back - page 1
    else:
        input("Invalid choice. Press Enter To Go Back To Inventory...")
        inventory_page(1)

    Item.remove_item(item) #remove old

    item.lastModifiedUID = User.current.UID #set user id
    item.lastModifiedDate = datetime.now().strftime("%d/%m/%Y %H:%M") #get and set current time.

    Item.append_item(item) #add edited

    inventory_page(1)   #return to inventory view (page 1)

def item_selector(items): # Display items list parameter in table format with number to select specific item.
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== Select Item ===\n")

    print(f'       {"Name":<40} {"Quantity":<15} {"Location":<25} {"Last Modified By":<25} {"Last Modified ":<25}')#header
    print("-"*130) #separator

    j = 0
    for i in items:
        print(f"[{j}]   {i.name:<40} {i.quantity:<15} {i.location:<25} {User.find_user(i.lastModifiedUID).firstName:<25} {i.lastModifiedDate:<25}")
        j += 1

    choice = input("\nSelect item by number (b to go back): ")

    if choice == 'b':
        return

    if not choice.isdigit() or int(choice) < 0 or int(choice) >= len(items): #validation that selection is displayed
        item_selector(items) #reload if invalid
        return
    
    #if item is valid then return selected item
    selected_item = items[int(choice)]

    return selected_item

def ask_validate_name_input():
    #Function to validate name inputs for ITEM
    value = input("Enter name: ") #ask again

    while True: #continue until correct
        if len(value) < 2 or len(value) > 30 or not all(i.isalpha() or i.isspace() for i in value): #check length and string content
            os.system('cls' if os.name == 'nt' else 'clear') #clear display
            value = input("Invalid input.\n\nEnter name: ") #ask again
        else:
            break

    return value    #return valid name

def ask_validate_quantity_input():
    #Function to validate quantity input
    value = input("Enter quantity: ")

    while True: #continue until correct
        if not value.isdigit() or int(value) < 0:
            os.system('cls' if os.name == 'nt' else 'clear') #clear display
            value = input("Invalid input.\n\nEnter quantity: ") #ask again
        else:
            break

    return value    #return valid quantity

def ask_validate_location_input():
    #Function to validate location input
    value = input("Enter location: ") #ask again
    
    while True: #continue until correct
        if len(value) < 2 or len(value) > 30 or not all(i.isalnum() or i.isspace() for i in value): #check length and string content
            os.system('cls' if os.name == 'nt' else 'clear') #clear display
            value = input("Invalid input.\n\nEnter location: ") #ask again
        else:
            break

    return value    #return valid location

if __name__ == "__main__":
    title_page()
