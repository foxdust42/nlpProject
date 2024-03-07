from enum import Enum
from typing import List, Any, Iterable
import datetime

class ArticleInfo:
    """Class for hadling article information
    """
    
    loaded : bool = False
    
    nullstring : str = "<NA>"
    
    list_divisions = []
    list_districts = []
    list_subdistricts = []
    
    sub_to_distr = {}
    distr_to_div = {}
    
    def __load_dicts(filename : str):
        f = open(filename, "r")
        line = f.readline()
        curr_div : str = None
        curr_distr : str = None
        
        while line != "":
            if line == "######":
                line = f.readline()
                ArticleInfo.list_divisions.append(line)
                curr_div = line
                line = f.readline()
            elif line == "------":
                line = f.readline()
                ArticleInfo.list_districts.append(line)
                ArticleInfo.distr_to_div.update({line: curr_div})
                curr_distr = line
                line = f.readline()
            else:
                ArticleInfo.list_subdistricts.append(line)
                ArticleInfo.sub_to_distr.update({line: curr_distr})
            
            line = f.readline()
            
    __load_dicts()
            
    def __init__(self, url : str, pub_meta : str, loc_meta : str, title : str, raw_text : str) -> None:
        ## metadata
        self.url : str = url
        self.pub_meta : datetime = datetime.datetime.strptime(pub_meta, '%B %d, %Y, %I:%M %p')
        self.loc_meta : str = loc_meta
        self.title : str = title
        self.raw_text : str = raw_text
        
        ## tags
        self.number_of_accidents_occured : int
        self.is_the_accident_data_yearly_monthly_or_daily : AccidentData
        self.day_of_the_week_of_the_accident : Weekday
        self.exact_location_of_accident : str
        self.area_of_accident : str
        self.division_of_accident : Division
        self.district_of_accident : str #TODO: figure out an enum?
        self.subdistrict_or_upazila_of_accident : str #TODO: as above
        self.is_place_of_accident_highway_or_expressway_or_water_or_other : str #TODO: ??? ask ig
        self.is_country_bangladesh_or_other_country : is_bangladesh
        self.is_type_of_accident_road_accident_or_train_accident_or_waterways_accident_or_plane_accident : AccidentType
        self.total_number_of_people_killed : int
        self.total_number_of_people_injured : int
        self.is_reason_or_cause_for_the_accident_ploughed_or_ram_or_hit_or_collision_or_breakfail_or_others : None #TODO: god knows
        self.primary_vehicle_involved : VechicleType
        self.secondary_vehicle_involved : VechicleType
        self.tertiary_vehicle_involved : VechicleType
        self.any_more_vehicles_involved : List[VechicleType]
        self.available_ages_of_the_deceased : List[int]
        self.accident_datetime_from_url : datetime
        
    def exportable(self) -> Iterable[Any]:
        """returns class info in a format ready to export to a csv file

        Returns:
            Iterable[Any]: An array containg class information
        """
        return [self.url, self.pub_meta, self.loc_meta, self.title, self.raw_text]

class AccidentData(Enum):
    D = "daily"
    M = "Monthly"
    Y = "Yearly"

class Weekday(Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WENDSDAY = "Wendsday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"
   
class Division(Enum):
    NA = 0
    Barishal = 1
    Chattogram = 2
    Dhaka = 3
    Khulna = 4
    Rajshahi = 5
    Rangpur = 6
    Mymensingh = 7
    Sylhet = 8
    
class is_bangladesh(Enum):
    other = 0
    Bangladesh = 1
    
class AccidentType(Enum):
    NA = 0
    Road = 1
    Train = 2
    Waterways = 3
    Plane = 4
    Ohter = 5
    
class VechicleType(Enum):
    pass

