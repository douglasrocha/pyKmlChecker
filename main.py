import MySQLdb
import keytree
import multiprocessing

from joblib import Parallel, delayed
from os import listdir
from shapely.geometry import Point, shape
from xml.etree import ElementTree



def get_Linha():
    db = MySQLdb.Connect(host='localhost',
                         user='root',
                         passwd='root',
                         db='mydatabase')

    cur = db.cursor()
    cur.execute("SELECT ORDEM, LINHA, DATAHORA, LATITUDE, LONGITUDE, VELOCIDADE, BAIRRO FROM bus")

    list_retorno = []
    
    for row in cur.fetchall():
        list_retorno.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])

    db.close()

    return list_retorno

def update_Bairro(row, bairro):
    db = MySQLdb.Connect(host='localhost',
                         user='root',
                         passwd='root',
                         db='mydatabase')

    cur = db.cursor()
    cur.execute ("UPDATE bus SET BAIRRO='%s' WHERE ORDEM='%s' AND LINHA='%s' AND DATAHORA='%s'" % (bairro, row[0], row[1], row[2]))
    db.commit()
    db.close()

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
    

def get_CoordinateHitsCountOnPolygon(x, bairro):
    global lines_out

    if x[6] != "" and x[6] != None:
        return 0

    p = Point(x[4], x[3])

    hits = filter(lambda e: shape(keytree.geometry(e)).contains(p), elems)
    len_hits = len(hits)

    if len_hits > 0:
        update_Bairro(x, bairro);

    return len_hits


num_cores = multiprocessing.cpu_count()    

list_bus = get_Linha()
lines_out = []
    
kml_count = get_KmlDataStructure()
kml_strings = get_KmlContentFromDataStructure(kml_count)

#Parse the KML doc
for i in range(0, len(kml_strings)):
    doc = kml_strings[i]
    curr_file = kml_count[i]

    print str(i + 1) + " out of " + str(len(kml_strings)) + "(" + curr_file[0] + ")"

    tree = ElementTree.fromstring(doc)
    kmlns = tree.tag.split('}')[0][1:]

    # Find all Polygon elements anywhere in the doc
    elems = tree.findall(".//{%s}Polygon" % kmlns)

    results = Parallel(n_jobs=num_cores)(delayed(get_CoordinateHitsCountOnPolygon)(i, curr_file[0]) for i in list_bus)

    curr_file[1] += sum(results)

    list_bus = get_Linha()
    
    print " "


for x in kml_count:
    if x[1] != 0:
        print str(x[0]) + " --> " + str(x[1])
