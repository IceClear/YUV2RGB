# -*- coding: utf-8 -*-  
"""  
Created on Thu Jan 10 10:48:00 2013  
  
@author: Chen Ming  
"""  
  
from numpy import *  
from PIL import Image  
import os

preview = True 

ret = 'res/'       

def convert(filename, width, height):
    print(filename)
    f_y = open(filename, "rb")
    f_uv= open(filename, "rb")
    converted_image_filename = ret + filename[0:-3] + "jpg"
    converted_image = Image.new("RGB", (width, height) )
    pixels = converted_image.load()
    uv_start = width*height

    f_y.seek(0);        
    for j in range(0, height):
        for i in range(0, width):
            #uv_index starts at the end of the yframe.  The UV is 1/2 height so we multiply it by j/2
            #We need to floor i/2 to get the start of the UV byte
            uv_index = uv_start + (width * math.floor(j/2)) + (math.floor(i/2))*2
            f_uv.seek(uv_index)
             
            y = ord(f_y.read(1))
            if not preview:
                u = ord(f_uv.read(1))
                v = ord(f_uv.read(1))
            else:
                v = ord(f_uv.read(1))
                u = ord(f_uv.read(1))
             
            b = 1.164 * (y-16) + 2.018 * (u - 128)
            g = 1.164 * (y-16) - 0.813 * (v - 128) - 0.391 * (u - 128)
            r = 1.164 * (y-16) + 1.596*(v - 128)
 
            pixels[i,j] = int(r), int(g), int(b)

    converted_image.save(converted_image_filename)

if __name__ == '__main__':  


    if not preview:
        path = 'capture/'
        size = (3968,2976)
    else:
        path = 'preview/'
        size = (1280, 960)
        
        files = os.listdir(path)

    for file in files:

        if not "yuv" in file:
            continue

        convert(path + file,size[0], size[1])
