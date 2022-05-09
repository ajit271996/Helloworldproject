from pymongo import MongoClient

class DefineArea:

    def __init__(self):
        self.client = MongoClient("mongodb+srv://admin:admin@cluster0.pgpb7.mongodb.net/test")
        self.db = self.client.TaxiCorp

    def define_area(self, top_left, top_right, bottom_left, bottom_right):
        area = {}
        valid_top_left = self.__validate_lat_log_data(top_left, 'Top Left')
        valid_top_right = self.__validate_lat_log_data(top_right, 'Top Right')
        valid_bottom_left = self.__validate_lat_log_data(bottom_left, 'Bottom Left')
        valid_bottom_right = self.__validate_lat_log_data(bottom_right, 'Bottom Right')
        if not (valid_top_left and valid_top_right and valid_bottom_left and valid_bottom_right):
            print('Target area could not be created as one or more Latitude and Longitude values ranges are Invalid')
            area['top_left'] = []
            area['top_right'] = []
            area['bottom_left'] = []
            area['bottom_right'] = []
        else:
            print('Target area For Latitude and Longitude values ranges are valid')
            area['top_left'] = top_left
            area['top_right'] = top_right
            area['bottom_left'] = bottom_left
            area['bottom_right'] = bottom_right
        self.db.area.insert_one(area)
        return self.get_last_defined_area()
    def __validate_lat_log_data(self ,intlist, strdesc):
        valid_data = True
        if (intlist[0] is None) or (intlist[1] is None):
            valid_data = False
            print(f"{strdesc} : Latitude and Longitude data cannot be Null ")
        if not (self.__is_float(intlist[0]) and self.__is_float(intlist[1])):
            valid_data = False
            print (f"{strdesc} : Latitude and Longitude Ranges should be float Values only Input data was {type(intlist[0])} and {type(intlist[1])} ")
            return valid_data
        if float(intlist[0]) > 90 or float(intlist[0]) < -90:
            print(f"{strdesc} : Latitude Ranges should be within -90 < Lat < 90 only ")
            valid_data = False
        if float(intlist[1]) > 180 or float(intlist[1]) < -180:
            print(f"{strdesc} : Longitude  Ranges should be within -180 < Long < 180 only ")
            valid_data = False
        return valid_data

    def __is_float(self,value):
        try:
            float(value)
            return True
        except:
            return False
        
    def get_last_defined_area(self):
        arealst = self.db.area.find()
        col_count = self.db.area.count_documents({})
        return arealst[col_count -1]
