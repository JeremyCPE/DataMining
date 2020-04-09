from PIL import Image


from operator import itemgetter
import numpy
import math
import matplotlib.pyplot as plot
import glob
import json
import os
from sklearn.cluster import KMeans

listTotImage = glob.glob("project/testimagesFake/*")
selectionMax = len(listTotImage) #Nombre d'images max selectionnées
n = 1
count = 0
print("Recuperation de la ",n, " couleur(s) des",selectionMax," images")
f = open("project/data.json", "w")
f.write("")
f.close()
dataName = {}
datap = []
for i in listTotImage:
    data = {}
    data['name'] = os.path.basename(i)
    tagName = os.path.basename(i).split(" ", 1)[0].replace(".jpg", "").split("_")
    data['tag'] = tagName
    data['isSample'] = 0
    imgfile = Image.open(i)
    numarray = numpy.array(imgfile.getdata(), numpy.uint8)
    clusters = KMeans(n_clusters = n)
    clusters.fit(numarray)
    npbins = numpy.arange(0, n+1)
    #nbpins = array([0, 1, ..., n-1])
    histogram = numpy.histogram(clusters.labels_, bins=npbins)
    labels = numpy.unique(clusters.labels_)
    colors = []
    sizes = histogram[0]
    def rgb_to_hex(rgb):
        return "#%02x%02x%02x" % rgb
    for j in range(n):
        color = rgb_to_hex(
           (math.ceil(clusters.cluster_centers_[j][0]), 
            math.ceil(clusters.cluster_centers_[j][1]), 
            math.ceil(clusters.cluster_centers_[j][2])))
        colors.append(color)
    data["color"] = color
    data["intensity"] = sizes.tolist()[0]
    data["size"] = os.path.getsize(i)
    print("ajout de ",os.path.basename(i),"...")
    datap.append(data)

dataName['pictures'] = datap
dataName['users'] = []    
with open('project/data.json', 'a') as outfile:
    json.dump(dataName, outfile)
print("Fin, voir le fichier json")