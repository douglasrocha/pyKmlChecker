import MySQLdb
from os import listdir
from xml.etree import ElementTree

import keytree
from shapely.geometry import Point, shape

kmls = listdir("./kml/")
kml_count = []

for x in kmls:
    kml_count.append([x, 0])


#MySQL queries
db = MySQLdb.Connect(host='localhost',
                     user='root',
                     passwd='root',
                     db='mydatabase')

cur = db.cursor()
cur.execute("SELECT LATITUDE, LONGITUDE FROM bus WHERE LINHA=570.0")

list570 = []

for row in cur.fetchall():
    list570.append([row[0], row[1]])

cur.execute("SELECT LATITUDE, LONGITUDE FROM bus WHERE LINHA=583.0")

list583 = []

for row in cur.fetchall():
    list583.append([row[0], row[1]])

db.close()

# Reads all kml files to strings' list
kml_strings = []

for x in kml_count:
    myfile = open("./kml/" + x[0], 'r')
    kml_strings.append(myfile.read())
    myfile.close()

#Parse the KML doc
for i in range(0, len(kml_strings)):
    doc = kml_strings[i]
    curr_file = kml_count[i]

    print str(i) + " out of " + str(len(kml_strings)) + "(" + curr_file[0] + ")"

    tree = ElementTree.fromstring(doc)
    kmlns = tree.tag.split('}')[0][1:]

    # Find all Polygon elements anywhere in the doc
    elems = tree.findall(".//{%s}Polygon" % kmlns)

    for i in range(0, len(list570)):
        x = list570[i]

        if i % 1000 == 0:
            print str(i) + " out of " + str(len(list570))

        # Here's our poin of interest
        p = Point(x[1], x[0])

        # Filter polygon elements using this lambda
        # keytree.geometry() makes a GeoJSON-like
        # geometry object from an element and shape()
        # makes a Shapely object of that
        hits = filter(lambda e: shape(keytree.geometry(e)).contains(p), elems)

        curr_file[1] += len(hits)
    
    print " "


for x in kml_count:
    if x[1] != 0:
        print x[0] + " --> " + x[1]
