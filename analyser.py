import nltk
import regex as re 
import csv
import sys

from articleinfo import ArticleInfo as artinf

## This actually does the assigning
## The result of this code is passed to the correcter script for manual review
## There is little point in working on this until I get answers 

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
