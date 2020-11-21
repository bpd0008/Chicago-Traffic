# Code to take user input and then code it in our dummy variable array
import pandas as pd
import json
import os
import numpy
import sys
from collections import namedtuple
from math import log,tan,pi,radians

# This code has been derived and then adopted from
# https://github.com/jkgiesler/parse-chicago-neighborhoods/blob/master/gps_to_neighborhood.py

def load_json():
    file_in = open(os.getcwd()+"/static/data/Neighborhoods_2012_polygons.json")
    d = json.load(file_in)
    return d

Pt = namedtuple('Pt','x,y')
Edge = namedtuple('Edge','a,b')
Poly = namedtuple('Poly','name,edges')
_eps = 1e-5
_huge = sys.float_info.max
_tiny = sys.float_info.min

def spherical_mercator_projection(longitude,latitude):
    x = -longitude
    y = log(tan(radians(pi/4 + latitude/2)))
    return (x,y)

def rayintersectseg(p, edge):
    a, b = edge
    if a.y > b.y:
        a, b = b, a
    if p.y == a.y or p.y == b.y:
        p = Pt(p.x, p.y + _eps)
    intersect = False

    if (p.y > b.y or p.y < a.y) or (
            p.x > max(a.x, b.x)):
        return False

    if p.x < min(a.x, b.x):
        intersect = True
    else:
        if abs(a.x - b.x) > _tiny:
            m_red = (b.y - a.y) / float(b.x - a.x)
        else:
            m_red = _huge
        if abs(a.x - p.x) > _tiny:
            m_blue = (p.y - a.y) / float(p.x - a.x)
        else:
            m_blue = _huge

        intersect = m_blue >= m_red
    return intersect

def is_odd(x):
    return x%2 == 1

def ispointinside(p, poly):
    ln = len(poly)
    return is_odd(sum(rayintersectseg(p, edge)
                    for edge in poly.edges ))

def get_all_neighborhoods():
    d = load_json()
    shape_list=[]
    for shape_idx in range(len(d['features'])):
        name = d['features'][shape_idx]['properties']['SEC_NEIGH']

        edges =[]
        for coordinate_idx in range(len(d['features'][shape_idx]['geometry']['coordinates'][0])-1):
            lon_1 = d['features'][shape_idx]['geometry']['coordinates'][0][coordinate_idx][0]
            lat_1 = d['features'][shape_idx]['geometry']['coordinates'][0][coordinate_idx][1]

            lon_2 = d['features'][shape_idx]['geometry']['coordinates'][0][coordinate_idx+1][0]
            lat_2 = d['features'][shape_idx]['geometry']['coordinates'][0][coordinate_idx+1][1]

            x1,y1 = spherical_mercator_projection(lon_1,lat_1)
            x2,y2 = spherical_mercator_projection(lon_2,lat_2)
            edges.append(Edge(a=Pt(x=x1,y=y1),b=Pt(x=x2,y=y2)))

        shape_list.append(Poly(name=name,edges=tuple(edges)))
    return shape_list

def find_neighborhood(test_long,test_lat,all_neighborhoods):
    x,y = spherical_mercator_projection(test_long,test_lat)
    for neighborhood in all_neighborhoods:
        correct_neighborhood = ispointinside(Pt(x=x,y=y),neighborhood)
        if correct_neighborhood:
            return neighborhood.name

all_neighborhoods = get_all_neighborhoods()

def get_neighborhood(long, lat):
    test_long = float(long)
    test_lat = float(lat)
    return find_neighborhood(test_long, test_lat, all_neighborhoods)