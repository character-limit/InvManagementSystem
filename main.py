import csv, os
from datetime import datetime
from item import Item

print("hello")

def main():
    items = Item.load_objects()

    for i in items:
        print(i)


    temp = Item("testname", 40, "sotragename", "0005", datetime.now().strftime("%d/%m/%Y %H:%M"))

    items.append(temp)

    Item.write_objects(items)

    for i in items:
        print(i)


if __name__ == "__main__":
    main()
