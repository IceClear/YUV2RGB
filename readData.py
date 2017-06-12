# -*- coding: utf-8 -*-  
"""  
  
@author: jingjinzhou 
"""  
  
import os
from numpy import *
import struct
import scipy.misc
from PIL import Image  

preview = True # nv21
confidence = True
        

if __name__ == '__main__':  

    retFile = 'resData/'

    if not preview:
        path = 'capture/'
        size = (992,744)
    else:
        path = 'preview/'
        size = (768,540)

    width = size[0]
    height = size[1]
    # print("width:", width)
    # print("height", height)
    
    files = os.listdir(path)

    for file in files:

        keyword = ".dat"
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
                    

                # print ret[i][j]

        tmpMax = amax(ret)
        tmpMin = amin(ret)
        print tmpMax
        print tmpMin


        ## normalize
        ret = ret.astype(float)

        for i in range(width):
            for j in range(height):
                # print(ret[i][j])
                ret[i][j] = (ret[i][j] - tmpMin) / (tmpMax - tmpMin) * 255
                # print(ret[i][j])

        ret = ret.astype(uint8)

        im=Image.frombytes('L',size, ret.tostring())
        im.save(retFile + path + file[0:-3] + 'jpg')


        # scipy.misc.imsave(retFile + path + file[0:-3] + 'png', ret)




        # break######test the first file
                

       