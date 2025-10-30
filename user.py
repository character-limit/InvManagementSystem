import csv, os, bcrypt

CSV_PATH = "users.csv"
COLUMNS = ["firstName", "lastName", "username", "password", "UID"] # fields for item obj in csv file

class User:

    users = [] #list of all user accs

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

        cls.users = []

        if not os.path.exists(CSV_PATH):
            print("no .csv found, check dir")
            return

        #read file, add each item to array of item obj
        with open(CSV_PATH, newline = "") as csvfile:
            reader = csv.DictReader(csvfile)

            for tempItem in reader:
                cls.users.append(cls(**tempItem))


    @classmethod
    def write_users(cls):
        if not os.path.exists(CSV_PATH):
            print("no .csv found, check dir")
            return

        with open(CSV_PATH, mode = "w", newline = "") as csvfile: #write whole file, easier for edits.
            writer = csv.DictWriter(csvfile, fieldnames=COLUMNS)
            writer.writeheader()

            for item in cls.users:
                writer.writerow({"firstName":item.firstName, "lastName":item.lastName, "username":item.username, "password":item.password, "UID":item.UID})
        print("write success")

    @classmethod
    def gen_UID(cls):
        cls.load_users()

        if not cls.users:
            return "0001" #catch empty list
        
        temp = int(cls.users[-1].UID) +1 #get last uid +=1
        uid = str(temp).zfill(4) #convert int to str with leading 0 for storage

        return uid
        
    def append_user(self):
        if not os.path.exists(CSV_PATH):
            print("no .csv found, check dir")
            return 
        
        with open(CSV_PATH, mode="a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=COLUMNS)

            writer.writerow({"firstName":self.firstName, "lastName":self.lastName, "username":self.username, "password":self.password, "UID":self.UID})
        
        User.load_users() #refresh users list

    def create_user(firstName, lastName, username, plainTextPassword):

        self = User(firstName, lastName, username, User.password_encrypt(plainTextPassword), User.gen_UID())

        self.append_user()

    @staticmethod
    def password_encrypt(password):

        return bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt())

    @staticmethod
    def password_check(entered, password):
        if bcrypt.checkpw(entered, password):
            return True
        else:
            return False