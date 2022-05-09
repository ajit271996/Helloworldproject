import json
from json2html import *
from flask import jsonify

from DefineArea import DefineArea
from SimulateTaxiPosition import SimulateTaxiPosition
from TaxiRegistration import TaxiRegistration
from TaxiUserAggregator import TaxiUserAggregator
from UserRegistration import UserRegistration
from flask import Response
from bson import json_util


class FrontEnd:
    def __init__(self):
        pass

    def create_taxis_data(self):
        taxis = TaxiRegistration()
        taxis_list = taxis.get_all_registered_taxis_all_data()
        if len(taxis_list) == 0:
            taxi_data_file_path = './taxilist'
            taxis.insert_records_from_csv(taxi_data_file_path)
        html = "<table><th>TaxiNumber</th>"
        taxi_dict_list = []
        for taxi in taxis_list:
            taxi_dict = {"TaxiDriverName":taxi['taxiDriverId'] ,"Taxi Number":taxi['taxiNumber'] ,"Taxi Type":taxi['taxiType'],"Taxi Drive Number":taxi['taxiDriverPhone']}
            taxi_dict_list.append(taxi_dict)
        data_processed = json.dumps({"taxis_list": taxi_dict_list})
        formatted_table = json2html.convert(json=data_processed)
        return formatted_table

    def create_users_data(self):
        users = UserRegistration()
        user_list = users.get_all_registered_users_all_data()
        if len(user_list) == 0:
            user_data_file_path = './userlist'
            users.insert_records_from_csv(user_data_file_path)
        html = "<table><th>UserName</th>"
        user_dict_list=[]
        for user in user_list:
            user_dict = {"UserName":user['name'] ,"Phone Number":user['phonenumber'] ,"Email Address":user['email']}
            user_dict_list.append(user_dict)
            
        data_processed = json.dumps({"user_list" : user_dict_list})
        formatted_table = json2html.convert(json=data_processed)
        print(formatted_table)
        print(user_list)
        return formatted_table

    def run_simulation_of_taxi_location(self):
        users = UserRegistration()
        user_list = users.get_all_registered_users()
        if len(user_list) == 0:
            user_data_file_path = './userlist'
            users.insert_records_from_csv(user_data_file_path)
        html = "<table><th>UserName</th>"
        for user in user_list:
            html = html + f'<tr><td>{user}</td></tr>'
        data_processed = json.dumps(user_list)
        formatted_table = json2html.convert(json=data_processed)
        return formatted_table

    def show_taxi_location_data(self):
        simtaxi = TaxiUserAggregator()
        user_list = simtaxi.get_simulation_data_taxi_from_db()
        if len(user_list) == 0:
            pass
        z = {}
        finaldict = {}
        final_list = []
        i = 0
        for data in user_list:
            locdata = data['location']
            latvalue = locdata['coordinates'][0]
            longvalue = locdata['coordinates'][1]
            longvalue = locdata['coordinates'][1]
            final_list.append({'Txiname': data["name"], 'Timestamp': data["timestamp"] , 'Latitude': latvalue ,'longitude': longvalue})
            print(finaldict)
            i = i + 1
            # print(final_list)
        data_processed = json.dumps(final_list)
        formatted_table = json2html.convert(json=data_processed)
        #print(formatted_table)
       # jsonify(final_list)
        return formatted_table

    def set_location_boudary(self,top_left,top_right,bottom_let,bottom_right):
        definearea = DefineArea()
        area_dict = definearea.define_area(top_left,top_right,bottom_let,bottom_right)
        return  area_dict

    def show_taxi_booked_data(self):
        simtaxi = TaxiUserAggregator()
        user_list = simtaxi.get_confirmed_taxi_bookings()
        if len(user_list) == 0:
            pass
        final_list = []
        i = 0
        for data in user_list:
            final_list.append(
                {'Txinumber': data["taxinumber"], 'UserPhoneNumber': data["userphone"]})
            i = i + 1
        data_processed = json.dumps(final_list)
        formatted_table = json2html.convert(json=data_processed)
        return formatted_table

