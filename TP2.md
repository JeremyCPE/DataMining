## EXERCICE 2.1
#### This is the code we made in order to print (in red) the visual information on count of languages of different programming paradigms released in every available year :

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

## EXERCICE 2.2
#### This is the top 20 intensities in each band and the creation of a single plot of these top intensities : 
```python
from PIL import Image
import matplotlib.pyplot as plot

def getTop20Index(array):
    array_tmp = array.copy()
    returned_array = []
    for i in range(20):
        index_max = max(range(len(array_tmp)), key=array_tmp.__getitem__)
        returned_array.append(index_max)
        array_tmp[index_max] = 0
    return returned_array

imgfile = Image.open("data/flower.jpg")

histogram = imgfile.histogram()
red = histogram[0:255]
green = histogram[256:511]
blue = histogram[512:767]

# Get the top 20 values for each array (red green and blue)
indexTop20Red = getTop20Index(red)
indexTop20Green = getTop20Index(green)
indexTop20Blue = getTop20Index(blue)

x=range(255)
y = []
for i in x:
    y.append((red[i],green[i],blue[i]))

figure, axes = plot.subplots()
figure.tight_layout()
axes.set_prop_cycle('color', ['red', 'green', 'blue'])

# Print the top 20 values with the scatter method
for i in range(20):
    plot.scatter(indexTop20Red[i], red[indexTop20Red[i]], color='r')
    plot.scatter(indexTop20Green[i], green[indexTop20Green[i]], color='g')
    plot.scatter(indexTop20Blue[i], blue[indexTop20Blue[i]], color='b')
    
plot.plot(x,y)
plot.show()
```
## EXERCICE 2.3
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

## EXERCICE 2.4
```python
import numpy as np
import matplotlib.pyplot as plot
from sklearn.cluster import KMeans

numarray = np.array([[1, 1], [1, 2], [1, 3], [1, 4], [1, 5], 
              [1, 6], [1, 7], [1, 8],[1, 9], [1, 10], 
              [10, 1], [10, 2], [10, 3], [10, 4], [10, 5], 
              [10, 6], [10, 7], [10, 8],[10, 9], [10, 10]])

clusters = KMeans(n_clusters = 4, n_init=50)
clusters.fit(numarray)
colors = np.array(["#ff0000", "#00ff00", "#0000ff", "#ffff00"])
    
plot.scatter(numarray[:, 0], numarray[:, 1], c=colors[clusters.labels_])
plot.show()
```
If we increase the value of n_init (for example here 50), the algorithm will be repeated 50 times and so the number of values in each cluster will be perfectly equal whereas it is often not equal with only 2 repetition. We understand that we need to repeat the algorithm if we want relevant data.

```python
from pandas.io.json import json_normalize
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import json

data = json.load(open('citypopulation.json'))
dataframe = json_normalize(data)

le = LabelEncoder()
dataframe['cityLabel'] = le.fit_transform(dataframe['cityLabel'])
dataframe = dataframe.astype(dtype= {"year":"<i4", "cityLabel":"<U200", "population":"i"})
dataframe = dataframe.loc[dataframe['year'] > 1500]
dataframe = dataframe.loc[dataframe['population'] < 1000000]
yearPopulation = dataframe[['year', 'population']]

clusters = KMeans(n_clusters = 2, n_init=1000)
clusters.fit(yearPopulation.values)
colors = np.array(["#ff0000", "#00ff00", "#0000ff", "#ffff00"])
   

plot.rcParams['figure.figsize'] = [10, 10]
plot.scatter(yearPopulation['year'], yearPopulation['population'],
      c=colors[clusters.labels_])
plot.show()
```
When we try with different population number, we can see that the scale changes. LabelEncoder has been used to normalize data values, to get data refined.
When we use **MiniBatchKMeans** , we can still see the same graphics but printed faster than the previous method.

When we look at the two graphs that represent the execution time in function of the cluster, we can see that KMeans has a "crescendo" behaviour whereas MiniBatchKMeans is more random.
