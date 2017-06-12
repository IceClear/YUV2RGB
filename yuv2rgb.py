# -*- coding: utf-8 -*-  
"""  
Created on Thu Jan 10 10:48:00 2013  
  
@author: Chen Ming  
"""  
  
from numpy import *  
from PIL import Image  
import os

preview = False # nv21
  
           
def yuv_import(filename,dims,numfrm,startfrm):  
    fp=open(filename,'rb')  
    blk_size = prod(dims) *3/2  
    fp.seek(blk_size*startfrm,0)  
    Y=[]  
    U=[]  
    V=[]  
    d00=dims[0]//2  
    d01=dims[1]//2  
    Yt=zeros((dims[0],dims[1]),uint8,'C')  
    Ut=zeros((d00,d01),uint8,'C')  
    Vt=zeros((d00,d01),uint8,'C')  
    # print dims[0]
    # print dims[1]
    for i in range(numfrm):  
        for m in range(dims[0]):  
            for n in range(dims[1]):  
                #print m,n  
                Yt[m,n]=ord(fp.read(1))  

        if not preview:
            for m in range(d00):  
                for n in range(d01):  
                    Ut[m,n]=ord(fp.read(1)) 
                    Vt[m,n]=ord(fp.read(1)) 
        else:
            for m in range(d00):  
                for n in range(d01):  
                    Vt[m,n]=ord(fp.read(1)) 
                    Ut[m,n]=ord(fp.read(1)) 

        # for m in range(d00):  
        #     for n in range(d01):  
        #         Vt[m,n]=ord(fp.read(1))  
        # for m in range(d00):  
        #     for n in range(d01):  
        #         Ut[m,n]=ord(fp.read(1))  
        Y=Y+[Yt]  
        U=U+[Ut]  
        V=V+[Vt]  
    fp.close()  
    return (Y,U,V)  

def yuv2rgb(Y,U,V,width,height):  
    U=repeat(U,2,0)  
    U=repeat(U,2,1)  
    V=repeat(V,2,0)  
    V=repeat(V,2,1)  
    rr=zeros((width,height),float,'C')  
    gg=zeros((width,height),float,'C')  
    bb=zeros((width,height),float,'C')  

    rr= Y+1.14*(V-128.0)  
    gg= Y-0.395*(U-128.0)-0.581*(V-128.0)  
    bb= Y+2.032*(U-128.0)             # 必须是128.0，否则出错  

    # rr = Y + (1.370705 * (V-128.0));
    # gg = Y - (0.698001 * (V-128.0)) - (0.337633 * (U-128.0));
    # bb = Y + (1.732446 * (V-128.0));

    rr = clip(rr, 0, 255)
    gg = clip(gg, 0, 255)
    bb = clip(bb, 0, 255)

 
    rr1=rr.astype(uint8)  
    gg1=gg.astype(uint8)  
    bb1=bb.astype(uint8)  
 
    # print bb1[0:6,0:6]  
      
    return rr1,gg1,bb1  

if __name__ == '__main__':  

    ret = 'res/'
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

        data=yuv_import(path + '/' + file,size,1,0)  

        R_=data[0][0]  
        G_=data[1][0]  
        B_=data[2][0]  
        RGB=yuv2rgb(R_,G_,B_,size[0],size[1])  
        im_r=Image.frombytes('L',size,RGB[0].tostring())  
        im_g=Image.frombytes('L',size,RGB[1].tostring())  
        im_b=Image.frombytes('L',size,RGB[2].tostring())  
        # im_r.show()  
        # for m in range(2):  
        #     print m,': ', R_[m,:]  
        co=Image.merge('RGB', (im_r,im_g,im_b))  
        # co.show()  
        savePath = ret + path + file[0:-3]+'jpg'
        print savePath
        co.save(savePath)  


        # # for m in range(2):  
        # #     print m,': ', YY[m,:]  
      
        # print R_.shape

        im=Image.frombytes('L',size, R_.tostring())  
        # im.show()  
        im.save(ret + path + file[0:-4]+ 'gray'+'.jpg')  