# -*- coding: utf-8 -*-  
"""  
  
@author: jingjinzhou 
"""  
  
import os
from numpy import *
import struct

preview = True # nv21
confidence = True
        

if __name__ == '__main__':  

    ret = 'resData/'

    if not preview:
        path = 'capture/'
        size = (992,744)
    else:
        path = 'preview/'
        size = (720,540)

    width = size[0]
    height = size[1]
    
    files = os.listdir(path)

    for file in files:

        keyword = "depth"
        keyword2 = "CONFIDENCE"

        if not keyword in file:
            continue

        if preview:
            if confidence:
                if keyword2 not in file:
                    continue
            else:
                if keyword2 in file:
                    continue

        print file

        fileData = open(path+file, 'rb')

        ret = zeros((width,height),float,'C') 

        for i in range(width):
            for j in range(height):
                if preview:
                    if confidence:
                        str16 = struct.unpack("c",fileData.read(1))[0] # char
                        ret[i][j] = str16[0] > '\x40'
                    else:
                        tmp = struct.unpack("h",fileData.read(2)) #short
                        ret[i][j] = tmp[0]

                else:
                    tmp = struct.unpack("f",fileData.read(4)) #float
                    ret[i][j] = tmp[0]
                    

                print ret[i][j]

        break######test the first file
                

       