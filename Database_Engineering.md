

```python
# Dependencies
import pandas as pd
import numpy as np
import os
import csv

from sqlalchemy import create_engine
import pymysql
pymysql.install_as_MySQLdb()

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.automap import automap_base
```


```python
# Save path to data set in a variable
data_file_cm = "clean_hawaii_measurements.csv"
data_file_cs = "clean_hawaii_stations.csv"
```


```python
# Reading CSV file and displaying data as DataFrame
data_frame_cm = pd.read_csv(data_file_cm)
data_frame_cm.tail()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>station</th>
      <th>date</th>
      <th>prcp</th>
      <th>tobs</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>18098</th>
      <td>USC00516128</td>
      <td>2017-08-17</td>
      <td>0.13</td>
      <td>72</td>
    </tr>
    <tr>
      <th>18099</th>
      <td>USC00516128</td>
      <td>2017-08-19</td>
      <td>0.09</td>
      <td>71</td>
    </tr>
    <tr>
      <th>18100</th>
      <td>USC00516128</td>
      <td>2017-08-21</td>
      <td>0.56</td>
      <td>76</td>
    </tr>
    <tr>
      <th>18101</th>
      <td>USC00516128</td>
      <td>2017-08-22</td>
      <td>0.50</td>
      <td>76</td>
    </tr>
    <tr>
      <th>18102</th>
      <td>USC00516128</td>
      <td>2017-08-23</td>
      <td>0.45</td>
      <td>76</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Reading CSV file and displaying data as DataFrame
data_frame_cs = pd.read_csv(data_file_cs)
data_frame_cs
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>station</th>
      <th>name</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>elevation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>USC00519397</td>
      <td>WAIKIKI 717.2, HI US</td>
      <td>21.27160</td>
      <td>-157.81680</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>USC00513117</td>
      <td>KANEOHE 838.1, HI US</td>
      <td>21.42340</td>
      <td>-157.80150</td>
      <td>14.6</td>
    </tr>
    <tr>
      <th>2</th>
      <td>USC00514830</td>
      <td>KUALOA RANCH HEADQUARTERS 886.9, HI US</td>
      <td>21.52130</td>
      <td>-157.83740</td>
      <td>7.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>USC00517948</td>
      <td>PEARL CITY, HI US</td>
      <td>21.39340</td>
      <td>-157.97510</td>
      <td>11.9</td>
    </tr>
    <tr>
      <th>4</th>
      <td>USC00518838</td>
      <td>UPPER WAHIAWA 874.3, HI US</td>
      <td>21.49920</td>
      <td>-158.01110</td>
      <td>306.6</td>
    </tr>
    <tr>
      <th>5</th>
      <td>USC00519523</td>
      <td>WAIMANALO EXPERIMENTAL FARM, HI US</td>
      <td>21.33556</td>
      <td>-157.71139</td>
      <td>19.5</td>
    </tr>
    <tr>
      <th>6</th>
      <td>USC00519281</td>
      <td>WAIHEE 837.5, HI US</td>
      <td>21.45167</td>
      <td>-157.84889</td>
      <td>32.9</td>
    </tr>
    <tr>
      <th>7</th>
      <td>USC00511918</td>
      <td>HONOLULU OBSERVATORY 702.2, HI US</td>
      <td>21.31520</td>
      <td>-157.99920</td>
      <td>0.9</td>
    </tr>
    <tr>
      <th>8</th>
      <td>USC00516128</td>
      <td>MANOA LYON ARBO 785.2, HI US</td>
      <td>21.33310</td>
      <td>-157.80250</td>
      <td>152.4</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Reading Columns of DataFrame
data_frame_cs.columns
```




    Index(['station', 'name', 'latitude', 'longitude', 'elevation'], dtype='object')




```python
# To ignore warnings that gets triggered while executing same class more than once
import warnings
from sqlalchemy import exc as sa_exc

with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=sa_exc.SAWarning)
```


```python
# Define 'Measurement' table
class Measurement(Base):
    __tablename__ = 'measure'
    __table_args__ = {'extend_existing': True} 
    id = Column(Integer, primary_key=True)
    #index = Column(Integer)
    station = Column(String)
    date = Column(String)
    prcp = Column(Float)
    tobs = Column(Integer)
```


```python
# Define 'Station' table
class Station(Base):
    __tablename__ = 'station'
    __table_args__ = {'extend_existing': True} 
    id = Column(Integer, primary_key=True)
    #index = Column(Integer)
    station = Column(String)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    elevation = Column(Float)
```


```python
# Right now, this table only exists in python and not in the actual database
Base.metadata.tables
```




    immutabledict({'measure': Table('measure', MetaData(bind=None), Column('id', Integer(), table=<measure>, primary_key=True, nullable=False), Column('station', String(), table=<measure>), Column('date', String(), table=<measure>), Column('prcp', Float(), table=<measure>), Column('tobs', Integer(), table=<measure>), schema=None), 'station': Table('station', MetaData(bind=None), Column('id', Integer(), table=<station>, primary_key=True, nullable=False), Column('station', String(), table=<station>), Column('name', String(), table=<station>), Column('latitude', Float(), table=<station>), Column('longitude', Float(), table=<station>), Column('elevation', Float(), table=<station>), schema=None)})




```python
# The ORM’s “handle” to the database is the Session.
from sqlalchemy.orm import Session
session = Session(engine)
```


```python
# Create our database engine
engine = create_engine('sqlite:///hawaii.sqlite')

# This is where we create our tables in the database
Base.metadata.create_all(engine)
```


```python
# To drop created tables
#Base.metadata.drop_all(engine)
```

#### Defining Reflection


```python
Base_Reflect = automap_base()
Base_Reflect.prepare(engine, reflect=True)
```


```python
Base_Reflect.classes.keys()
```




    ['measure', 'station']




```python
# Loading data from Pandas 'DataFrame' to 'Sqlite' DB
Station_sqlite = data_frame_cs.to_sql(name='station', con=engine, if_exists='append', index=False)
Measurement_sqlite = data_frame_cm.to_sql(name='measure', con=engine, if_exists='append', index=False)
```


```python
# Save reference to the table
Station = Base_Reflect.classes.station
Measurement = Base_Reflect.classes.measure
```


```python
Station, Measurement
```




    (sqlalchemy.ext.automap.station, sqlalchemy.ext.automap.measure)


