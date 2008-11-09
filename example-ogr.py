#!/usr/bin/python

import osgeo.ogr as ogr
import sys
from colorgradient import *
from earthpov import *

filename = 'data-ogr/shp2929/shp2929.shp'
threshold_area=10 # only render features with an area bigger than this

try:
	datasource = ogr.Open(filename)
	if datasource == None:
		raise IOError
except:
	print "Unable to open shapefile"
	sys.exit(1)


# colors
green = Color(rgb=[0.0,180.0/255.0,0.0])
red = Color(rgb=(180.0/255.0,0.0,0.0))
gradient = HSVGradient(c1=green,c2=red)



# collect geometries
geoms=[]
values=[]
maxvalue=0
lyr = datasource.GetLayer(0)
feat=lyr.GetNextFeature()
while (feat):
   all_geom = feat.GetGeometryRef() 
   geom = all_geom.GetGeometryRef(0) # only use first polygon of multipolygons
   if geom.GetArea()>threshold_area:
      wkt = geom.ExportToWkt()
      # water supply per captia
      value = feat.GetFieldAsDouble(5)
      values.append(value)
      geoms.append(wkt)
      if value>maxvalue:
         maxvalue=value
   feat=lyr.GetNextFeature()

# create graphs
pov = EarthPOV(colors=gradient)

for i in range(0,len(geoms)):
   print geoms[i]
   pov.addWKT(geoms[i],float(values[i])/maxvalue)

print pov

