#!/usr/bin/python

import StringIO
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

