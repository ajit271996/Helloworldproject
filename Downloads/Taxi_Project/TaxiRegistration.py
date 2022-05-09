from pymongo import MongoClient
import re

class TaxiRegistration:
    def __init__(self):
        self.taxi = {}
        self.client = MongoClient("mongodb+srv://admin:admin@cluster0.pgpb7.mongodb.net/test")
        self.db = self.client.TaxiCorp

    def create_taxi(self,taxi_number,taxi_type,taxi_driver_id,taxi_driver_phone):
        tres = ""
        taxiNumber = taxi_number
        taxiType = taxi_type
        taxiDriverId = taxi_driver_id
        taxiDriverPhome = taxi_driver_phone
        if self.duplicate_taxiNumber(taxiNumber, taxiType, taxiDriverId,taxi_driver_phone):
            if self.verify_taxi(taxiNumber, taxiType, taxiDriverId):
                self.taxi = {"taxiNumber": taxiNumber, "taxiType": taxiType, "taxiDriverId": taxiDriverId ,"taxiDriverPhone": taxi_driver_phone}
                result = self.db.taxidata.insert_one(self.taxi)
                # self.taxilist.append(self.taxi)
                print("Taxi registered successfully,taxiid - {0}".format(result.inserted_id))
                tres = "Taxi registered successfully,taxiid - {0}".format(result.inserted_id)
            # print(self.taxilist)

        else:
            print("Taxi is already registered")
            tres = "Taxi is already registered"
        return  tres

    def duplicate_taxiNumber(self, taxiNumber, taxiType, taxiDriverId,duplicate_taxiNumber):
        flag = 0
        for taxi in self.db.taxidata.find():
            if taxi["taxiNumber"] == taxiNumber :
                flag = 1
        if flag == 0:
            return True
        else:
            return False

    def verify_taxi(self, taxiNumber, taxiType, taxiDriverId):
        regex = r'^[a-zA-Z0-90-9]*$'
        flag1 = -1
        if taxiType.isalpha():
            flag1 =0
        else:
            print("Invalid taxiType! Please enter the valid taxiType")
            flag1 =1
        if (re.fullmatch(regex, taxiNumber)):
            flag1 =0
        else:
            print("Invalid taxiNumber! Please enter the valid taxiNumber")
            flag1=1
        if (re.fullmatch(regex, taxiDriverId)):
            flag1=0
        else:
            print("Invalid taxiDriverId! Please enter the valid taxiDriverId")
            flag1=1

        if flag1==0:
            return True
        else:
            return False

    def get_all_registered_taxis(self):
        taxilst = self.db.taxidata.find()
        taxis_in_db = []
        for taxi in taxilst:
            taxis_in_db.append(taxi['taxiNumber'])
        return taxis_in_db
        
    def get_all_registered_taxis_all_data(self):
        taxilst = self.db.taxidata.find()
        taxis_in_db = []
        for taxi in taxilst:
            taxis_in_db.append(taxi)
        return taxis_in_db
    
    def get_taxi_type_of_taxi_num(self,txnum):
        taxitype = ""
        for taxi in self.db.taxidata.find():
            if taxi["taxiNumber"] == txnum :
                taxitype = taxi["taxiType"]
        return taxitype

    def insert_records_from_csv(self, csvpath):
        with open(csvpath + '.csv', 'r') as taxi_dt:
            tax_reg_list = []
            for taxi_row in taxi_dt:
                taxi_row = taxi_row.rstrip()
                if taxi_row:
                    (taxiNumber, taxiType, taxiDriverName,taxiDriverPhone) = taxi_row.split(',')
                    self.create_taxi(taxiNumber ,taxiType ,taxiDriverName,taxiDriverPhone)