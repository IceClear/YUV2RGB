# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 10:48:00 2013

@author: Chen Ming
"""

from numpy import *
from PIL import Image
import os
import cv2

def read_YUV420(image_path, rows, cols):
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

    with open(image_path, 'rb') as reader:
        for i in range(rows):
            for j in range(cols):
                gray[i, j] = ord(reader.read(1))

        for i in range(int(rows / 2)):
            for j in range(int(cols / 2)):
                img_U[i, j] = ord(reader.read(1))

        for i in range(int(rows / 2)):
            for j in range(int(cols / 2)):
                img_V[i, j] = ord(reader.read(1))

    return [gray, img_U, img_V]

'works for yuv420p'
def merge_YUV2RGB_v1(Y, U, V):
    """
    转换YUV图像为RGB格式（放大U、V）
    :param Y: Y分量图像
    :param U: U分量图像
    :param V: V分量图像
    :return: RGB格式图像
    """
    # Y分量图像比U、V分量图像大一倍，想要合并3个分量，需要先放大U、V分量和Y分量一样大小
    enlarge_U = cv2.resize(U, (0, 0), fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
    enlarge_V = cv2.resize(V, (0, 0), fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)

    # 合并YUV3通道
    img_YUV = cv2.merge([Y, enlarge_U, enlarge_V])

    dst = cv2.cvtColor(img_YUV, cv2.COLOR_YUV2BGR)
    return dst

if __name__ == '__main__':

    image_path = ''
    size = (3840,2880)
    Y, U, V = read_YUV420(image_path, size[1], size[0])

    dst = merge_YUV2RGB_v1(Y, U, V)

    cv2.imshow("dst", dst)
    cv2.imwrite('test_yuv.png', dst)
    cv2.waitKey(0) # not enter key in the terminal
