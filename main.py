import csv, os
from datetime import datetime
from item import Item
from user import User

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

##ADD VALIDATION!!
def add_item_page():
    #Page to input item name to be Added.
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== Add Item ===\n")

    name = input("Item Name: ")
    quantity = input("Quantity: ")
    location = input("Location: ")
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

    item_selector(results) # load table, with numbered input to select a specific item.
    #select from results using item selector

def edit_item_page():
    print("=== Edit Item ===\n")

##UNFINISEHD
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

    print(f"Selected item: {selected_item}") #debug print

    return selected_item


if __name__ == "__main__":
    title_page()
