from fileinput import close
import json
import random
from collections import defaultdict

# opens 01_data 
with open("01_Data.json") as f:
  data = json.load(f)


# places the biggest cities in each state 
biggest_cities = [] 
# places new sorted list of cities by population
sorted_data = []
d = defaultdict(dict)
# sorts the data by population
sorted_data = sorted(data, key= lambda x: x['population'], reverse=True)




# used to filter out states we need 
# also appends biggest cities in each state to add to a new json file to be used for later in the program
us_states = ['Alabama', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Washington DC', 'Delaware', 'Florida', 'Georgia',  'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
temp=[] # temp list to make sure that we don't visit the same state again
for i in sorted_data:
  for x in us_states:
    if i["state"] == x and i["state"] not in temp:
      temp.append(i["state"])
      biggest_cities.append(i)
      break

for i in biggest_cities:
    d[i["state"]].update(i)
        


# created a new json with data of biggest city of each state 
with open("sorted.json",'w') as output_file:
  json.dump(list(d.values()), output_file, indent=4)

# opens new json 
with open("sorted.json") as f:
  filter_data = json.load(f)




close_cities_data = []
#sorts the states by closest 
n = defaultdict(dict)
close_cities_data = sorted(filter_data, key= lambda x: x['longitude'], reverse=True)
# add the rank for each city
rank = 1
for item in close_cities_data:
    item['rank'] = rank
    rank +=1



for i in close_cities_data:
    n[i["state"]].update(i)

        

with open("new.json",'w') as output_file:
  json.dump(list(n.values()), output_file, indent=4)


# opens newnew json 
with open("new.json") as f:
  legit_data= json.load(f)

# makes random colors hex
# error colors need to have 6 hex codes
def randColor():
    color = '#{:02x}{:02x}{:02x}'.format(*map(lambda x: random.randint(0, 255), range(3)))
    return color
  


FeatureCollection = {}
FeatureCollection["type"] = "FeatureCollection"
FeatureCollection["features"] = []


def makePoint(city):
  feature = {
    "type": "Feature",
    "properties": {
      "marker-color":randColor(),
      "marker-symbol": [0]
    },
    "geometry": {
      "type": "Point",
      "coordinates": [0,0]
    }
  }

  # print(dir(city.items()))
  for key,val in city.items():
    if key == 'latitude':
      feature['geometry']['coordinates'][1] = val
    elif key == 'longitude':
      feature['geometry']['coordinates'][0] = val
 
    elif key == 'rank':
      feature['properties']['marker-symbol'][0] = val
    
    else:
      feature['properties'][key] = val
  return feature


def makeLineString(leftside):
    feature = {
      "type": "Feature",
      "properties": {
        "color":randColor(),
      },
      "geometry": {
        "type": "LineString",
        "coordinates": 
        
          leftSide
        
      }
    }
    return feature
    



# creates the lines for each state based on the rank
# the lines draws by long and lat of each city 
g = legit_data
leftSide = []

for i in range(len(legit_data)-1):   
     leftSide.append( [legit_data[i]["longitude"], legit_data[i]["latitude"]])
     leftSide.append([legit_data[i+1]["longitude"], legit_data[i+1]["latitude"]])
    

points = []
for stateInfo in legit_data:
    FeatureCollection["features"].append(makePoint(stateInfo))
 

linestring = []
FeatureCollection["features"].append(makeLineString(leftSide))


with open("new.geojson","w") as f:
  json.dump(FeatureCollection,f,indent=4)
