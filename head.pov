
//#include "colors.inc"
/*
global_settings {
   radiosity {
      brightness 2.0
      count 100
      error_bound 0.15
      gray_threshold 0.0
      low_error_factor 0.2
      minimum_reuse 0.015
      nearest_count 10
      recursion_limit 5
      #if (version>3.1)
         adc_bailout 0.01
         max_sample 0.5
         media off
         normal off
         always_sample 1
         pretrace_start 0.08
         pretrace_end 0.01
      #end
   }
}
*/
camera {
   //orthographic
   location <15, 150, -180> // -130 
   right 16/9 * x
   up y
   //right 1.3 * 4/3 * x
   //up 1.3 * y
   look_at <15, 25, 0>
   aperture 0.1  // a bit of focal blur
   focal_point < 0, 10, 0> // focus on this point
}

light_source { <90, 300, 0> color rgb 1 }
light_source { <-90, 300, 0> color rgb 1 }

plane { y, 0
   pigment { 
      color rgb <1.0 1.0 1.0> 
   }
   finish { 
      ambient .2 
      diffuse .6  
      specular .75   
      roughness .001  
      reflection { .1 }  
   }
}
