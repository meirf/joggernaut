import xml.etree.cElementTree as et
from collections import defaultdict
from math import radians, cos, sin, asin, sqrt
import json
import urllib2

def get_coordinates():
    sxml = ''.join(open("/Users/meirfischer/Dropbox/django_tut/mysite/jogger/graph_preparation/mwap_a.kml").readlines())
    tree = et.fromstring(sxml)
    coordinates = []

    for el in tree.findall('Placemark'):
        for ch in el.getchildren():
            for gc in ch.getchildren():
                if gc.tag == "coordinates":
                    if len(coordinates)==42:
                        coordinates.append(None)
                    coordinates.append(tuple(float(s) for s in gc.text.split(',')[:2]))

    return coordinates

def get_all_elevations():
    coords = get_coordinates()
    #elevs = []
    elevs = [8.772932052612305, 8.630032539367676, 8.481337547302246, 8.473003387451172, 8.605457305908203, 8.851371765136719, 9.326964378356934, 9.620454788208008, 10.08272743225098, 11.16177463531494, 11.96563720703125, 12.13568782806396, 12.42085742950439, 12.87494850158691, 8.372590065002441, 8.12594985961914, 8.07753849029541, 8.126249313354492, 8.17297649383545, 8.269344329833984, 8.467561721801758, 8.599291801452637, 8.693227767944336, 9.083831787109375, 9.349800109863281, 9.437838554382324, 9.580528259277344, 9.914894104003906, 8.121710777282715, 7.835072040557861, 7.691619873046875, 7.598601818084717, 7.615684509277344, 7.728802680969238, 7.702752113342285, 7.725890636444092, 7.606010437011719, 7.569760322570801, 7.693739414215088, 7.730432987213135, 7.644207000732422, 7.592205047607422, None, 7.205403804779053, 7.732362747192383, 8.290694236755371, 7.37311649323, 7.17826652527, 6.80265760422, 6.78662490845, 7.14887714386, 8.43306159973, 8.35956192017, 8.1632232666, 7.93828582764, 7.62221002579, 7.09258747101, 5.68282175064, 7.37508964539]
    #for i,c in enumerate(coords):
    #    if c is None:
    #        elevs.append(None)
    #    else:
    #        elevs.append(get_elevation(c))
    return elevs

def get_elevation(coord_pair_long_lat):
    commad_coords = str(coord_pair_long_lat[1])+","+str(coord_pair_long_lat[0])
    api_str = "http://maps.googleapis.com/maps/api/elevation/json?locations="+commad_coords+"&sensor=false"
    data = json.load(urllib2.urlopen(api_str))
    try:
        return data["results"][0]["elevation"]
    except IndexError:
        print data["status"]

# key: node id, value: [(nodeid_neighbor, distance), (), ...]
def get_adj_list():
    coords = get_coordinates()
    neighbors = defaultdict(list)
    for i in range(28):
        neighbors[i].append(i+14)
        if i>13:
            neighbors[i].append(i-14)
        if i%14==0:
            neighbors[i].append(i+1)
        elif i%14==13:
            neighbors[i].append(i-1)
        else:
            neighbors[i].extend([i-1, i+1])
    for i in range(28, 42):
        neighbors[i].append(i-14)
        if i%14==0:
            neighbors[i].append(i+1)
        elif i%14==13:
            neighbors[i].append(i-1)
        else:
            neighbors[i].extend([i-1, i+1])
        if i < 30:
            neighbors[i].append(i+15)            
        elif i < 35:
            neighbors[i].append(i+16)
        elif i < 40:
            neighbors[i].append(i+17)
        if i==41:
            neighbors[i].append(58)
    for i in range(43, 58):
        neighbors[i].append(i+1)
        if i!=43:
            neighbors[i].append(i-1)
        if i<45:
            neighbors[i].append(i-15)
        if i<51 and i>45:
            neighbors[i].append(i-16)
        if i>51 and i<57:
            neighbors[i].append(i-17)
    neighbors[58].extend([41, 57])
    for node_id in neighbors:
        for j,neighbor in enumerate(neighbors[node_id]):
            dist = get_haversine(coords[node_id], coords[neighbor])
            neighbors[node_id][j] = (neighbor, dist)
    return neighbors

def get_haversine(coord_pair_a, coord_pair_b):
    # convert decimal degrees to radians 
    lon1 = coord_pair_a[0]
    lat1 = coord_pair_a[1]
    lon2 = coord_pair_b[0]
    lat2 = coord_pair_b[1]
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km * 1000

if __name__ == "__main__":
    elevs = get_all_elevations()
    for i,e in enumerate(elevs):
        print i
        print e
    coords = get_coordinates()
    for i,e in enumerate(coords):
        print i
        print e
    adj_list = get_adj_list()
    for k,v in adj_list.items():
        print k
        print v