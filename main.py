import csv, os
from datetime import datetime
from item import Item
from user import User

print("hello")

def main():
    items = Item.load_items()

    for i in items:
        print(i)


    temp = Item("testname", 40, "sotragename", "0005", datetime.now().strftime("%d/%m/%Y %H:%M"))

    items.append(temp)

    Item.write_items(items)

    for i in items:
        print(i)


    users = User.load_users()

    for i in users:
        print(i)


    temp = User("first", "last", "username", "password", "UID")

    users.append(temp)

    User.write_users(users)

    for i in users:
        print(i)


if __name__ == "__main__":
    main()
