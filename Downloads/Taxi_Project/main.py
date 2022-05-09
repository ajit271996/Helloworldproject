import sys
from datetime import datetime
import time
import random
import sched
from DefineArea import DefineArea
from FrontEnd import FrontEnd
from SimulateTaxiPosition import SimulateTaxiPosition
from UserRegistration import UserRegistration
from TaxiRegistration import TaxiRegistration
from SimulateUserPosition import SimulateUserPosition
from TaxiUserAggregator import TaxiUserAggregator
from flask import Flask, request, render_template
import json
from json2html import *

taxisim = SimulateTaxiPosition()
taxis = TaxiRegistration()


lst_taxi_location = []
lst_user_location = []
txinum = ''

def publish_taxi_data(publish_int, itn_count, taxilist, area_boundary):
    for itn in range(0, itn_count):
        if itn == 0:
            print("no wait")
        else:
            time.sleep(publish_int)
        try:
            global  lst_user_location
            lst_taxi_location.append(taxisim.taxis_simulation_data(taxilist, area_boundary))
        except KeyboardInterrupt:
            break;


app = Flask(__name__)
gui = FrontEnd()
area_dict = {}

@app.route("/")
def index():
    htmltxt = """<html> 
             <head>
             <title>Taxi Corp Portal</title>
            </head>
            <body>
                   <table>
                   <tr><td>
                   <a href='/setareatemplate' > Define Area </a> 
                   </td></tr>
                   <tr><td>
                   <a href='/newtaxiregister' > Register New Taxi </a> 
                   </td></tr>
                   <tr><td>
                   <a href='/newuserregister' > Register New User </a>
                   </td></tr>
                   <tr><td>
                   <tr><td>
                   <a href='/taxiregister' > Get Registered List of Taxis from database </a> 
                   </td></tr>
                   <tr><td>
                   <a href='/userregister' > Get Registered List of Users from database </a>
                   </td></tr>
                   <tr><td>
                   <a href='/publishtaxidata' > Run  Simuation for Taxi  Location Data </a>
                   </td></tr>
                    <tr><td>
                   <a href='/taxilocations' > Show Taxi Positions on UI </a>
                   </td></tr>
                    <tr><td>
                   <a href='/usersearchtaxi' > Get Nearest Taxi for User and Book Taxi</a>
                   </td></tr>
                    <tr><td>
                   <a href='/gettaibookings' > Display Confirmed Bookings of Taxis </a>
                   </td></tr>
                   </table>
            </body>
            </html>"""
    return htmltxt


@app.route("/taxiregister/")
def show_taxi_data():
    return gui.create_taxis_data()


@app.route("/userregister/")
def show_user_data():
    return gui.create_users_data()

@app.route("/taxilocations/")
def taxi_location_data():
    return gui.show_taxi_location_data()

@app.route("/newuserregister/")
def reg_user_template():
    return render_template('reguser.html')
@app.route("/reguserresults/", methods=['GET', 'POST'])
def reg_user():

    if request.method == 'POST':
        result = request.form
        uname = result['unmae']
        uemail = result['uemail']
        uphone = result['uphone']
        users = UserRegistration()
        status = users.create_user(uname,uemail,uphone)
    return status

@app.route("/newtaxiregister")
def reg_taxi_template():
    return render_template('regtaxi.html')

@app.route("/regtaxiresults", methods=['GET', 'POST'])
def reg_taxi():
    if request.method == 'POST':
        result = request.form
        tname = result['tname']
        tnum = result['tnum']
        ttype = result['ttype']
        tphone = result['tphone']
        taxis = TaxiRegistration()
        status = taxis.create_taxi(tnum,ttype,tname,tphone)
    return status

@app.route("/setareatemplate")
def set_area_template():
    return render_template('definearea.html')
@app.route("/setarearesults", methods=['GET', 'POST'])
def set_area():

    if request.method == 'POST':
        result = request.form
        toplat = result['toplat']
        botlat = result['bottomlat']
        lftlng = result['leftlong']
        rtlng =  result['rightlong']
        TOP_LEFT = [toplat, lftlng]
        TOP_RIGHT = [toplat,rtlng]
        BOTTOM_LEFT = [botlat,lftlng]
        BOTTM_RIGHT = [botlat,rtlng]
        global area_dict
        area_dict = gui.set_location_boudary(TOP_LEFT,TOP_RIGHT,BOTTOM_LEFT,BOTTM_RIGHT)
    return f"Area is defined with data as Top Lat {toplat} , Bottom Lat {botlat} Lef tLong {lftlng} , Right Long{rtlng}"

@app.route('/usersearchtaxi')
def set_user_search():
    return render_template('usersearchtaxi.html')
    

@app.route('/publishtaxidata')
def simulate():
    return render_template('ShowWaiting.html')


@app.route('/publishtaxidatafn', methods=['GET', 'POST'])
def publish_taxi_data_ui():
    if request.method == 'POST':
        result = request.form
        TAXIS_LIST = taxis.get_all_registered_taxis()
        PUBLISH_INTERVAL_SECS = 60
        SIMULATION_LENGTH = 4
        global  area_dict
        print(area_dict)
        publish_taxi_data(PUBLISH_INTERVAL_SECS, SIMULATION_LENGTH, TAXIS_LIST, area_dict)
        users = UserRegistration()
        USER_LIST = users.get_all_registered_users()
        usersim = SimulateUserPosition()
        global lst_user_location
        lst_user_location = usersim.users_simulation_data(USER_LIST, area_dict)
        outcome = f"Published Taxi Simulation data for  every {PUBLISH_INTERVAL_SECS / 60} mins {SIMULATION_LENGTH} times "
    return render_template("done.html", display=outcome)  

@app.route(("/setuserresults") , methods=['GET', 'POST'])
def fecth_user_nearest_taxi():
    if request.method == 'POST':
        result = request.form
        USER_PHONE_NUMBER = result['phone']
        usr_taxi_type = result['txtype']
        print(f"From HTML got input as {usr_taxi_type}")
        agg = TaxiUserAggregator()
        alltime_taxi_loaction = []
        global  lst_taxi_location
        msguser = ''
        for lst_min in lst_taxi_location:
            alltime_taxi_loaction = alltime_taxi_loaction + lst_min
        agg_list = agg.get_nearest_taxi_for_user(alltime_taxi_loaction,lst_user_location,USER_PHONE_NUMBER,usr_taxi_type)
        print(agg_list)
        tlast = len(agg_list) - 1
        nearest_taxi = agg_list[tlast]
        msguser = "*******Customer Location *****" + "<br>" + json2html.convert(json=agg_list[0])
        msguser = msguser +   "*******Taxis within 1 km distance *****" + "<br>"
        for cnt in range(1,tlast-2):
            msguser  = msguser +   "<br>" + json2html.convert(json=agg_list[cnt])
        msguser = msguser +   "*******Nearest Taxi *****" + "<br>" + json2html.convert(json=agg_list[tlast])
        fnres = ""
        if len(agg_list) > 1 :
           if nearest_taxi is not None:
            txinum = nearest_taxi['Nearest TAXI Number']
            fnres = f"<br> Result : Taxi Number  {txinum}  is successfuly booked."
            agg.confirm_user_taxi_booking(txinum, USER_PHONE_NUMBER)
        else:
           fnres = f"No Taxis Were Aavialble for Booking within 1 KM with Taxi Type as {usr_taxi_type}. No taxi is booked "


    return  f"{msguser} {fnres}"


@app.route(("/gettaibookings"))
def get_taxi_bookingdata():
    return gui.show_taxi_booked_data()




# gui.create_taxis_data();
# ################  Defing the Area boundary  #############################

# print('###########  Define the Area bounday ###############################')
#
# print('Please Enter Area Lat Long Data')
# TOP_LAT = input("Area Top  Latitude: ")
# BOTTOM_LAT= input("Area Bottom Latitude: ")
# LEFT_LONG = input("Area Left Latitude: ")
# RIGHT_LONG = input("Area Right Longitude: ")
# TOP_LEFT = [TOP_LAT,LEFT_LONG]
# TOP_RIGHT = [TOP_LAT,RIGHT_LONG]
# BOTTOM_LEFT = [BOTTOM_LAT,LEFT_LONG]
# BOTTM_RIGHT = [BOTTOM_LAT,RIGHT_LONG]
# definearea = DefineArea()
# area_dict = definearea.define_area(TOP_LEFT,TOP_RIGHT,BOTTOM_LEFT,BOTTM_RIGHT)
# print(f"Area Left boundary = {area_dict['top_left']}")
#
# # ################  Perform the User Registration  #############################
# print('###########  Perform the User Registration ###############################')
# USER_DATA_FILE_PATH = './userlist'
# users.insert_records_from_csv(USER_DATA_FILE_PATH)
#
# # ################  Perform the Taxi Registration  #############################
# print('###########  Perform the Taxi Registration ###############################')
# TAXI_DATA_FILE_PATH = './taxilist'
# taxis.insert_records_from_csv(TAXI_DATA_FILE_PATH)
#
# #  ##############  get all reistered taxis from database upto 50  #####################
# TAXIS_LIST = taxis.get_all_registered_taxis()
# #  ##############  get all reistered users from database upto 5  #####################

# PUBLISH_INTERVAL_SECS = 60
# SIMULATION_LENGTH = 2
# usersim = SimulateUserPosition()
# # ################  Simulate  the Taxi Position within the area  #############################
# print(f'################  Simulating   the Taxi Position within the area (every {PUBLISH_INTERVAL_SECS / 60} mins upto desired value: {SIMULATION_LENGTH} #############################')
# publish_taxi_data(PUBLISH_INTERVAL_SECS,SIMULATION_LENGTH,TAXIS_LIST,area_dict)
#
# lst_user_location = usersim.users_simulation_data(USER_LIST,area_dict)
#
#
# print('################  Fetching the Taxi Nearest to the User Location for given user...  #############################')
# USER_PHONE_NUMBER="9768125870"
# agg = TaxiUserAggregator()
# alltime_taxi_loaction = []
# for lst_min in lst_taxi_location:
#     alltime_taxi_loaction = alltime_taxi_loaction + lst_min
#
# print(f"Number of Simulation Data points {len(alltime_taxi_loaction)}")
#
# nearest_taxi = agg.get_nearest_taxi_for_user(alltime_taxi_loaction,lst_user_location,USER_PHONE_NUMBER)
# txinum = nearest_taxi['name']
# agg.confirm_user_taxi_booking(txinum,USER_PHONE_NUMBER)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
