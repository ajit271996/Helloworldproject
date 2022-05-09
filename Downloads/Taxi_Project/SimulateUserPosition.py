from datetime import datetime
import time
import random
import sched
from pymongo import MongoClient


class SimulateUserPosition:
    def __init__(self):
        self.message = {}
        self.client = MongoClient("mongodb+srv://admin:admin@cluster0.pgpb7.mongodb.net/test")
        self.db = self.client.TaxiCorp

    def __get_user_location(self,area_boundary):
        pos = []
        tl = area_boundary['top_left']
        br = area_boundary['bottom_right']
        lat_variate = random.uniform(float(tl[0]), float(br[0]))
        lng_variate = random.uniform(float(br[1]), float(tl[1]))
        pos.append(lat_variate)
        pos.append(lng_variate)
        return  pos

    def users_simulation_data(self, userlist, area_boundary):
        user_list = []
        print(self.__get_user_location(area_boundary))
        for user in userlist:
            lat_posn = self.__get_user_location(area_boundary)[0]
            lng_posn = self.__get_user_location(area_boundary)[1]
            message = {"name": str(user),
                       'location': {
                           'type': "Point",
                           'coordinates': [lng_posn,lat_posn]
                       },
                       "timestamp": str(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
                       }
            # self.__insert_Taxi_location_to_db(message)
            user_list.append(message)
        print(user_list)
        return  user_list


    def __publish_user_data(self,publish_int,userlist, area_boundary):
        loopCount = 0
        scheduler = sched.scheduler(time.time, time.sleep)
        now = time.time()
        while True:
            try:
                scheduler.enterabs(now + loopCount, 1, self.users_simulation_data(), argument=(userlist,area_boundary))
                loopCount += int(publish_int)
                scheduler.run()
            except KeyboardInterrupt:
                break
    def __insert_User_location_to_db(self,messagedict):
        self.message = messagedict
        print(f"Trying to  Insert User location  data {self.message}")
        result = self.db.taxilocationdata.insert_one(self.message)
        print(f"Successfully Inserted Taxi  data {self.message} -- id {result}")





