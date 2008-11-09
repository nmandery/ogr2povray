#!/usr/bin/python

import osgeo.ogr as ogr
import sys

filename = 'data-ogr/shp2929/shp2929.shp'

try:
	datasource = ogr.Open(filename)
	if datasource == None:
		raise IOError
except:
	print "Unable to open shapefile"
	sys.exit(1)

lyr = datasource.GetLayer(0)
feat=lyr.GetNextFeature()
while (feat):
   geo=feat.GetGeometryColumn()
   feat=lyr.GetNextFeature()
