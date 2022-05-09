
from pymongo import MongoClient
import re


class UserRegistration:
    def __init__(self):
        self.user = {}
        self.client = MongoClient("mongodb+srv://admin:admin@cluster0.pgpb7.mongodb.net/test")
        self.db = self.client.TaxiCorp

    def create_user(self,user_name,user_email,user_phone_number):
        res = ""
        name = user_name
        email = user_email
        phonenumber = user_phone_number
        if self.duplicate_user(name, email, phonenumber):
            if self.verify_user(name, email, phonenumber):
                self.user = {"name": name, "email": email, "phonenumber": phonenumber}
                result = self.db.userdata.insert_one(self.user)
                # self.userlist.append(self.user)
                print("User registered successfully,userid - {0}".format(result.inserted_id))
                res = f"User registered successfully,userid - {result.inserted_id}"
            # print(self.userlist)

        else:
            print("Name, email or phone number are already registered")
            res = f"Name, email or phone number are already registered"
        return res

    def duplicate_user(self, name, email, phonenumber):
        flag = 0
        for user in self.db.userdata.find():
            if user["name"] == name or user["email"] == email or user["phonenumber"] == phonenumber:
                flag = 1
        if flag == 0:
            return True
        else:
            return False

    def verify_user(self, name, email, phonenumber):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        flag1 = -1
        if name.isalpha():
            flag1 =0
        else:
            print("Invalid name! Please enter the valid Name")
            flag1 =1
        if (re.fullmatch(regex, email)):
            flag1 =0
        else:
            print("Invalid Email! Please enter the valid Email")
            flag1=1
        if phonenumber.isnumeric() and int(len(str(phonenumber))) == 10:
            flag1=0
        else:
            print("Invalid Phonenumber! Please enter the valid Phonenumber")
            flag1=1

        if flag1==0:
            return True
        else:
            return False

    def get_all_registered_users(self):
        userlst = self.db.userdata.find()
        users_in_db = []
        for usr in userlst:
            users_in_db.append(usr['name'])
        return users_in_db
        
    def get_all_registered_users_all_data(self):
        userlst = self.db.userdata.find()
        users_in_db = []
        for usr in userlst:
            users_in_db.append(usr)
        return users_in_db

    def get_registered_user_by_phone_number(self,phone_num):
        userlst = self.db.userdata.find({"phonenumber": phone_num})
        users_in_db = []
        for usr in userlst:
            users_in_db.append(usr['name'])
        return users_in_db

    def insert_records_from_csv(self, csvpath):
        with open(csvpath + '.csv', 'r') as user_dt:
            for user_row in user_dt:
                user_row = user_row.rstrip()
                if user_row:
                    (userName, userEmail, userPhone) = user_row.split(',')
                    self.create_user(userName ,userEmail ,userPhone)

