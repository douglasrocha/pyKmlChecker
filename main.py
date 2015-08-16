from urllib import urlopen
from xml.etree import ElementTree

import keytree
from shapely.geometry import Point, shape

#Parse the KML doc
doc = urlopen("http://pleiades.stoa.org/places/638753/kml").read()
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

print hits
