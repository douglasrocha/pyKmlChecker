from os import listdir
from xml.etree import ElementTree

import keytree
from shapely.geometry import Point, shape

kml_files = listdir("./kml/")
kml_strings = []

# Reads all kml files to strings' list
for x in kml_files:
    myfile = open("./kml/" + x, 'r')
    kml_strings.append(myfile.read())
    myfile.close()

print kml_strings[1]

#Parse the KML doc
for i in range(0, len(kml_strings)):
    doc = kml_strings[i]
    curr_file = kml_files[i]

    tree = ElementTree.fromstring(doc)
    kmlns = tree.tag.split('}')[0][1:]

    # Find all Polygon elements anywhere in the doc
    elems = tree.findall(".//{%s}Polygon" % kmlns)

    # Here's our poin of interest
    p = Point(28.722144580890763, 37.707799701548467)

    # Filter polygon elements using this lambda
    # keytree.geometry() makes a GeoJSON-like
    # geometry object from an element and shape()
    # makes a Shapely object of that
    hits = filter(lambda e: shape(keytree.geometry(e)).contains(p), elems)

    print curr_file + " --> " + str(len(hits))
