import MySQLdb
import keytree
import multiprocessing

from joblib import Parallel, delayed
from os import listdir
from shapely.geometry import Point, shape
from xml.etree import ElementTree

def get_Linha(linha):
    db = MySQLdb.Connect(host='localhost',
                         user='root',
                         passwd='root',
                         db='mydatabase')

    cur = db.cursor()
    cur.execute("SELECT LATITUDE, LONGITUDE FROM bus WHERE LINHA=" + linha)

    list_retorno = []
    
    for row in cur.fetchall():
        list_retorno.append([row[0], row[1]])

    db.close()

    return list_retorno


def get_KmlDataStructure():
    kmls = listdir("./kml/")
    kml_count = []

    for x in kmls:
        kml_count.append([x, 0])

    return kml_count
    

def get_KmlContentFromDataStructure(datastructure):
    kml_strings = []

    for x in kml_count:
        myfile = open("./kml/" + x[0], 'r')
        kml_strings.append(myfile.read())
        myfile.close()

    return kml_strings
    

def get_CoordinateHitsCountOnPolygon(x):
    p = Point(x[1], x[0])

    hits = filter(lambda e: shape(keytree.geometry(e)).contains(p), elems)
    return len(hits)


num_cores = multiprocessing.cpu_count()    

list570 = get_Linha("570.0")
list583 = get_Linha("583.0")
    
kml_count = get_KmlDataStructure()
kml_strings = get_KmlContentFromDataStructure(kml_count)


#Parse the KML doc
for i in range(0, len(kml_strings)):
    doc = kml_strings[i]
    curr_file = kml_count[i]

    print str(i) + " out of " + str(len(kml_strings)) + "(" + curr_file[0] + ")"

    tree = ElementTree.fromstring(doc)
    kmlns = tree.tag.split('}')[0][1:]

    # Find all Polygon elements anywhere in the doc
    elems = tree.findall(".//{%s}Polygon" % kmlns)

    results = Parallel(n_jobs=num_cores)(delayed(get_CoordinateHitsCountOnPolygon)(i) for i in list583)

    curr_file[1] += sum(results)
    
    print " "


for x in kml_count:
    if x[1] != 0:
        print str(x[0]) + " --> " + str(x[1])
