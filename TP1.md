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



