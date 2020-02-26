### Exercice 2.1

```python
from pandas.io.json import json_normalize
import pandas as pd
import json
import math
import matplotlib.pyplot as plot

jsondata = json.load(open('data/plparadigm.json'))
array = []

for data in jsondata:
    array.append([data['year'], data['languageLabel'], data['paradigmLabel']])

dataframe = pd.DataFrame(array, columns=['year', 'languageLabel', 'paradigmLabel'])
dataframe = dataframe.astype(dtype= {"year" : "int64", "languageLabel" : "<U200", "paradigmLabel" : "<U200"})

grouped = dataframe.groupby(['year']).count()
grouped = grouped.rename(columns={'languageLabel':'count'})
grouped = grouped.groupby(['paradigmLabel'])

#Initialization of subplots
nr = math.ceil(grouped.ngroups/2)
fig, axes = plot.subplots(nrows=nr, ncols=2, figsize=(20,25))

#Creation of subplots
for i, group in enumerate(grouped.groups.keys()):
    g = grouped.get_group(group).reset_index()
    g.plot(x='year', y='count', kind='bar',title=group, color='green', ax=axes[math.floor(i/2),i%2])

   
grouped2 = dataframe.groupby('year').count()
grouped2 = grouped2.rename(columns={'year':'count', 'paradigmLabel':'count'}).reset_index().drop(columns={'languageLabel':'count'})
grouped2.plot(x=0, kind='bar', title="Programming languages per year", color="red")

plot.show()
```

### Exercice 2.3
In this exercise, we will take a look at KMeans clustering algorithm. Continuing with images, we will now find 4 predominant colors in an image. (https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html)

```python
from PIL import Image
import numpy
import math
import matplotlib.pyplot as plot
from sklearn.cluster import KMeans

imgfile = Image.open("data/flower.jpg")

numarray = numpy.array(imgfile.getdata(), numpy.uint8)

clusters = KMeans(n_clusters = 4)
clusters.fit(numarray)


npbins = numpy.arange(0, 5)
histogram = numpy.histogram(clusters.labels_, bins=npbins)
labels = numpy.unique(clusters.labels_)


barlist = plot.bar(labels, histogram[0])
for i in range(4):
    barlist[i].set_color('#%02x%02x%02x' % (math.ceil(clusters.cluster_centers_[i][0]),
        math.ceil(clusters.cluster_centers_[i][1]), math.ceil(clusters.cluster_centers_[i][2])))
plot.show()
```

1. Assume that the number of clusters is given by the user, generalize the above code.

```python
from PIL import Image
import numpy
import math
import matplotlib.pyplot as plot
from sklearn.cluster import KMeans

while True:
    n = input("Choisissez le nb de cluster ")
    try:
        n = int(n)
        break
    except ValueError:
        print("Saisie invalide")
    
imgfile = Image.open("data/flower.jpg")

numarray = numpy.array(imgfile.getdata(), numpy.uint8)

clusters = KMeans(n_clusters = n)
clusters.fit(numarray)


npbins = numpy.arange(0, n+1)
#nbpins = array([0, 1, ..., n-1])
histogram = numpy.histogram(clusters.labels_, bins=npbins)
labels = numpy.unique(clusters.labels_)


barlist = plot.bar(labels, histogram[0])
for i in range(n):
    barlist[i].set_color('#%02x%02x%02x' % (math.ceil(clusters.cluster_centers_[i][0]),
        math.ceil(clusters.cluster_centers_[i][1]), math.ceil(clusters.cluster_centers_[i][2])))
plot.show()
```

2. In case of bar chart, ensure that the bars are arranged in the descending order of the frequency of colors.

```python
from PIL import Image


from operator import itemgetter
import numpy
import math
import matplotlib.pyplot as plot
from sklearn.cluster import KMeans

#while True:
#    n = input("Choisissez le nb de cluster ")
#    try:
#        n = int(n)
#        break
#    except ValueError:
#        print("Saisie invalide")
n = 4
imgfile = Image.open("data/flower.jpg")

numarray = numpy.array(imgfile.getdata(), numpy.uint8)

clusters = KMeans(n_clusters = n)
clusters.fit(numarray)

npbins = numpy.arange(0, n+1)
#nbpins = array([0, 1, ..., n-1])
histogram = numpy.histogram(clusters.labels_, bins=npbins)
a = numpy.argsort(histogram[0], axis=0)
print(a)
histogram[0].sort()
print(histogram[0])
labels = numpy.unique(clusters.labels_)
print(barlist)
barlist = plot.bar(labels, histogram[0])
for i in range(n):
    barlist[i].set_color('#%02x%02x%02x' % (math.ceil(clusters.cluster_centers_[i][0]),
        math.ceil(clusters.cluster_centers_[i][1]), math.ceil(clusters.cluster_centers_[i][2])))
plot.show()
```
3. Also add support for pie chart in addition to the bar chart. Ensure that we use the image colors as the wedge colors. (e.g., given below)

```python
from PIL import Image
from operator import itemgetter
import numpy
import math
import matplotlib.pyplot as plot
from sklearn.cluster import KMeans

#while True:
#    n = input("Choisissez le nb de cluster ")
#    try:
#        n = int(n)
#        break
#    except ValueError:
#        print("Saisie invalide")
n = 6
imgfile = Image.open("data/flower.jpg")
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
for i in range(n):
    color = rgb_to_hex(
        (math.ceil(clusters.cluster_centers_[i][0]), 
         math.ceil(clusters.cluster_centers_[i][1]), 
         math.ceil(clusters.cluster_centers_[i][2])))
    colors.append(color)
print(colors)
plot.pie(sizes, labels=labels, colors=colors,shadow=True, startangle=140)
plot.show()                        
```

4. Do you have any interesting observations?

