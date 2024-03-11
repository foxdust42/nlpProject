from enum import Enum
from typing import List, Any, Iterable, Dict
import datetime
import regex as re

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
   
    
    def __load_dicts(filename : str, list_divisions : List[str], list_districts : List[str], list_subdistricts: List[str],
                     sub_to_distr : Dict[str, str], distr_to_div: Dict[str, str]):
        f = open(filename, "r")
        line = f.readline()
        curr_div : str = None
        curr_distr : str = None
        
        while line != "":
            if line == "######\n":
                line = f.readline().strip('\n')
                list_divisions.append(line)
                curr_div = line
                line = f.readline()
            elif line == "------\n":
                line = f.readline().strip('\n')
                list_districts.append(line)
                distr_to_div.update({line: curr_div})
                curr_distr = line
                line = f.readline()
            else:
                line = line.strip('\n')
                list_subdistricts.append(line)
                sub_to_distr.update({line: curr_distr})
            
            line = f.readline()
            
    __load_dicts("parsed.txt", list_divisions, list_districts, list_subdistricts, sub_to_distr, distr_to_div)
            
    def __init__(self, url : str, pub_meta : str, loc_meta : str, title : str, raw_text : str) -> None:
        ## metadata
        self.url : str = url
        self.pub_meta : datetime = datetime.datetime.strptime(pub_meta, '%B %d, %Y, %I:%M %p')
        self.loc_meta : str = loc_meta
        self.title : str = title
        self.raw_text : str = raw_text
        
        ## tags
        self.number_of_accidents_occured : int = None
        self.is_the_accident_data_yearly_monthly_or_daily : AccidentData = None
        self.day_of_the_week_of_the_accident : Weekday = None
        self.exact_location_of_accident : str = None
        self.area_of_accident : str = None
        self.division_of_accident : str = None
        self.district_of_accident : str  = None
        self.subdistrict_or_upazila_of_accident : str = None
        self.is_place_of_accident_highway_or_expressway_or_water_or_other : str #TODO: ??? ask ig
        self.is_country_bangladesh_or_other_country : is_bangladesh= None
        self.is_type_of_accident_road_accident_or_train_accident_or_waterways_accident_or_plane_accident : AccidentType
        self.total_number_of_people_killed : int = None
        self.total_number_of_people_injured : int = None
        self.is_reason_or_cause_for_the_accident_ploughed_or_ram_or_hit_or_collision_or_breakfail_or_others : None #TODO: god knows
        self.primary_vehicle_involved : VechicleType = None
        self.secondary_vehicle_involved : VechicleType = None
        self.tertiary_vehicle_involved : VechicleType = None
        self.any_more_vehicles_involved : List[VechicleType] = None
        self.available_ages_of_the_deceased : List[int] = None
        self.accident_datetime_from_url : datetime = None
        
    def exportable(self) -> Iterable[Any]:
        """returns class info in a format ready to export to a csv file

        Returns:
            Iterable[Any]: An array containg class information
        """
        return [self.url, self.pub_meta, self.loc_meta, self.title, self.raw_text, self.number_of_accidents_occured, self.is_the_accident_data_yearly_monthly_or_daily,
                self.day_of_the_week_of_the_accident]

class AccidentData(Enum):
    D = "daily"
    M = "Monthly"
    Y = "Yearly"
    NA = "<NA>"
    
    def __str__(self) -> str:
        return self.value 

class Weekday(Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WENDSDAY = "Wendsday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"
   
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

def resolve_weekday_string(string : str) -> str:
    print("".join(["<", string.lower(), ">"]))
    #if string.lower() in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
    m = re.search("(?<=( )|(^))(monday|tuesday|wednesday|thursday|friday|saturday|sunday)(?=( )|($))", string.lower())
    if m is not None:
        return m.group(0).title()
    else:
        return ArticleInfo.nullstring
    
def resolve_weekday_date(string : str) -> str:
    date : datetime = None
    try:
        date = datetime.datetime.strptime(string, "%B %d, %Y")
        return datetime.datetime.strftime(date, "%A")
    except ValueError:
        date = None
    try:
        date = datetime.datetime.strptime(string, "%d %m %Y")  
        return datetime.datetime.strftime(date, "%A")
    except ValueError:
        date = None
        
    print(f"Warning: invalid date format in: {string}")
    return ArticleInfo.nullstring
            
def resolve_temporal_reference(string : str, date : datetime) -> str:
    """parses temporal references like 'today' or 'yesterday'
    
    Args:
        string (str): reference to resolve
        date (datetime): date to resolve against
        
    Returns:
        str: resolved day of week or ArticleInfo.nullstring
    """
    if re.search("today", string) is not None:
        return datetime.datetime.strftime(date, "%A")
    return ArticleInfo.nullstring