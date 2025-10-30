import csv, os

CSV_PATH = "inventory.csv"
COLUMNS = ["name", "quantity", "location", "lastModifiedUID", "lastModifiedDate"] # fields for item obj in csv file

class Item:
    def __init__(self, name, quantity, location, lastModifiedUID, lastModifiedDate):
        self.name = name
        self.quantity = int(quantity)
        self.location = location
        self.lastModifiedUID = lastModifiedUID
        self.lastModifiedDate = str(lastModifiedDate)

    def __repr__(self):
        return f"Item(name={self.name}, quantity={self.quantity}, location={self.location}, lastModifiedUID={self.lastModifiedUID}, lastModifiedDate={self.lastModifiedDate})"
    
    @classmethod
    def load_items(cls):
        items = [] #init return

        if not os.path.exists(CSV_PATH):
            print("no .csv found, check dir")
            return items # catch if no file.

        #read file, add each item to array of item obj
        with open(CSV_PATH, newline = "") as csvfile:
            reader = csv.DictReader(csvfile)

            for tempItem in reader:
                items.append(cls(**tempItem))

        return items
    
    @classmethod
    def write_items(cls, items):
        if not os.path.exists(CSV_PATH):
            print("no .csv found, check dir")
            return

        with open(CSV_PATH, mode = "w", newline = "") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=COLUMNS)
            writer.writeheader()

            for item in items:
                writer.writerow({"name":item.name, "quantity":item.quantity, "location":item.location, "lastModifiedUID":item.lastModifiedUID, "lastModifiedDate":item.lastModifiedDate})
