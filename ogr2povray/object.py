"""
this file contains classes for the povray-objects this converter can 
create. so far only prisms can be created.
"""

class PovObject:
   def __init__(self):
      pass

class Prism(PovObject):
   def __init__(self,height,cubic=False):
      PovObject.__init__(self)
      self.height=height
      self.points=[]
      self.rgb=(1.0,0.0,0.0)
      self.cubic=cubic

   def addPoint(self,x,y):
      self.points.append((x,y))

   def setRGB(self,rgb):
      self.rgb=rgb

   def __repr__(self):
      if len(self.points)>2:
         if self.cubic: # needs some bug hunting - povray complains about unclosed splines
            rep="\nprism { cubic_spline\n 0, %f, %d" % (self.height,len(self.points)+2)
         else:
            rep="\nprism { linear_spline\n 0, %f, %d" % (self.height,len(self.points))
         for point in self.points:
            rep+=",\n <%f, %f>" % point
         if self.cubic:
            rep+=",\n <%f, %f>" % self.points[1]
            rep+=",\n <%f, %f>" % self.points[0]
         rep+="\ntexture { pigment { color rgbf <%f, %f, %f, 0.0> }}" % self.rgb
         rep+="\nfinish { phong 0.2 phong_size 40 }}"
      else:
         rep=''
      return rep


