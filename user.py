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

    @classmethod
    def gen_UID(cls):
        users = cls.load_users()

        if not users:
            return "0001" #catch empty list
        
        temp = int(users[-1].UID) +1 #get last uid +=1
        uid = str(temp).zfill(4) #convert int to str with leading 0 for storage

        return uid
        
    def append_user(self):
        if not os.path.exists(CSV_PATH):
            print("no .csv found, check dir")
            return 
        
        with open(CSV_PATH, mode="a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=COLUMNS)

            writer.writerow({"firstName":self.firstName, "lastName":self.lastName, "username":self.username, "password":self.password, "UID":self.UID})
        
    def create_user(self, firstName, lastName, username, plainTextPassword):
        
        self.firstName = firstName
        self.lastName = lastName
        self.username = username
        self.password = self.password_encrypt(plainTextPassword)
        self.UID = self.genUID()

        self.append_user(self)

    @staticmethod
    def password_encrypt(password):
        print("")

    @staticmethod
    def password_decrypt(password):
        print("")

    
        
