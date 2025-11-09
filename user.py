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
    
    @classmethod             #Function to load all users from csv to a list
    def load_users(cls):

        cls.users = []

        if not os.path.exists(CSV_PATH):
            print("no .csv found, check dir")
            return           # catch if no file.

         #read file, add each item to array of item obj
        with open(CSV_PATH, newline = "") as csvfile:
            reader = csv.DictReader(csvfile)

            for tempItem in reader:
                cls.users.append(cls(**tempItem))


    @classmethod   #Function to write users list to csv file
    def write_users(cls):
        if not os.path.exists(CSV_PATH):
            print("no .csv found, check dir")
            return  # catch if no file.

        with open(CSV_PATH, mode = "w", newline = "") as csvfile: #write whole file, easier for edits.
            writer = csv.DictWriter(csvfile, fieldnames=COLUMNS)
            writer.writeheader()    #Re-write header as writing whole file.

            for item in cls.users:  #iterate through users, write each to file.
                writer.writerow({
                    "firstName":item.firstName,
                    "lastName":item.lastName, 
                    "username":item.username, 
                    "password":item.password, 
                    "UID":item.UID})

    @classmethod    #Function to generate a new UID for each new account
    def gen_UID(cls):
        cls.load_users()    #load all users

        if not cls.users:
            return "0001" #catch empty list
        
        temp = int(cls.users[-1].UID) +1 #get last uid +=1
        uid = str(temp).zfill(4) #convert int to str with leading 0 for storage

        return uid
    
    @classmethod    #Function to create a new user and then append it to csv.
    def create_user(cls, firstName, lastName, username, plainTextPassword):
        cls.append_user(User(firstName, lastName, username, User.password_encrypt(plainTextPassword), User.gen_UID()))

    @classmethod    #Function to append a user to csv file
    def append_user(cls, user):
        if not os.path.exists(CSV_PATH):
            print("no .csv found, check dir")
            return  #catch if no file.
        
        with open(CSV_PATH, mode="a", newline="") as csvfile: #open in append mode
            writer = csv.DictWriter(csvfile, fieldnames=COLUMNS)    #add only new line, dont re-write fully.
            writer.writerow({
                "firstName":user.firstName, 
                "lastName":user.lastName, 
                "username":user.username, 
                "password":user.password, 
                "UID":user.UID})

        User.load_users() #refresh users list

    @staticmethod   #Function to take plaintext password and return hashed ver.
    def password_encrypt(password):
        return bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt()).decode("utf-8") #hash, decode to str for csv

    @staticmethod   #Function to check entered password against stored hashed password
    def password_check(entered, password):
        if bcrypt.checkpw(entered.encode("utf-8"), password.encode("utf-8")):#bcrypt lib check
            return True                                                      #must be in bytes format, hence encode.
        else:
            return False
        
    @staticmethod   #method to check inputted user data, and then put them as session object if correct.
    def login(username, password):
        User.load_users()

        for user in User.users:#iterate through users, check for match
            if user.username == username:
                if User.password_check(password, user.password):
                    print("login success")
                    User.current = user
                    return True

    @staticmethod
    def find_user(UID): #function to take UID and return user obj for corresponding.
        User.load_users()

        for user in User.users:
            if user.UID == UID:
                return user
        return None