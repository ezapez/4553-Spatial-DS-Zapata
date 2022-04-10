from operator import length_hint
from pickletools import long1
from textwrap import indent
import pandas as pd
import csv
import json
from shapely.geometry import Point
import geopandas 
from rich import print 
from math import radians, cos, sin, asin,tan, atan,sqrt


# ufo data set to global
gs = None
df = None
ufoPoints = []


# brute force method to calulate all the distance fir cities
def haversineDistance(lon1, lat1, lon2, lat2, units="miles"):
    """Calculate the great circle distance in kilometers between two points on the earth (start and end) where each point
        is specified in decimal degrees.
    Params:
        lon1  (float)  : decimel degrees longitude of start (x value)
        lat1  (float)  : decimel degrees latitude of start (y value)
        lon2  (float)  : decimel degrees longitude of end (x value)
        lat3  (float)  : decimel degrees latitude of end (y value)
        units (string) : miles or km depending on what you want the answer to be in
    Returns:
        distance (float) : distance in whichever units chosen
    """
    radius = {"km": 6371, "miles": 3956}

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = radius[units]  # choose miles or km for results
    return c * r

#makes json file for new data
def makePointsList():
  # adding the points using geopandas
  # taking from Prof G example in P02
  f = open('cities.geojson')
  data = json.load(f)
  
  # this will be used to list each city in a new json to find the distance of each other city by points
  cities = []
  for feature in data["features"]:
      if feature["properties"]:
          cities.append({
            "city":feature["properties"]["city"],
            "state":feature["properties"]["state"],
            "point":feature["geometry"]["coordinates"],
            "distances":[],
            "ufos":[]
          })

  return cities

#function to calculate city distance
def calcCityDistances(cities):
  for i in range(len(cities)):
      lon1,lat1 = cities[i]['point']
      for j in range(len(cities)):
        lon2,lat2 = cities[j]['point']
        cities[i]['distances'].append(haversineDistance(lon1, lat1, lon2, lat2))
  return cities









# write to new json
def saveJson(data,name):
  with open(name,"w") as f:
    f.write(json.dumps(data,indent=2))





# loading ufos 
def loadUfos():
  global df
  df = pd.read_csv('ufo.csv')

# making ufos into points to be used for another function
def loadUfoIndex():
  global gs
  global df
  for index, row in df.iterrows():
    p = Point(row['lon'],row['lat'])
    ufoPoints.append(p)
    
  gs = geopandas.GeoSeries(ufoPoints)
  

# function to make a list of cities points 
def cities_points():
  city_points = []
  for i in range(len(cities)):
      lon1,lat1 = cities[i]['point']
      pointslist = lon1, lat1
      city_points.append(pointslist)
  return city_points




#function to find the closest ufos for each city
def findClosestUfos(city_point):
  global gs

  closestUfos = []
  
  for i in range(len(city_point)):
    
    cp = Point(city_point[i])
    distances = gs.distance(cp)
    

    sortedDistance = []
    for i in range(len(distances)):
      sortedDistance.append((i,distances[i]))
    sortedDistance.sort(key = lambda x: x[1]) 

    close_ufos = sortedDistance[0:100]
    closestUfos.append(close_ufos)
  


  for  j in range(len(cities)):
    cities[j]["ufos"].append(closestUfos[j])
    
  return cities

  


     
 
  

  



def driver():
  pass


if __name__=='__main__':

  cities = makePointsList()
  cities = calcCityDistances(cities)
  loadUfos()
  loadUfoIndex()
  citys = cities_points()
  cities = findClosestUfos(citys)
  saveJson(cities,"distance_cities.json")
