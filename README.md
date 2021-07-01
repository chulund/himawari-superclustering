# himawari-8 superclustering script
The script in this respotitory are the simplified version for hotspot superclustering and determining point of origin using arcpy.
Although simplified, it should be sufficient to do hotspot superclustering and generating point of origin attribute.

It should be noted there is no extended version for the python/arcgis based superclustering since the superclustering was mostly done via model-builder and also FME.
The Matlab version of the script is also included in this repository. However, it is not recommended since the process is so long.

### Folder explanation
There are several folder in this repository. When running the script it is advised to keep the folder location as it is.
 - Script : contains the actual script for the superclustering. The environment should be setup properly before running the script.
 - Data : the input ascii data should be put here. More info on the data format see Input section. 
 - Output: the output cluster shapefile will be put in here.
 - Arcgisfile: contains the neccessary arcgis .aprx file as well as the location for the filegeodatabase to be created, which contains the intermediate results.
 - Other : zipped file containing scripts for matlab based superclustering, plotting, gridding, and many other matlab functions.

### Environment
The IDE environment should be setup properly in order for the script to work properly. The script was tested only in interpreter Python 3.7 (arcgispro-py3).
If arcgis pro is installed, the python excecutable should be located in the following folder: `...\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe`

### Input
The input file for the script, the format is similar to Chermelle usual output. The folder contains the Kangaroo Island hotspots file (kangarooisland.csv) for sample. Here is the snippet of the file
```
datetime,longitude,latitude,x,y,mir,tir,albedo,frp,state
20191221000000,136.939453,-35.703125,2585,4534,368.5625,296.875,0.179688,-999, SA
20191224000000,137.032227,-35.677734,2589,4533,340.125,300.5,0.210938,78.47, SA
20191224000000,137.007812,-35.703125,2588,4534,364.125,299.125,0.179688,278.13, SA
20191224000000,137.03125,-35.703125,2589,4534,397.3125,307.625,0.171875,799.62, SA
20191224000000,137.053711,-35.702148,2590,4534,354.8125,306,0.109375,186.81, SA
```

### defined variables
The first part of the script contains the following variable, which can be changed:  
```
out_folder = "D:/Research/2021/Githubing/Output"
work_folder = "D:/Research/2021/Githubing/Arcgisfile"
aprx_input = r"D:/Research/2021/Githubing/Arcgisfile/Clustering.aprx"
csv_input = r"D:/Research/2021/Githubing/Data/kangarooIsland.csv"
buffer_size = "2000 Meters"
time_threshold = "2 Hours"
```

The rest of the script is commented and should be self explanatory.


@Nur Trihantoro - 30 June 2021
