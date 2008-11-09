#!/usr/bin/python

import psycopg2
import sys
from colorgradient import *
from earthpov import *


db_str = "dbname=geodb user=nico password=nico"
conn = psycopg2.connect(db_str)
cur = conn.cursor()

# the country with the maximal emissions is set as 100% 
cur.execute("select max(metric_tons) from rendering_emissions")
max_em = float(cur.fetchone()[0])

# only get outer polygon
cur.execute("select name,metric_tons ,astext(st_buildarea(sT_ExteriorRing(the_geom))) from rendering_emissions")

# get some colors
#green = Color(rgb=[0.0,1.0,0.0])
green = Color(rgb=[0.0,180.0/255.0,0.0])
#orange = Color(rgb=(1.0,72.0/255.0,0.0))
#red = Color(rgb=(1.0,0.0,0.0))
red = Color(rgb=(180.0/255.0,0.0,0.0))
gradient = HSVGradient(c1=green,c2=red)

# and a whole planet ;)
pov = EarthPOV(colors=gradient)

for row in cur.fetchall():
   # use sys.stdout for data output and stderr for messages
   percent = float(row[1])/max_em
   sys.stderr.write('Rendering %s -> %f of max\n' % (row[0],percent) )
   if row[2]==None:
      sys.stderr.write('Null-Geometry - ignoring\n')
   else:
      pov.addWKT(row[2],percent)

sys.stdout.write(str(pov))

