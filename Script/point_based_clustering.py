# script to cluster point based on

#import library
import arcpy
import os

#define variables
out_folder = "D:/Research/2021/Githubing/Output"
work_folder = "D:/Research/2021/Githubing/Arcgisfile"
aprx_input = r"D:/Research/2021/Githubing/Arcgisfile/Clustering.aprx"
csv_input = r"D:/Research/2021/Githubing/Data/kangarooIsland.csv"
buffer_size = "2000 Meters"
time_threshold = "2 Hours"

# Create geodatabase
out_gdb = "Clustering.gdb"
print("create workspace {}/{}".format(work_folder,out_gdb))
if not (os.path.isdir("{}/{}".format(work_folder,out_gdb))):
    arcpy.management.CreateFileGDB(work_folder,out_gdb)
workspace = r"{}/{}".format(work_folder,out_gdb)
arcpy.env.workspace = workspace

# Set property to overwrite existing output, by default
arcpy.env.overwriteOutput = True

# Use half of the cores on the machine to speed up process
arcpy.env.parallelProcessingFactor = "50%"

# load hotspot data, convert csv to shapefile
print("load data {}".format(csv_input))
arcpy.management.XYTableToPoint(csv_input, "hotspots", "longitude", "latitude","", arcpy.SpatialReference(4326))

#convert time field
arcpy.management.ConvertTimeField("hotspots", "datetime", "yyyyMMddHHmmss", "datetime_converted", "Date")

#project shapefile to custom conformal projection
wkt = "PROJCS['GDA20 / Australia Lambert Comformal Conic',GEOGCS['GDA2020',DATUM['D_GDA2020'," \
      "SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.017453292519943295]]," \
      "PROJECTION['Lambert_Conformal_Conic']," \
      "PARAMETER['standard_parallel_1',-18],PARAMETER['standard_parallel_2',-36]," \
      "PARAMETER['latitude_of_origin',-25],PARAMETER['central_meridian',140],PARAMETER['false_easting',0]," \
      "PARAMETER['false_northing',0],UNIT['Meter',1]]"
arcpy.management.Project("hotspots","hotspots_projected",wkt,"GDA2020_To_WGS_1984_2")

#create layer object
aprx = arcpy.mp.ArcGISProject(aprx_input)
arcpy.MakeFeatureLayer_management("hotspots_projected", "hotspots_lyr")
arcpy.SaveToLayerFile_management("hotspots_lyr", "hotspots_lyr.lyrx")

#insert layer to maps
m = aprx.listMaps("Map")[0]
lyr = m.addDataFromPath(r"{}/hotspots_lyr.lyrx".format(work_folder))
lyr = m.listLayers()[0]

#enable time to layer for clustering
lyr.enableTime("datetime_converted")
mt = lyr.time
mt.isTimeEnabled = True

#clustering
arcpy.gapro.FindPointClusters(lyr, "hotspots_clustered", "DBSCAN", 2, buffer_size, "Time", time_threshold)

#add field for point of origin and fire duration
arcpy.AddField_management("hotspots_clustered", "origin", "LONG",
                          field_alias="point of origin", field_is_nullable="NULLABLE")
arcpy.AddField_management("hotspots_clustered", "duration", "DOUBLE",
                          field_alias="duration (hours)", field_is_nullable="NULLABLE")

#populate the fields
with arcpy.da.UpdateCursor("hotspots_clustered", ["origin","FEAT_TIME","START_DATE","END_DATE","duration"]) as cursor:
    for row in cursor:
        # Update the starting point if hotspot time = cluster start time
        if row[1]==row[2]:
            row[0] = 1
        else:
            row[0] = 0
        durationDelta = row[3]-row[2]
        row[4] = durationDelta.total_seconds()/3600 # in hours
        cursor.updateRow(row)

#copy clustered layer into new layer to be exported
arcpy.management.Copy("hotspots_clustered", "cluster_export")

#add and alter some fields
arcpy.management.AlterField("cluster_export", "CLUSTER_ID", "clusterID", "Supercluster ID")
arcpy.management.ConvertTimeField("cluster_export", "FEAT_TIME", "Date", "time", "TEXT", "yyyy/MM/dd HH:mm:ss")
arcpy.management.ConvertTimeField("cluster_export", "START_DATE", "Date", "start_time", "TEXT", "yyyy/MM/dd HH:mm:ss")
arcpy.management.ConvertTimeField("cluster_export", "END_DATE", "Date", "end_time", "TEXT", "yyyy/MM/dd HH:mm:ss")
arcpy.management.DeleteField("cluster_export", ["datetime_converted","COLOR_ID","FEAT_TIME","START_DATE","END_DATE"])

#export result to shapefile
arcpy.conversion.FeatureClassToFeatureClass("cluster_export", out_folder, "cluster_export.shp")