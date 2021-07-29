from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
import pprint

PATH = '/Applications/chromedriver'
driver = webdriver.Chrome(PATH)


# Selenium 
#driver.get('https://riverlevels.uk/levels#.YQF7yhNKhQI')

# BeatifulSoup
#source = requests.get('https://riverlevels.uk/levels#.YQF7yhNKhQI').text

#soup = BeautifulSoup(source, 'lxml')

# Array of UK Countys and .no of monitoring stations
Uk_county_stations = ["Bedfordshire (21 monitoring stations)", "Berkshire (63 monitoring stations)", "Bristol (15 monitoring stations)", "Buckinghamshire (47 monitoring stations)", "Cambridgeshire (69 monitoring stations)", "Cheshire (29 monitoring stations)", "Cornwall (99 monitoring stations)", "Cumbria (102 monitoring stations)", "Derbyshire (51 monitoring stations)", "Devon (152 monitoring stations)", "Dorset (81 monitoring stations)", "Durham (34 monitoring stations)", "East Riding of Yorkshire (56 monitoring stations)", "East Sussex (56 monitoring stations)", "Essex (78 monitoring stations)", "Gloucestershire (94 monitoring stations)", "Greater London (161 monitoring stations)", "Greater Manchester (65 monitoring stations)", "Hampshire (125 monitoring stations)", "Herefordshire (19 monitoring stations)", "Hertfordshire (43 monitoring stations)", "Isle of Wight (18 monitoring stations)", "Kent (90 monitoring stations)", "Lancashire (85 monitoring stations)", "Leicestershire (35 monitoring stations)", "Lincolnshire (154 monitoring stations)", "Merseyside (15 monitoring stations)", "Norfolk (78 monitoring stations)", "North Yorkshire (155 monitoring stations)", "Northamptonshire (62 monitoring stations)", "Northumberland (55 monitoring stations)", "Nottinghamshire (28 monitoring stations)", "Oxfordshire (76 monitoring stations)", "Rutland (8 monitoring stations)", "Shropshire (36 monitoring stations)", "Somerset (107 monitoring stations)", "South Yorkshire (56 monitoring stations)", "Staffordshire (50 monitoring stations)", "Suffolk (71 monitoring stations)", "Surrey (81 monitoring stations)", "Tyne & Wear (9 monitoring stations)", "Warwickshire (28 monitoring stations)", "West Glamorgan (20 monitoring stations)", "West Midlands (23 monitoring stations)", "West Sussex (53 monitoring stations)", "West Yorkshire (99 monitoring stations)", "Wiltshire (78 monitoring stations)", "Worcestershire (30 monitoring stations)"]

# Array of Uk Countys
Uk_countys = ["Bedfordshire", "Berkshire", "Bristol", "Buckinghamshire", "Cambridgeshire", "Cheshire", "Cornwall", "Cumbria", "Derbyshire", "Devon", "Dorset", "Durham", "East Riding of Yorkshire", "East Sussex", "Essex", "Gloucestershire", "Greater London", "Greater Manchester", "Hampshire", "Herefordshire", "Hertfordshire", "Isle of Wight", "Kent", "Lancashire", "Leicestershire", "Lincolnshire", "Merseyside", "Norfolk", "North Yorkshire", "Northamptonshire", "Northumberland", "Nottinghamshire", "Oxfordshire", "Rutland", "Shropshire", "Somerset", "South Yorkshire", "Staffordshire", "Suffolk", "Surrey", "Tyne & Wear", "Warwickshire", "West Glamorgan", "West Midlands", "West Sussex", "West Yorkshire", "Wiltshire", "Worcestershire"]

# Dict of UK countys (key) and monitoring staions (value)


UK_river_stations = {}

for i in Uk_countys:
    if ' ' in i:
        i = i.replace(' ', '-')

    driver.get(f'https://riverlevels.uk/levels/{i}') # Opens county page
    twocol = driver.find_element_by_class_name('twocol') #
    links = twocol.find_elements_by_tag_name('a')
    for link in links:
        href = link.get_attribute('href')
        if href is not None:
            pass
            #print(href)
   
    twocol_text = twocol.text

    twocol_text_split = twocol_text.split('\n')

    UK_river_stations[i] = twocol_text_split
    
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(UK_river_stations)
    

    time.sleep(5)

print(UK_river_stations)

"""

# Dictionary of Countys and subsections
Uk_subsections_test = {'Bedfordshire':['Bedford Road Sluice Northampton Automation','Beofrd GS'], 'Berkshire':['Haymills FD', 'Jubilee River at Manor Farm Weir']}

# Scotland 
Scotland_county_stations = ["Aberdeenshire (20 monitoring stations)", "Angus (11 monitoring stations)", "Argyll and Bute (16 monitoring stations)", "Ayrshire and Arran (26 monitoring stations)", "Banffshire (9 monitoring stations)", "Berwickshire (8 monitoring stations)", "Caithness (4 monitoring stations)", "City of Aberdeen (4 monitoring stations)", "City of Dundee (1 monitoring stations)", "City of Edinburgh (7 monitoring stations)", "City of Glasgow (1 monitoring stations)", "Clackmannan (1 monitoring stations)", "Dumfries (19 monitoring stations)", "Dunbartonshire (12 monitoring stations)", "East Lothian (9 monitoring stations)", "Fife (5 monitoring stations)", "Inverness (37 monitoring stations)", "Kincardineshire (7 monitoring stations)", "Lanarkshire (17 monitoring stations)", "Midlothian (2 monitoring stations)", "Moray (9 monitoring stations)", "Nairn (1 monitoring stations)", "Orkney (3 monitoring stations)", "Perth and Kinross (33 monitoring stations)", "Renfrewshire (7 monitoring stations)", "Ross and Cromarty (22 monitoring stations)", "Roxburgh, Ettrick and Lauderdale (22 monitoring stations)", "Shetland (3 monitoring stations)", "Stirling and Falkirk (18 monitoring stations)", "Sutherland (20 monitoring stations)", "The Stewartry of Kirkcudbright (4 monitoring stations)", "Tweeddale (10 monitoring stations)", "West Lothian (2 monitoring stations)", "Western Isles (8 monitoring stations)", "Wigtown (14 monitoring stations)"]

Scotland_countys = ["Aberdeenshire", "Angus", "Argyll and Bute", "Ayrshire and Arran", "Banffshire", "Berwickshire", "Caithness", "City of Aberdeen", "City of Dundee", "City of Edinburgh", "City of Glasgow", "Clackmannan", "Dumfries", "Dunbartonshire", "East Lothian", "Fife", "Inverness", "Kincardineshire", "Lanarkshire", "Midlothian", "Moray", "Nairn", "Orkney", "Perth and Kinross", "Renfrewshire", "Ross and Cromarty", "Roxburgh, Ettrick and Lauderdale", "Shetland", "Stirling and Falkirk", "Sutherland", "The Stewartry of Kirkcudbright", "Tweeddale", "West Lothian", "Western Isles", "Wigtown"]



Scotland_river_stations = {}

for i in Scotland_countys:
    if ' ' in i:
        i = i.replace(' ', '-')

    driver.get(f'https://riverlevels.uk/levels/{i}')
    twocol = driver.find_element_by_class_name('twocol')
    twocol_text = twocol.text

    twocol_text_split = twocol_text.split('\n')

    Scotland_river_stations[i] = twocol_text_split

    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(Scotland_river_stations)

    time.sleep(5)

print(Scotland_river_stations)



# Wales
Wales_county_stations = ["Clwyd (25 monitoring stations)", "Dyfed (70 monitoring stations)", "Gwent (26 monitoring stations)", "Gwynedd (23 monitoring stations)", "Mid Glamorgan (28 monitoring stations)", "Powys (50 monitoring stations)", "South Glamorgan (8 monitoring stations)"]

Wales_countys = ["Clwyd", "Dyfed", "Gwent", "Gwynedd", "Mid Glamorgan", "Powys", "South Glamorgan"]

Wales_river_stations = {}



for i in Wales_countys:
    if ' ' in i:
        i = i.replace(' ', '-')

    driver.get(f'https://riverlevels.uk/levels/{i}')
    twocol = driver.find_element_by_class_name('twocol')
    twocol_text = twocol.text

    twocol_text_split = twocol_text.split('\n')

    Wales_river_stations[i] = twocol_text_split

    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(Wales_river_stations)

    time.sleep(5)

print(Wales_river_stations)

"""