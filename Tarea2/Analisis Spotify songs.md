Tarea: Analisis dataset Spotify songs

Listamos los archivos para verificar que tenemos el csv necesario.


```python
!ls
```

    'Analisis Spotify songs.ipynb'	 Untitled.ipynb       venv
     Netflix.ipynb			 jupyter_env
     Popular_Spotify_Songs.csv	 netflix_titles.csv


Instalamos pandas y lo importamos.


```python
!pip install pandas
```

    Requirement already satisfied: pandas in ./venv/lib/python3.12/site-packages (2.3.3)
    Requirement already satisfied: numpy>=1.26.0 in ./venv/lib/python3.12/site-packages (from pandas) (2.3.3)
    Requirement already satisfied: python-dateutil>=2.8.2 in ./venv/lib/python3.12/site-packages (from pandas) (2.9.0.post0)
    Requirement already satisfied: pytz>=2020.1 in ./venv/lib/python3.12/site-packages (from pandas) (2025.2)
    Requirement already satisfied: tzdata>=2022.7 in ./venv/lib/python3.12/site-packages (from pandas) (2025.2)
    Requirement already satisfied: six>=1.5 in ./venv/lib/python3.12/site-packages (from python-dateutil>=2.8.2->pandas) (1.17.0)



```python
import pandas as pd
```

Cargamos el Dataset y mostramos los primeros 10 datos.


```python
df = pd.read_csv("Popular_Spotify_Songs.csv", encoding='ISO-8859-1')
```


```python
df_row_data=df
```


```python
df.head(5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>track_name</th>
      <th>artist(s)_name</th>
      <th>artist_count</th>
      <th>released_year</th>
      <th>released_month</th>
      <th>released_day</th>
      <th>in_spotify_playlists</th>
      <th>in_spotify_charts</th>
      <th>streams</th>
      <th>in_apple_playlists</th>
      <th>...</th>
      <th>bpm</th>
      <th>key</th>
      <th>mode</th>
      <th>danceability_%</th>
      <th>valence_%</th>
      <th>energy_%</th>
      <th>acousticness_%</th>
      <th>instrumentalness_%</th>
      <th>liveness_%</th>
      <th>speechiness_%</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Seven (feat. Latto) (Explicit Ver.)</td>
      <td>Latto, Jung Kook</td>
      <td>2</td>
      <td>2023</td>
      <td>7</td>
      <td>14</td>
      <td>553</td>
      <td>147</td>
      <td>141381703</td>
      <td>43</td>
      <td>...</td>
      <td>125</td>
      <td>B</td>
      <td>Major</td>
      <td>80</td>
      <td>89</td>
      <td>83</td>
      <td>31</td>
      <td>0</td>
      <td>8</td>
      <td>4</td>
    </tr>
    <tr>
      <th>1</th>
      <td>LALA</td>
      <td>Myke Towers</td>
      <td>1</td>
      <td>2023</td>
      <td>3</td>
      <td>23</td>
      <td>1474</td>
      <td>48</td>
      <td>133716286</td>
      <td>48</td>
      <td>...</td>
      <td>92</td>
      <td>C#</td>
      <td>Major</td>
      <td>71</td>
      <td>61</td>
      <td>74</td>
      <td>7</td>
      <td>0</td>
      <td>10</td>
      <td>4</td>
    </tr>
    <tr>
      <th>2</th>
      <td>vampire</td>
      <td>Olivia Rodrigo</td>
      <td>1</td>
      <td>2023</td>
      <td>6</td>
      <td>30</td>
      <td>1397</td>
      <td>113</td>
      <td>140003974</td>
      <td>94</td>
      <td>...</td>
      <td>138</td>
      <td>F</td>
      <td>Major</td>
      <td>51</td>
      <td>32</td>
      <td>53</td>
      <td>17</td>
      <td>0</td>
      <td>31</td>
      <td>6</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Cruel Summer</td>
      <td>Taylor Swift</td>
      <td>1</td>
      <td>2019</td>
      <td>8</td>
      <td>23</td>
      <td>7858</td>
      <td>100</td>
      <td>800840817</td>
      <td>116</td>
      <td>...</td>
      <td>170</td>
      <td>A</td>
      <td>Major</td>
      <td>55</td>
      <td>58</td>
      <td>72</td>
      <td>11</td>
      <td>0</td>
      <td>11</td>
      <td>15</td>
    </tr>
    <tr>
      <th>4</th>
      <td>WHERE SHE GOES</td>
      <td>Bad Bunny</td>
      <td>1</td>
      <td>2023</td>
      <td>5</td>
      <td>18</td>
      <td>3133</td>
      <td>50</td>
      <td>303236322</td>
      <td>84</td>
      <td>...</td>
      <td>144</td>
      <td>A</td>
      <td>Minor</td>
      <td>65</td>
      <td>23</td>
      <td>80</td>
      <td>14</td>
      <td>63</td>
      <td>11</td>
      <td>6</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 24 columns</p>
</div>



NOTA: fué necesario cargar el archivo con un encoding específico ya que contiene algunos carácteres especiales.

Obtenemos información de las columnas que contiene el csv.


```python
df.columns
```




    Index(['track_name', 'artist(s)_name', 'artist_count', 'released_year',
           'released_month', 'released_day', 'in_spotify_playlists',
           'in_spotify_charts', 'streams', 'in_apple_playlists', 'in_apple_charts',
           'in_deezer_playlists', 'in_deezer_charts', 'in_shazam_charts', 'bpm',
           'key', 'mode', 'danceability_%', 'valence_%', 'energy_%',
           'acousticness_%', 'instrumentalness_%', 'liveness_%', 'speechiness_%'],
          dtype='object')



Podemos obtener la dimensión del archivo.


```python
df.shape
```




    (953, 24)



Para obtener el número de columnas y filas usamos las siguientes funciones.


```python
print("número de columnas:",len(df.columns))
print("número de filas:",len(df))

```

    número de columnas: 24
    número de filas: 953


Si necesitamos saber si hay valores vacíos en el csv usamos la siguiente función.


```python
df.isnull().sum().sort_values(ascending=False)
```




    key                     95
    in_shazam_charts        50
    track_name               0
    artist(s)_name           0
    released_month           0
    released_day             0
    artist_count             0
    released_year            0
    in_spotify_charts        0
    in_spotify_playlists     0
    streams                  0
    in_apple_playlists       0
    in_deezer_playlists      0
    in_apple_charts          0
    in_deezer_charts         0
    bpm                      0
    mode                     0
    danceability_%           0
    valence_%                0
    energy_%                 0
    acousticness_%           0
    instrumentalness_%       0
    liveness_%               0
    speechiness_%            0
    dtype: int64




```python
df["key"].head(10)
```




    0     B
    1    C#
    2     F
    3     A
    4     A
    5    C#
    6     F
    7     F
    8    C#
    9     D
    Name: key, dtype: object




```python
df["in_shazam_charts"].head(10)
```




    0    826
    1    382
    2    949
    3    548
    4    425
    5    946
    6    418
    7    194
    8    953
    9    339
    Name: in_shazam_charts, dtype: object




```python
df["key"] = df["key"].replace("",pd.NA).fillna("/")
```


```python
df["in_shazam_charts"] = df["in_shazam_charts"].replace("", pd.NA).fillna("/")

```

Para comprobar que se han llenado los campos vacíos podemos hacer un .head() a las columnas que hicimos cambios.


```python
df["in_shazam_charts"].head(30)
```




    0       826
    1       382
    2       949
    3       548
    4       425
    5       946
    6       418
    7       194
    8       953
    9       339
    10      251
    11      168
    12    1,021
    13    1,281
    14        /
    15      187
    16        0
    17    1,173
    18      187
    19       29
    20        0
    21      150
    22       73
    23      139
    24    1,093
    25      168
    26       96
    27      211
    28      325
    29        0
    Name: in_shazam_charts, dtype: object



Podemos comprobar si en nuestro csv hay duplicados haciendo lo siguiente.


```python
inicial = len(df)
```


```python
df = df.drop_duplicates()
```


```python
print("Se eliminaron ",(inicial - len(df)), " duplicados del csv")
```

    Se eliminaron  0  duplicados del csv


Una vez hemos limpiado los datos, podemos hacer algunas "consultas".


```python
df.loc[df["in_spotify_playlists"]>500 , ["track_name" , "artist(s)_name"]].head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>track_name</th>
      <th>artist(s)_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Seven (feat. Latto) (Explicit Ver.)</td>
      <td>Latto, Jung Kook</td>
    </tr>
    <tr>
      <th>1</th>
      <td>LALA</td>
      <td>Myke Towers</td>
    </tr>
    <tr>
      <th>2</th>
      <td>vampire</td>
      <td>Olivia Rodrigo</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Cruel Summer</td>
      <td>Taylor Swift</td>
    </tr>
    <tr>
      <th>4</th>
      <td>WHERE SHE GOES</td>
      <td>Bad Bunny</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Sprinter</td>
      <td>Dave, Central Cee</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Ella Baila Sola</td>
      <td>Eslabon Armado, Peso Pluma</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Columbia</td>
      <td>Quevedo</td>
    </tr>
    <tr>
      <th>8</th>
      <td>fukumean</td>
      <td>Gunna</td>
    </tr>
    <tr>
      <th>9</th>
      <td>La Bebe - Remix</td>
      <td>Peso Pluma, Yng Lvcas</td>
    </tr>
  </tbody>
</table>
</div>




```python
df.loc[df["artist(s)_name"].str.contains("linkin park",case=False) , ["track_name"]].head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>track_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>331</th>
      <td>Numb</td>
    </tr>
    <tr>
      <th>358</th>
      <td>In The End</td>
    </tr>
  </tbody>
</table>
</div>




```python

```


```python
df.loc[df["released_year"]<=2000 , ["track_name" , "artist(s)_name"]].head(20)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>track_name</th>
      <th>artist(s)_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>65</th>
      <td>Yellow</td>
      <td>Chris Molitor</td>
    </tr>
    <tr>
      <th>80</th>
      <td>Riptide</td>
      <td>Vance Joy</td>
    </tr>
    <tr>
      <th>114</th>
      <td>Everybody Wants To Rule The World</td>
      <td>Tears For Fears</td>
    </tr>
    <tr>
      <th>166</th>
      <td>Every Breath You Take - Remastered 2003</td>
      <td>The Police</td>
    </tr>
    <tr>
      <th>182</th>
      <td>Creep</td>
      <td>Radiohead</td>
    </tr>
    <tr>
      <th>195</th>
      <td>Have You Ever Seen The Rain?</td>
      <td>Creedence Clearwater Revival</td>
    </tr>
    <tr>
      <th>199</th>
      <td>Take On Me</td>
      <td>a-ha</td>
    </tr>
    <tr>
      <th>250</th>
      <td>The Real Slim Shady</td>
      <td>Eminem</td>
    </tr>
    <tr>
      <th>265</th>
      <td>Cupid ï¿½ï¿½ï¿½ Twin Ver. (FIFTY FIFTY) ï¿½ï¿½...</td>
      <td>sped up 8282</td>
    </tr>
    <tr>
      <th>320</th>
      <td>Gangsta's Paradise</td>
      <td>Coolio, L.V.</td>
    </tr>
    <tr>
      <th>358</th>
      <td>In The End</td>
      <td>Linkin Park</td>
    </tr>
    <tr>
      <th>424</th>
      <td>Running Up That Hill (A Deal With God)</td>
      <td>Kate Bush</td>
    </tr>
    <tr>
      <th>425</th>
      <td>Dream On</td>
      <td>Aerosmith</td>
    </tr>
    <tr>
      <th>439</th>
      <td>Agudo Mï¿½ï¿½gi</td>
      <td>Styrx, utku INC, Thezth</td>
    </tr>
    <tr>
      <th>441</th>
      <td>All I Want for Christmas Is You</td>
      <td>Mariah Carey</td>
    </tr>
    <tr>
      <th>442</th>
      <td>Last Christmas</td>
      <td>Wham!</td>
    </tr>
    <tr>
      <th>443</th>
      <td>Rockin' Around The Christmas Tree</td>
      <td>Brenda Lee</td>
    </tr>
    <tr>
      <th>444</th>
      <td>Jingle Bell Rock</td>
      <td>Bobby Helms</td>
    </tr>
    <tr>
      <th>447</th>
      <td>It's the Most Wonderful Time of the Year</td>
      <td>Andy Williams</td>
    </tr>
    <tr>
      <th>448</th>
      <td>Let It Snow! Let It Snow! Let It Snow!</td>
      <td>Dean Martin</td>
    </tr>
  </tbody>
</table>
</div>




```python
df.loc[df["in_spotify_playlists"]>df["in_apple_playlists"] , ["track_name" , "artist(s)_name"]].head(20)

```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>track_name</th>
      <th>artist(s)_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Seven (feat. Latto) (Explicit Ver.)</td>
      <td>Latto, Jung Kook</td>
    </tr>
    <tr>
      <th>1</th>
      <td>LALA</td>
      <td>Myke Towers</td>
    </tr>
    <tr>
      <th>2</th>
      <td>vampire</td>
      <td>Olivia Rodrigo</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Cruel Summer</td>
      <td>Taylor Swift</td>
    </tr>
    <tr>
      <th>4</th>
      <td>WHERE SHE GOES</td>
      <td>Bad Bunny</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Sprinter</td>
      <td>Dave, Central Cee</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Ella Baila Sola</td>
      <td>Eslabon Armado, Peso Pluma</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Columbia</td>
      <td>Quevedo</td>
    </tr>
    <tr>
      <th>8</th>
      <td>fukumean</td>
      <td>Gunna</td>
    </tr>
    <tr>
      <th>9</th>
      <td>La Bebe - Remix</td>
      <td>Peso Pluma, Yng Lvcas</td>
    </tr>
    <tr>
      <th>10</th>
      <td>un x100to</td>
      <td>Bad Bunny, Grupo Frontera</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Super Shy</td>
      <td>NewJeans</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Flowers</td>
      <td>Miley Cyrus</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Daylight</td>
      <td>David Kushner</td>
    </tr>
    <tr>
      <th>14</th>
      <td>As It Was</td>
      <td>Harry Styles</td>
    </tr>
    <tr>
      <th>15</th>
      <td>Kill Bill</td>
      <td>SZA</td>
    </tr>
    <tr>
      <th>16</th>
      <td>Cupid - Twin Ver.</td>
      <td>Fifty Fifty</td>
    </tr>
    <tr>
      <th>17</th>
      <td>What Was I Made For? [From The Motion Picture ...</td>
      <td>Billie Eilish</td>
    </tr>
    <tr>
      <th>18</th>
      <td>Classy 101</td>
      <td>Feid, Young Miko</td>
    </tr>
    <tr>
      <th>19</th>
      <td>Like Crazy</td>
      <td>Jimin</td>
    </tr>
  </tbody>
</table>
</div>



Para hacer gráficos tenemos que instalar matplotlib e importar la librería


```python
!pip install matplotlib
```

    Requirement already satisfied: matplotlib in ./venv/lib/python3.12/site-packages (3.10.6)
    Requirement already satisfied: contourpy>=1.0.1 in ./venv/lib/python3.12/site-packages (from matplotlib) (1.3.3)
    Requirement already satisfied: cycler>=0.10 in ./venv/lib/python3.12/site-packages (from matplotlib) (0.12.1)
    Requirement already satisfied: fonttools>=4.22.0 in ./venv/lib/python3.12/site-packages (from matplotlib) (4.60.1)
    Requirement already satisfied: kiwisolver>=1.3.1 in ./venv/lib/python3.12/site-packages (from matplotlib) (1.4.9)
    Requirement already satisfied: numpy>=1.23 in ./venv/lib/python3.12/site-packages (from matplotlib) (2.3.3)
    Requirement already satisfied: packaging>=20.0 in ./venv/lib/python3.12/site-packages (from matplotlib) (25.0)
    Requirement already satisfied: pillow>=8 in ./venv/lib/python3.12/site-packages (from matplotlib) (11.3.0)
    Requirement already satisfied: pyparsing>=2.3.1 in ./venv/lib/python3.12/site-packages (from matplotlib) (3.2.5)
    Requirement already satisfied: python-dateutil>=2.7 in ./venv/lib/python3.12/site-packages (from matplotlib) (2.9.0.post0)
    Requirement already satisfied: six>=1.5 in ./venv/lib/python3.12/site-packages (from python-dateutil>=2.7->matplotlib) (1.17.0)



```python
import matplotlib.pyplot as plt
```


```python
count = df["released_year"].value_counts().sort_index()
```


```python
plt.figure()
plt.plot(count.index, count.values)
plt.title("conteos por año")
plt.xlabel("año")
plt.ylabel("count")
plt.show()
```


    
![png](output_39_0.png)
    



```python

```


```python

```


```python

```


```python

```


```python

```


```python

```
