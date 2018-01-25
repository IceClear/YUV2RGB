# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 10:48:00 2013

@author: Chen Ming
"""

from numpy import *
import cv2

screenLevels = 255.0
preview = True


def read_YUV420(image_path, rows, cols, numfrm):
    """
    读取YUV文件，解析为Y, U, V图像
    :param image_path: YUV图像路径
    :param rows: 给定高
    :param cols: 给定宽
    :return: 列表，[Y, U, V]
    """
    # create Y
    gray = np.zeros((rows, cols), np.uint8)
    # print(type(gray))
    # print(gray.shape)

    # create U,V
    img_U = np.zeros((int(rows / 2), int(cols / 2)), np.uint8)
    # print(type(img_U))
    # print(img_U.shape)

    img_V = np.zeros((int(rows / 2), int(cols / 2)), np.uint8)
    # print(type(img_V))
    # print(img_V.shape)
    Y = []
    U = []
    V = []
    reader=open(image_path,'rb')

    # with open(image_path, 'rb') as reader:
    for num in range(numfrm-1):
        Y_buf = reader.read(cols * rows)
        gray = np.reshape(np.frombuffer(Y_buf, dtype=np.uint8), [rows, cols])

        U_buf = reader.read(cols//2 * rows//2)
        img_U = np.reshape(np.frombuffer(U_buf, dtype=np.uint8), [rows//2, cols//2])

        V_buf = reader.read(cols//2 * rows//2)
        img_V = np.reshape(np.frombuffer(V_buf, dtype=np.uint8), [rows//2, cols//2])
        # for i in range(rows):
        #     for j in range(cols):
        #         gray[i, j] = ord(reader.read(1))
        #
        # for i in range(int(rows / 2)):
        #     for j in range(int(cols / 2)):
        #         img_U[i, j] = ord(reader.read(1))
        #
        # for i in range(int(rows / 2)):
        #     for j in range(int(cols / 2)):
        #         img_V[i, j] = ord(reader.read(1))
        Y = Y+[gray]
        U = U+[img_U]
        V = V+[img_V]

    return [Y, U, V]

# def yuv_import(filename,dims,numfrm,startfrm):
#     fp=open(filename,'rb')
#     blk_size = prod(dims) *3/2
#     fp.seek(blk_size*startfrm,0)
#     Y=[]
#     # U=[]
#     # V=[]
#     # print dims[0]
#     # print dims[1]
#     d00=dims[0]//2
#     d01=dims[1]//2
#     # print d00
#     # print d01
#     Yt=zeros((dims[0],dims[1]),uint8,'C')
#     # Ut=zeros((d00,d01),uint8,'C')
#     # Vt=zeros((d00,d01),uint8,'C')
#     for i in range(numfrm):
#         for m in range(dims[0]):
#             for n in range(dims[1]):
#                 #print m,n
#                 Yt[m,n]=ord(fp.read(1))
#         # for m in range(d00):
#         #     for n in range(d01):
#         #         Ut[m,n]=ord(fp.read(1))
#         # for m in range(d00):
#         #     for n in range(d01):
#         #         Vt[m,n]=ord(fp.read(1))
#         Y=Y+[Yt]
#         # U=U+[Ut]
#         # V=V+[Vt]
#     fp.close()
#     return Y
def yuv2rgb(Y,U,V,width,height):
    enlarge_U = cv2.resize(U, (0, 0), fx=2.0, fy=2.0)
    enlarge_V = cv2.resize(V, (0, 0), fx=2.0, fy=2.0)

    # 合并YUV3通道
    img_YUV = cv2.merge([Y, enlarge_U, enlarge_V])

    dst = cv2.cvtColor(img_YUV, cv2.COLOR_YUV2BGR)
    return dst



if __name__ == '__main__':
    from PIL import Image
    import os, sys
    sys.path.append('./')
    import f_game_dic
    from f_game_dic import f_game_dic_new_test as dataset
    import subprocess
    import imageio
    import numpy as np
    import subprocess


    get_yuv = False

 # -i BlueWorld.yuv -w 3840 -h 1920 -x 1 -o BlueWorld_1.yuv -l 3840 -m 2880 -y 1 -f 3 -n 1
    if get_yuv:
        for i in range(len(dataset)):
            video = imageio.get_reader('/media/s/YuhangSong_1/env/ff/vr_new/'+dataset[i]+'.mp4', 'ffmpeg')
            info = video.get_meta_data()
            [W,H] = info['source_size']
            print(W)
            print(H)
            print(dataset[i]+' is starting')
            subprocess.call(["./360tools_conv", "-i", '/media/s/YuhangSong_1/env/ff/vr_new/'+dataset[i]+'.yuv', "-w",str(W), "-h", str(H), "-x", str(1), "-o", '/media/s/Iceclear/CMP/'+dataset[i]+'.yuv', "-l", str(3840), "-m", str(2880), "-y", str(1), "-f", str(3)])
            print(dataset[i]+' is finished')
    else:
            size = (3840,2880)
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            for i in range(len(dataset)):
                video = imageio.get_reader('/media/s/YuhangSong_1/env/ff/vr_new/'+dataset[i]+'.mp4', 'ffmpeg')
                info = video.get_meta_data()
                # print(info)
                fps = info['fps']
                # print(stop)
                frame_num = info['nframes']
                print(frame_num)
                savePath = '/media/s/Iceclear/CMP/'
                # print(H)
                print(dataset[i]+' is starting')
                videoWriter = cv2.VideoWriter(savePath+dataset[i]+'.avi',fourcc,fps,size)#最后一个是保存图片的尺寸
                [Y,U,V]=read_YUV420(savePath + dataset[i]+'.yuv',size[1],size[0],frame_num)
                # print((Y[0]==Y[5]).all())
                # subprocess.call(["./360tools_conv", "-i", '/media/s/YuhangSong_1/env/ff/vr_new/'+dataset[i]+'.yuv', "-w",str(W), "-h", str(H), "-x", str(1), "-o", '/media/s/Iceclear/CMP/'+dataset[i]+'.yuv', "-l", str(3840), "-m", str(2880), "-y", str(1), "-f", str(3)])
                for index in range(frame_num-1):
                    RGB=yuv2rgb(Y[index],U[index],V[index],size[0],size[1])
                    videoWriter.write(RGB)
                videoWriter.release()
                print(dataset[i]+' is finished')

        # x = 3840
        # y = 1920

        # print(len(Y))
        # RGB=yuv2rgb(Y[i],U[i],V[i],size[0],size[1])
        # print(RGB.shape)
        # im_r=Image.frombytes('L',size,RGB[0].tostring())
        # im_g=Image.frombytes('L',size,RGB[1].tostring())
        # im_b=Image.frombytes('L',size,RGB[2].tostring())
        # co=Image.merge('RGB', (im_r,im_g,im_b))
        # co.show()
        # savePath = './a.jpg'
        # print(savePath)

        # RGB.save(savePath)
        # # print(len(data))
        # # #print data
        # # #im=array2image(array(data[0][0]))
        # YY=data[0][0]
        # print(YY.shape)
        # # UU = np.array(data[1][0], dtype=np.float)
        # # VV = np.array(data[2][0], dtype=np.float)
        # # image = Image.new("RGB",(x,y))
        # # B=YY+1.779*UU
        # # G=YY-0.3455*UU-0.7169*VV
        # # R=YY+1.4075*VV
        # # print(B.shape)
        # # for i in range(0,x):
        # #     for j in range(0,y):
        # #         image.putpixel((i,j),(int(B[i][j]),int(G[i][j]),int(R[i][j])))
        # # # for m in range(2):
        # #     # print(m,': ', YY[m,:])
        # # # im = cv2.cvtColor(YY,cv2.COLOR_YUV2RGB)
        # im=Image.frombytes('L',(3840,2880),YY.tostring())
        # # # im.show()
        # im.save('./a.jpg')
