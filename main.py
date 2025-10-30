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
        print(i) """


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

    User.login(username, password)

if __name__ == "__main__":
    main()
