from enum import Enum
from typing import List, Any, Iterable, Dict
import datetime
import regex as re
import spacy
from spacy import tokens
from word2number import w2n
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
        self.pub_meta : datetime = None
        try:
            self.pub_meta = datetime.datetime.strptime(pub_meta, '%B %d, %Y, %I:%M %p')
        except ValueError:
            pass
        self.loc_meta : str = loc_meta
        self.title : str = title
        self.raw_text : str = raw_text
        
        ## tags
        self.number_of_accidents_occured : int = None
        self.is_the_accident_data_yearly_monthly_or_daily : AccidentData = None
        self.day_of_the_week_of_the_accident : str = None
        self.exact_location_of_accident : str = None
        self.area_of_accident : str = None
        self.division_of_accident : str = None
        self.district_of_accident : str = None
        self.subdistrict_or_upazila_of_accident : str = None
        self.is_place_of_accident_highway_or_expressway_or_water_or_other : str = None #TODO: ??? ask ig
        self.is_country_bangladesh_or_other_country : is_bangladesh= None
        self.is_type_of_accident_road_accident_or_train_accident_or_waterways_accident_or_plane_accident : AccidentType = AccidentType.NA
        self.total_number_of_people_killed : int = None
        self.total_number_of_people_injured : int = None
        self.is_reason_or_cause_for_the_accident_ploughed_or_ram_or_hit_or_collision_or_breakfail_or_others : str = None #TODO: god knows
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
        return [self.url, self.pub_meta, self.loc_meta, self.title, self.raw_text, self.number_of_accidents_occured,
                self.is_the_accident_data_yearly_monthly_or_daily, self.day_of_the_week_of_the_accident,
                self.exact_location_of_accident, self.area_of_accident, self.division_of_accident,
                self.district_of_accident, self.subdistrict_or_upazila_of_accident,
                self.is_place_of_accident_highway_or_expressway_or_water_or_other,
                self.is_country_bangladesh_or_other_country, self.is_type_of_accident_road_accident_or_train_accident_or_waterways_accident_or_plane_accident,
                self.total_number_of_people_killed, self.total_number_of_people_injured,
                self.is_reason_or_cause_for_the_accident_ploughed_or_ram_or_hit_or_collision_or_breakfail_or_others,
                self.primary_vehicle_involved, self.secondary_vehicle_involved, self.tertiary_vehicle_involved,
                self.any_more_vehicles_involved, self.available_ages_of_the_deceased,
                self.accident_datetime_from_url]
    @classmethod 
    def title_row(cls) -> Iterable[str]: 
        return ["url",
        "pub_meta",
        "loc_meta",
        "title",
        "raw_text",
        "number_of_accidents_occured",
        "is_the_accident_data_yearly_monthly_or_daily",
        "day_of_the_week_of_the_accident",
        "exact_location_of_accident",
        "area_of_accident",
        "division_of_accident",
        "district_of_accident",
        "subdistrict_or_upazila_of_accident",
        "is_place_of_accident_highway_or_expressway_or_water_or_other",
        "is_country_bangladesh_or_other_country",
        "is_type_of_accident_road_accident_or_train_accident_or_waterways_accident_or_plane_accident",
        "total_number_of_people_killed",
        "total_number_of_people_injured",
        "is_reason_or_cause_for_the_accident_ploughed_or_ram_or_hit_or_collision_or_breakfail_or_others",
        "primary_vehicle_involved",
        "secondary_vehicle_involved",
        "tertiary_vehicle_involved",
        "any_more_vehicles_involved",
        "available_ages_of_the_deceased",
        "accident_datetime_from_url"]

    def setdate(self, date : datetime.datetime):
        self.pub_meta = date
        

def GenericArticle() -> ArticleInfo:
    ga : ArticleInfo = ArticleInfo("https://example.com", "March 18, 2022, 03:03 PM", "Generic city", "Title", "<<<<<TEXT>>>>>")
    if ga.pub_meta is None:
        ga.setdate(datetime.datetime(2022, 2, 2, 11, 22))
    
 
    ga.number_of_accidents_occured = 1 
    ga.is_the_accident_data_yearly_monthly_or_daily = AccidentData.D
    ga.day_of_the_week_of_the_accident = "Monday"
    ga.exact_location_of_accident = "Location"
    ga.area_of_accident = "Generic Intersection"
    ga.division_of_accident = "Div"
    ga.district_of_accident = "Dis"
    ga.subdistrict_or_upazila_of_accident = "Sub" 
    ga.is_place_of_accident_highway_or_expressway_or_water_or_other = "Highway"
    ga.is_country_bangladesh_or_other_country = is_bangladesh.Bangladesh
    ga.is_type_of_accident_road_accident_or_train_accident_or_waterways_accident_or_plane_accident = "road" 
    ga.total_number_of_people_killed = 2
    ga.total_number_of_people_injured = 5
    ga.is_reason_or_cause_for_the_accident_ploughed_or_ram_or_hit_or_collision_or_breakfail_or_others = "collision"
    ga.primary_vehicle_involved = "Truck"
    ga.secondary_vehicle_involved = "Pedestrian"
    ga.tertiary_vehicle_involved = "Oil tanker"
    ga.any_more_vehicles_involved = ["A", "B"]
    ga.available_ages_of_the_deceased = [1, 2, 3]
    ga.accident_datetime_from_url = ga.pub_meta
    
    return ga

def artinfo_from_list(args : List[str]) -> ArticleInfo:
    pass 

class AccidentData(Enum):
    D = "Daily"
    M = "Monthly"
    Y = "Yearly"
    NA = "<NA>"
    
    def __str__(self) -> str:
        return self.value 

class AccidentType(Enum):
    """Enum for different accident types

    As some accidents are truly intermodal, an order must be established among them, that is:
    
    Plane >
    Train >
    Water >
    Road  >
    Other
    
    i.e.: if a train crashes into an oil tanker, then,
    so long as the train was an operated vechicle as opposed to cargo,
    the accident will be classified as a train accident.
    
    Likewise, a car driving into an oil tanker would be a water accident.
    """
    
    TRAIN = "Train"
    WATER = "Waterway"
    PLANE = "Plane"
    ROAD = "Road"
    OTHER = "Other"
    NA = ArticleInfo.nullstring
    
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
    NA = "<NA>"
    
    def __str__(self) -> str:
        return self.value
   
class is_bangladesh(Enum):
    other = "Ohter"
    Bangladesh = "Bangladesh"
    
    def __str__(self) -> str:
        return self.value
    
class VechicleType(Enum):
    Bus = "Bus"
    Car = "Car"
    Noah = "Noah"
    Human_hauler  = "Human hauler"
    Trolley = "Trolley"
    Chander_Gari  = "Chander Gari"
    Auto_Rickshaw = "Auto Rickshaw"
    CNG = "CNG"
    Easy_Bike = "Easy-bike"
    Truck = "Truck"
    Garbage_Truck  = "Garbage Truck"
    Trailer = "Trailer"
    Motorcycle = "Motorcycle"
    Microbus = "Microbus"
    Scooter = "Scooter"
    Construction_vehicle = "Construction vehicle"
    Bicycle = "Bicycle"
    Ambulance = "Ambulance"
    Pickup = "Pickup"
    Lorry = "Lorry"
    Paddy_Cutter_Vechicles = "Paddy cutter vehicles"
    Bulkhead = "Bulkhead"
    Crane = "Crane"
    Wrecker = "Wrecker"
    Tractor = "Tractor"
    Cart = "Cart"
    Leguna = "Leguna"
    Nosimon = "Nosimon"
    Three_Wheeler = "Three-Wheeler"
    Four_Wheeler = "Four-Wheeler"
    Votvoti = "Votvoti"
    Kariman = "Kariman"
    Mahindra = "Mahindra"
    Van = "Van"
    Rickshaw = "Rickshaw"
    Boat = "Boat"
    Trawler = "Trawler"
    Vessel = "Vessel"
    Launch = "Launch"
    Tanker = "Tanker"
    Oil_Tanker = "Oil Tanker"
    Road_roller = "Road roller"
    Power_Tiller = "Power Tiller"
    Excavator = "Excavator"
    Train = "Train"
    Airplane = "Airplane"
    Pedestrian = "Pedestrian"
    Other = "Other"
    NA = ArticleInfo.nullstring

    def __str__(self) -> str:
        return self.value
        


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
    if re.search("yesterday|last (night|morning|afternoon)", string) is not None:
        return datetime.datetime.strftime((date - datetime.timedelta(days=1)), "%A")
    return ArticleInfo.nullstring

def parse_dead_and_injured(doc : tokens.Doc)-> tuple[int, int]:
    """parses text for deaths and injuries

    Args:
        doc (tokens.Doc): spacy document object

    Returns:
        tuple[int, int]: tuple containing deaths and injuries, in that order
    """
    kill_count : int = 0
    kill_flag : bool = False
    wound_count : int = 0
    wound_flag : bool = False
    for chunk in doc.noun_chunks:
        #print(chunk.text, chunk.root.text, chunk.root.dep_, chunk.root.head.text, chunk.root.head.lemma_)
        if chunk.root.head.lemma_ in ["kill", "die"]:
            print(chunk.text, chunk.root.text, chunk.root.dep_, chunk.root.head.text, chunk.root.head.lemma_)
            #for ent in chunk.ents:
            #    print("E:", ent.text, ent.label_)
            for token in chunk.subtree:
                print("T:", token.text)
                if (token.pos_ in "PROPN" or token.tag_ == "NN") and token.dep_ in ["nsubjpass", "nsubj"]:
                    kill_count += 1
                if token.pos_ == "NUM" and token.dep_ in ["nummod"]:
                    # print(token.text, token.pos_, w2n.word_to_num(token.text))
                    kill_count += w2n.word_to_num(token.text) 
        if chunk.root.head.lemma_ in ["injure", "wound"]:
            for token in chunk.subtree:
                if token.pos_ == "PROPN" or (token.tag_ == "NN" and token.dep_ in ["nsubjpass", "nsubj"]):
                    wound_count += 1
                if token.pos_ == "NUM" and token.dep_ in ["nummod"]:
                    # print(token.text, token.pos_, w2n.word_to_num(token.text))
                    wound_count += w2n.word_to_num(token.text) 
        if chunk.root.head.lemma_ in ["sustain"]:
            loc_f : bool = False
            for token in chunk.root.head.subtree:
                # print(token.lemma_)
                if token.lemma_ in ["wound", "injury"]:
                    loc_f = True
                    break;
            if loc_f == False:
                continue
            for token in chunk.subtree:
                if token.pos_ == "PROPN" or (token.tag_ == "NN" and token.dep_ in ["nsubjpass", "nsubj"]):
                    wound_count += 1
                if token.pos_ == "NUM" and token.dep_ in ["nummod"]:
                    #print(token.text, token.pos_, w2n.word_to_num(token.text))
                    wound_count += w2n.word_to_num(token.text) 
                    
    return (kill_count, wound_count)
