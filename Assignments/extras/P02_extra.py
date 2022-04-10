from operator import length_hint
from pickletools import long1
from textwrap import indent
from sklearn.neighbors import NearestNeighbors
import numpy as np
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
            "ufos":[]
          })

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
    # distances = gs.distance(cp)
    x = cp
    nbrs = NearestNeighbors(n_neighbors=100,algorithm='ball_tree').fit(x)
    print(nbrs)
    sortedDistance = []
    # for i in range(len(city_point)):
    

      # for i in range(len(distances)):
      #   sortedDistance.append((i,distances[i]))
      #   sortedDistance.sort(key = lambda x: x[1]) 


    # close_ufos = sortedDistance[0:100]    
    # closestUfos.append(close_ufos)
    

    


  # for  j in range(len(cities)):
  #   cities[j]["ufos"].append(closestUfos[j])
    
  # return cities

  


     
 
  

  



def driver():
  pass


if __name__=='__main__':

  cities = makePointsList()
  loadUfos()
  loadUfoIndex()
  citys = cities_points()
  cities = findClosestUfos(citys)
  saveJson(cities,"distance_cities.json")
 