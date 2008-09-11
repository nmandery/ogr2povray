#!/usr/bin/python

import psycopg2
import StringIO
import sys
from colorgradient import *

def valuepair(valstr):
   return map(float,valstr.split(' '))


class EarthPOV:
   def __init__(self,colors,pxheightmax=80):
      self.buffer = StringIO.StringIO()
      self.__header__()
      self.minvalue = 0.0002
      self.povheight=pxheightmax # max height in povray
      self.colors = colors

   def __header__(self):
      self.buffer.write( """

         // insert scene description before this point
         """)
      
   def addWKT(self,wkt,value,obj_modifier=''):
      """
      note: polygons with "holes" will not work
      """
      if not wkt.startswith('POLYGON(('):
         raise TypeError('Only Polygons are supported')
      if not 0.0<=value<=1.0:
         raise ValueError('value has to be between 0.0 and 1.0')
      if value==0.0:
         value = self.minvalue
      
      wktdata = wkt[wkt.rfind('(')+1:wkt.find(')')].split(',')
      data = map(valuepair,wktdata)
      
      data.append(data[1]) # cubic splines need these two extra points
      data.append(data[0])
      self.buffer.write('prism { cubic_spline\n 0, %f, %d \n' % (self.povheight*value,len(data)))
      for point in data:
         self.buffer.write(',\n <%f, %f>' % (point[0], point[1]))
      self.buffer.write('\ntexture { pigment { color rgbf <%f, %f, %f, 0.0> }}' % self.colors.getColor(value).rgb() )
      self.buffer.write('\nfinish { phong 0.2 phong_size 40 }')
      self.buffer.write('\n%s\n}\n' % obj_modifier)
   
   def getvalue(self):
      return self.buffer.getvalue()
   
   def __repr__(self):
      return self.getvalue()




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

