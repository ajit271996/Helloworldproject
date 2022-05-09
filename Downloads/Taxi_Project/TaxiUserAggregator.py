from datetime import datetime

from pymongo import MongoClient, GEOSPHERE
from bson.son import SON
import pprint
import random
import json
import boto3
from json2html import *

from UserRegistration import UserRegistration
from TaxiRegistration import TaxiRegistration


class TaxiUserAggregator:

    def __init__(self):
        self.db_uri = 'mongodb+srv://admin:admin@cluster0.pgpb7.mongodb.net/test'
        self.client = MongoClient(self.db_uri)
        self.db = self.client.TaxiCorp

    def get_nearest_taxi_for_user(self, lstTaxiSimulation, lstUserSimulation ,user_phone_number,usr_taxi_type):
        #  List of taxis
        taxi_list = lstTaxiSimulation
        # list of Customers
        customer_list = lstUserSimulation
        # Access the MongoDB Service
        aggregator_cli = MongoClient(self.db_uri)
        # Create a Database
        aggregator_db = aggregator_cli['TaxiCorp']
        # Create Collections
        taxis = aggregator_db['taxis_location']
        res = taxis.delete_many({})

        customers = aggregator_db['customers_locations']
        res = customers.delete_many({})

        # Populate the Collections
        res = taxis.insert_many(taxi_list)
        res = customers.insert_many(customer_list)

        # Display the Database Collections
        print('########################### Aggregator: TAXIS ###########################')

        for doc in taxis.find():
            pprint.pprint(doc)

        print('########################### Aggregator: CUSTOMERS ###########################')

        for doc in customers.find():
            pprint.pprint(doc)

        # Create Index(es)
        taxis.create_index([('location', GEOSPHERE)])
        customers.create_index([('location', GEOSPHERE)])

        # Run Queries

        # Select specific  Customer
        usr = UserRegistration()
        txi = TaxiRegistration()
        customername = usr.get_registered_user_by_phone_number(user_phone_number)
        filtered_lst = list(filter(lambda person: person['name'] == customername[0], customer_list))
        customer_loc = filtered_lst[0]['location']
        cust_name = filtered_lst[0]['name']

        jsonlist = []
        custloc = {}
        nertxiloc = []
        print('######################## CUSTOMER LOCATION ########################')
        print(f'Customer Name : {cust_name}')
        pprint.pprint(customer_loc)
        custlat = customer_loc['coordinates'][1]
        custlng = customer_loc['coordinates'][0]
        custloc['CustomerName'] = cust_name
        custloc['Customer_Location_lat'] = custlat
        custloc['Customer_Location_lng'] = custlng
 
        
        jsonlist.append(custloc)
        # jsonlist.append(customer_loc)

        # Getting all taxis within a certain distance range from a customer
        print(f'######################## ALL TAXIS WITHIN 1 Km  from Customer && Type {usr_taxi_type} ########################')
        
        range_query = {'location': SON([("$near", customer_loc), ("$maxDistance", 1000)])}
        near_type_list = []
        for doc1 in taxis.find(range_query):
            neartxloc = {}
            pprint.pprint(doc1)
            txname = doc1['name']
            neartxloc['Taxi Number'] = txname
            txitype  = txi.get_taxi_type_of_taxi_num(txname)
            print(f"Got Taxi Type as {txitype} for Taxi num {txname}")
            tloca = doc1['location']
            tlat = tloca['coordinates'][1]
            tlng = tloca['coordinates'][0]
            neartxloc['Taxi Latitude'] = tlat
            neartxloc['Taxi Longitute'] = tlng
            neartxloc['Taxi Type'] = txitype
            if usr_taxi_type == txitype or usr_taxi_type == "All":    
                jsonlist.append(neartxloc)
                near_type_list.append(doc1)

                
        near_taxis = aggregator_db['nearest_taxis']
        res = near_taxis.delete_many({})

        # Populate the Collections
        res = near_taxis.insert_many(near_type_list)

        # Getting the nearest taxis withim range and of type  to a customer
        near_taxis.create_index([('location', GEOSPHERE)])
        print(f'######################## THE  NEAREST TAXI  with Type {usr_taxi_type} ########################')
        matchdic = {}
        nearest_query = {'location': {"$near": customer_loc}}
        for doc2 in near_taxis.find(nearest_query).limit(1):
            pprint.pprint(doc2)
            matchdic['Nearest TAXI Number'] = doc2['name']
            txitype  = txi.get_taxi_type_of_taxi_num(doc2['name'])
            mtloca = doc2['location']
            mtlat = mtloca['coordinates'][1]
            mtlng = mtloca['coordinates'][0]
            matchdic['Taxi Latitude'] = mtlat
            matchdic['Taxi Longitute'] = mtlng 
            matchdic['Taxi Type'] =  txitype      
            jsonlist.append(matchdic)  
        return  jsonlist

    def confirm_user_taxi_booking(self,taxi_number,user_phone):
        if self.duplicate_taxi_booking(taxi_number, user_phone):
            self.booking = {"taxinumber": taxi_number, "userphone": user_phone,"bookingtime": str(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))}
            result = self.db.TaxiUserBookingData.insert_one(self.booking)
            self.send_notification_user(taxi_number)
            print(f"User  {user_phone } successfully booked taxi {taxi_number} Booking ID : {result.inserted_id}")
        else:
            print(f"The Taxi with Id {taxi_number} is not available for booking as it has been already booked by another customer")


    def duplicate_taxi_booking(self, taxi_number,user_phone):
        flag = 0
        for bkng in self.db.TaxiUserBookingData.find():
            if bkng["taxinumber"] == taxi_number :
                flag = 1
        if flag == 0:
            return True
        else:
            return False

    def get_simulation_data_taxi_from_db(self):
        taxiloc = self.db.taxis_location.find()
        taxiloc_db = []
        for tdata in taxiloc:
            taxiloc_db.append(tdata)
        return taxiloc_db

    def get_confirmed_taxi_bookings(self):
        taxibkdata = self.db.TaxiUserBookingData.find()
        taxibk_db = []
        for tdata in taxibkdata:
            taxibk_db.append(tdata)
        return taxibk_db
        
    def send_notification_user(self,taxinum):
        client = boto3.client('sns', region_name='us-east-1')
        topic_arn = "arn:aws:sns:us-east-1:637577528657:Taxibooking"

        try:
            client.publish(TopicArn=topic_arn, Message=f"Taxi {taxinum} Booked for User ", Subject="Taxi Booking Confirmed")
            result = 1
        except Exception:
            result = 0