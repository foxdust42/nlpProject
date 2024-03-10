import warnings
import regex as re 
import csv
import sys
import spacy

from spacy import displacy

import articleinfo
from articleinfo import ArticleInfo as artinf

## This actually does the assigning
## The result of this code is passed to the correcter script for manual review

##
#   -> https://spacy.io/usage
##

'''
Absent answers the following assumptions are made:
• follow the admin. implication chain
• resolve relative time phrases (i.e. today, yesterday, etc.) wrt to post metadata
• accident_datetime_from_url is just article metadata
• vechicle primacy follows order of apperance in text
• the "any_more_..." field is a list
Currenty ureslovable:
• what is the daily/monthly/yearly field?
• what goes in the cause field? 
'''

'''
Lists in round brackets inside
<NA> to denote nulls

Admin. division of Bangladesh:
Division (8) -> District (64) -> Upazilla / Subdistrict (495) -> Council (4573 Village + 329 Town + 11 City = 4913 Total)
Cities appear to be independent of the upazillas?

All admin division = <NA> if accident not in Bangladesh

while Upazilla => District => Division, it is unclear whether to follow this implication or only use what can be drawn from text

should temporal references like "Today" be resolved wrt. to the pub metadata or as <NA> if they don't follow from the text?

• number_of_accidents_occured <1> -> An accident report generally describes one accident? what if the accidents described are on different dates?/ in different locations?
• is_the_accident_data_yearly_monthly_or_daily <D> -> ??
• day_of_the_week_of_the_accident <Friday> -> ✓ 
• exact_location_of_accident <Daroga intersection> -> ✓ appears to be most specific info available (like X intersection, near Y, etc.)
• area_of_accident <Subarnachar> -> ✓ most specific geo. location (like city)
• division_of_accident <NA> -> See note above 
• district_of_accident <Noakhali> -> ↥
• subdistrict_or_upazila_of_accident <Subarnachar> -> ✓ From loc meta if available?
• is_place_of_accident_highway_or_expressway_or_water_or_others <intersection> -> ✓ // Category?, should a list of possible values also be attached to data?
• is_country_bangladesh_or_other_country <Bangledesh> -> ✓ Given in url
• is_type_of_accident_road_accident_or_train_accident_or_waterways_accident_or_plane_accident <road> -> ✓ by vechicle?
• total_number_of_people_killed <2> -> ✓
• total_number_of_people_injured <2> -> ✓
• is_reason_or_cause_for_the_accident_ploughed_or_ram_or_hit_or_collision_or_breakfail_or_others <collision> -> ?? A collision/ram is a type of accident, not a cause.
• primary_vehicle_involved <autorickshaw> -> Which vechicle is primary? secondary?
• secondary_vehicle_involved <truck> -> ↥
• tertiary_vehicle_involved <NA> -> ↥
• any_more_vehicles_involved <NA> -> List? also, ↥
• available_ages_of_the_deceased <(30,2)> -> ✓
• accident_datetime_from_url <20231201 18:48> -> Pub date?; it is in the example, but that's not from the url
'''

def clean_text(raw_text : str) -> str:
    """replaces odd unicode characters appearing in text with their more common counterparts

    Args:
        raw_text (str): raw text

    Returns:
        str: cleaned text
    """
    ## These look similar, but break literally everything
    clean = raw_text.replace('–','-')   # 'En Dash' -> dash
    clean = clean.replace('’', '\'')    # 'right single quotation mark' -> single quote mark/apostrophe
    clean = clean.replace(' ', ' ')     # 'Non braking space' -> space
    
    return clean

## Test lists

assert(len(artinf.list_divisions) == 8)
assert(len(artinf.list_districts) == 64)
assert(len(artinf.list_subdistricts) == 495)

## end test

## load articles
try:
    csvfile = open('articles_test.csv', 'r', newline='')
except OSError:
    print("Failed to open file")
    sys.exit(-1)

input = csv.reader(csvfile, delimiter=';', quoting=csv.QUOTE_ALL, strict=True)

try:
    outfile = open('tagged_unchecked.csv', 'w', newline='')
except OSError:
    print("failed to open file")
    csvfile.close()
    sys.exit(-1)
    
output = csv.writer(outfile, delimiter=';', quoting=csv.QUOTE_ALL, strict=True)
    
try:
    next(input) # skip title row
    line = next(input)
except StopIteration:
    print("Empty file!")
    csvfile.close()
    outfile.close()
    sys.exit(0)
   

## setup the language processor
 
nlp = spacy.load("en_core_web_sm")




date_fail : int = 0
i=0
    
while True:
    """the main program loop
    """
    ## load metadata, nothing fancy
    # url, pub_meta, loc_meta, title, text
    operating_text = clean_text(line[5])
    operating_title = clean_text(line[3])
    
    article = artinf(line[0], line[1], line[2], operating_title, operating_text)
    
    # static logic
    
    """
        The url tells us whether something is from bangladesh
        .../category/Bangladesh/...
        or not
        .../category/World/...
    """
     
    if re.search("^https:\/\/www\.unb\.com\/category\/[Bb]angladesh\/.*", article.url) is None:
        article.is_country_bangladesh_or_other_country = articleinfo.is_bangladesh.other
        article.division_of_accident = artinf.nullstring
        article.district_of_accident = artinf.nullstring
        article.subdistrict_or_upazila_of_accident = artinf.nullstring
    else:
        article.is_country_bangladesh_or_other_country = articleinfo.is_bangladesh.Bangladesh        
    
    # natural language processing
   
    doc = nlp(article.raw_text)
    
    #displacy.serve(doc, style="ent", page=True)
    
    print(article.url)
    
    for ent in doc.ents:
        if ent.label_ == "DATE":
            print(ent.text, ent.label_)
   
    ## weekday
    gen = (ent for ent in doc.ents if ent.label_ == "DATE")
    article.day_of_the_week_of_the_accident = artinf.nullstring
    for ent in gen:
        wd = articleinfo.resolve_weekday_string(ent.text)
        if wd != artinf.nullstring:
            article.day_of_the_week_of_the_accident = wd
            break
        wd = articleinfo.resolve_weekday_date(ent.text)
        if wd != artinf.nullstring:
            article.day_of_the_week_of_the_accident = wd
            break
    # If we're here and still haven't parsed the date, we look for expressions like "yesterday" or "last night", etc.
    if article.day_of_the_week_of_the_accident == artinf.nullstring:
        date_fail += 1
        print(f"Failed to parse weekday for article {i}")
    
    print (article.day_of_the_week_of_the_accident)
    
    
    ##TODO: parese properly
    article.number_of_accidents_occured = -1
    article.is_the_accident_data_yearly_monthly_or_daily = articleinfo.AccidentData.NA
    ## END TODO 
    
    if i == -1:
        sents = list(doc.sents)
        displacy.serve(sents, style="dep", page=True)
        
    
    ## Write result and iterate
    
    output.writerow(article.exportable())
    
    #for string in line:
        #print(string)
    try:
        print("======")
        line = next(input)
        i += 1
        if i >=100: 
            raise StopIteration
    except StopIteration:
        break
        
    
csvfile.close()
outfile.close()

print(f"failed to parse {date_fail} dates")

print("All is done")
