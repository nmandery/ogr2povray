
import colorsys

class Color:
   """
   pretty basic class to manage colors
   """
   
   def __init__(self,rgb=None,hsv=None):
      """
      create a new color
      use rgb OR hsv to set the inital value - else it will be black
      """
      self.value = [.0,.0,.0] # default is just black
      self.set(rgb=rgb,hsv=hsv)
   
   def set(self,rgb=None,hsv=None):
      """
      set the color
      you can either specify rgb or hsv values 
      """     
      if rgb!=None:
         self.value = colorsys.rgb_to_hsv(*rgb)
      if hsv!=None:
         self.value = hsv
   
   def rgb(self):
      """
      get a tuple of rgb values
      """
      return colorsys.hsv_to_rgb(*self.value)
   
   def hsv(self):
      """
      get a tuple of hsv values
      """
      return self.value
   
   def htmlhex(self):
      """
      return the value as hex-string for html use
      """
      vs=map(self.tohex,self.rgb()) 
      return "#%s" % ''.join(vs)
      
      
   def tohex(self,value):
      """
      """
      v = "%x" % (value*255)
      if len(v)==1:
         v="0"+v
      return v

class Gradient:
   def __init__(self,c1,c2):
      """
      0.0 -> c1
      1.0 -> c2
      """
      self.c1=c1
      self.c2=c2
   
   def getColor(self,value):
      """
      get the color for a value between 0.0 (c1) and 1.0 (c2)
      """
      raise NotImplementedError
   
      
      
class HSVGradient(Gradient):
   """
   calculate via hsv-values
   """
   def __init__(self,**kwargs):
      Gradient.__init__(self,**kwargs)
      
   def getColor(self,value):
      result=[]
      hsv1 = self.c1.hsv()
      hsv2 = self.c2.hsv()
      for i in range(3):
         c = hsv1[i]-hsv2[i]
         result.append(hsv1[i]-(c*value))
      return Color(hsv=result)
         