import csv, os, bcrypt

CSV_PATH = "users.csv"
COLUMNS = ["firstName", "lastName", "username", "password", "UID"] # fields for item obj in csv file

class User:

    users = [] #list of all user accs
    current = None

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
    
    @classmethod
    def create_user(cls, firstName, lastName, username, plainTextPassword):
        cls.append_user(User(firstName, lastName, username, User.password_encrypt(plainTextPassword), User.gen_UID()))

    @classmethod
    def append_user(cls, user):
        if not os.path.exists(CSV_PATH):
            print("no .csv found, check dir")
            return 
        
        with open(CSV_PATH, mode="a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=COLUMNS)

            writer.writerow({"firstName":user.firstName, "lastName":user.lastName, "username":user.username, "password":user.password, "UID":user.UID})

        User.load_users() #refresh users list

    @staticmethod
    def password_encrypt(password):

        return bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt()).decode("utf-8") #hash, decode to str for csv

    @staticmethod
    def password_check(entered, password):
        if bcrypt.checkpw(entered.encode("utf-8"), password.encode("utf-8")):
            return True
        else:
            return False
        
    @staticmethod
    def login(username, password):
        User.load_users()

        for user in User.users:
            if user.username == username:
                if User.password_check(password, user.password):
                    print("login success")
                    User.current = user
                else:
                    print("incorrect password")

        print("username not found")

    @staticmethod
    def find_user(UID):
        User.load_users()

        for user in User.users:
            if user.UID == UID:
                return user
        return None