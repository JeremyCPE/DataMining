### Exercice 1.2


```python
import numpy as np
dataset = np.loadtxt("pl.csv", dtype={'names': ('name', 'year'), 'formats': ('U100', 'i4')},
   skiprows=1, delimiter=",", encoding="UTF-8")
print(dataset)
```
```python
import numpy as np
dataset = np.loadtxt("pl.tsv", dtype={'names': ('name', 'year'), 'formats': ('U100', 'i4')},
   skiprows=1, delimiter="\t", encoding="UTF-8")
print(dataset) 
```
Un fichier TSV est un fichier dont les données sont séparés par des tabulation (\t)

### Exercice 1.5

#### Exercice 1.5.1

* 1. The population of countries in alphabetical order of their names and ascending order of year.
```python
from pandas.io.json import json_normalize
import pandas as pd
import json

jsondata = json.load(open('query.json'))
array = []

for data in jsondata:
  array.append([data['year'], data['countryLabel'], data['population']])
dataframe = pd.DataFrame(array, columns=['year', 'countryLabel', 'population'])
dataframe = dataframe.astype(dtype= {"year" : "int64", "countryLabel" : "<U200", "population" : "<U200"})
order = dataframe.sort_values(by=['countryLabel', 'year'],ascending=[True,True])
print(order)
```
2. The latest available population of every country

```python
from pandas.io.json import json_normalize
import pandas as pd
import json

jsondata = json.load(open('query.json'))
array = []

for data in jsondata:
  array.append([data['year'], data['countryLabel'], data['population']])
dataframe = pd.DataFrame(array, columns=['year', 'countryLabel', 'population'])
dataframe = dataframe.astype(dtype= {"year" : "int64", "countryLabel" : "<U200", "population" : "int64"})
order = dataframe.sort_values('year').groupby('countryLabel').tail(1)
print(order)
```

3. The country with the lowest and highest population (considering the latest population)


```python
from pandas.io.json import json_normalize
import pandas as pd
import json

jsondata = json.load(open('query.json'))
array = []

for data in jsondata:
  array.append([data['year'], data['countryLabel'], data['population']])
dataframe = pd.DataFrame(array, columns=['year', 'countryLabel', 'population'])
dataframe = dataframe.astype(dtype= {"year" : "int64", "countryLabel" : "<U200", "population" : "int64"})
order = dataframe.max()
print(order)
print("-----------------")
order = dataframe.min()
print(order)
```

#### Exercice 1.5.2

1. The number of articles published on different subjects every year.

```python
from pandas.io.json import json_normalize
import pandas as pd
import json

jsondata = json.load(open('query2.json'))
array = []

for data in jsondata:
  array.append([data['title'], data['subjectLabel'], data['year']])
dataframe = pd.DataFrame(array, columns=['title', 'subjectLabel', 'year'])
dataframe = dataframe.astype(dtype= {"year" : "int64", "subjectLabel" : "<U200", "title" : "<U200"})
order = dataframe.groupby(['subjectLabel','year']).count()
print(order)
```

2. Top subject of interest to the scientific community every year(based on the above query results).

```python
from pandas.io.json import json_normalize
import pandas as pd
import json

jsondata = json.load(open('query2.json'))
array = []

for data in jsondata:
  array.append([data['title'], data['subjectLabel'], data['year']])
dataframe = pd.DataFrame(array, columns=['title', 'subjectLabel', 'year'])
dataframe = dataframe.astype(dtype= {"year" : "int64", "subjectLabel" : "<U200", "title" : "<U200"})
order = dataframe.groupby(['subjectLabel','year']).agg('max')
print(order)
print("------------------------")
Q2_ = order.groupby('year')['title'].transform(max) == order['title']
print(order[Q2])
```
3. Top 10 subjects of interest to the scientific community (based on the above query results) since 2010.

```python
from pandas.io.json import json_normalize
import pandas as pd
import json

jsondata = json.load(open('query2.json'))
array = []

for data in jsondata:
  array.append([data['title'], data['subjectLabel'], data['year']])
dataframe = pd.DataFrame(array, columns=['title', 'subjectLabel', 'year'])
dataframe = dataframe.astype(dtype= {"year" : "int64", "subjectLabel" : "<U200", "title" : "<U200"})
order = dataframe.groupby(['subjectLabel','year']).agg('max')
print(order)
print("------------------------")
Q3 = dataframe[dataframe.year >= 2010].groupby(['subjectLabel','year']).agg('size').head(10)
print(Q3)
```
