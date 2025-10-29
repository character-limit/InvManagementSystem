import csv, os

CSV_PATH = "users.csv"
COLUMNS = ["firstName", "lastName", "username", "password", "UID"] # fields for item obj in csv file

class User:

    def __init__(self, firstName, lastName, username, password, UID):
        self.firstName = firstName
        self.lastName = lastName
        self.username = username
        self.password = password
        self.UID = UID

    def __repr__(self):
        return f"User(name={self.firstName} {self.lastName}, username={self.username}, password={self.password}, UID={self.UID})"
    
    @classmethod
    def load_users(cls):
        users = [] #init return

        if not os.path.exists(CSV_PATH):
            print("no .csv found, check dir")
            return users # catch if no file.

        #read file, add each item to array of item obj
        with open(CSV_PATH, newline = "") as csvfile:
            reader = csv.DictReader(csvfile)

            for tempItem in reader:
                users.append(cls(**tempItem))

        return users
    
    @classmethod
    def write_users(cls, users):
        if not os.path.exists(CSV_PATH):
            print("no .csv found, check dir")
            return users # catch if no file.

        with open(CSV_PATH, mode = "w", newline = "") as csvfile: #write whole file, easier for edits.
            writer = csv.DictWriter(csvfile, fieldnames=COLUMNS)
            writer.writeheader()

            for item in users:
                writer.writerow({"firstName":item.firstName, "lastName":item.lastName, "username":item.username, "password":item.password, "UID":item.UID})
        print("write success")