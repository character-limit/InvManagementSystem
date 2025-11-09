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
    
    #Function to write inputted items list to csv file
    @classmethod
    def write_items(cls, items):
        #Check file path exists, if not, output error
        if not os.path.exists(CSV_PATH):
            print("no .csv found, check dir")
            return
        
        with open(CSV_PATH, mode = "w", newline = "") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=COLUMNS)    #Write whole file, easier for edits.
            writer.writeheader() #Re-write header as writing whole file.

            for item in items:  #iterate through items, write each to the file.
                writer.writerow({
                    "name":item.name, 
                    "quantity":item.quantity, 
                    "location":item.location, 
                    "lastModifiedUID":item.lastModifiedUID, 
                    "lastModifiedDate":item.lastModifiedDate
                    })

    @classmethod    #Function to create a new item and then append it to csv.
    def create_item(cls, name, quantity, location, lastModifiedUID, lastModifiedDate):
        cls.append_item(Item(name, quantity, location, lastModifiedUID, lastModifiedDate))

    @classmethod
    def append_item(cls, item):
        if not os.path.exists(CSV_PATH):
            print("no .csv found, check dir")
            return #catch if no file.
        
        with open(CSV_PATH, mode="a", newline="") as csvfile: #open in append mode
            writer = csv.DictWriter(csvfile, fieldnames=COLUMNS)
            #add only new line, dont re-write fully.
            writer.writerow({"name":item.name, "quantity":item.quantity, "location":item.location, "lastModifiedUID":item.lastModifiedUID, "lastModifiedDate":item.lastModifiedDate})

        Item.load_items() #refresh items list

    @classmethod 
    def remove_item(cls, item):
        items = cls.load_items() #load current items

        #update items list, exluding removed item
        items = [i for i in items if not (i.name == item.name and i.location == item.location and i.lastModifiedDate == item.lastModifiedDate)]

        #Re-wrute
        cls.write_items(items)

        Item.load_items() #refresh items list