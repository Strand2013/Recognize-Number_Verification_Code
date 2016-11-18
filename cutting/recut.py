# -*- coding: utf-8 -*-
"""
@author: surui
"""
import numpy as np
import cv2

def recut(image):
    '''
    input is one image
    output is one image
    '''
    if image is not None:
        image_test = image.copy()
        image_split1 = image.copy()
        high , width = image_split1.shape
        image_test = np.where(image_test >= 250, 0, 1)
        tx = np.sum(image_test, axis=0)
        ty = np.sum(image_test, axis=1)
        try:
            left = np.nonzero(tx)[0][0]
        except:
            left = 0
        try:
            right = np.nonzero(tx)[0][-1]
        except:
            right = width
        try:
            up = np.nonzero(ty)[0][-1]
        except:
            up = high
        try:
            down = np.nonzero(ty)[0][0]
        except:
            down = 0
        if up-down <= 8:
            up = high-1
            down = 0
        if left >= 1:
            left -= 1
        if right < width:
            width += 1
        if down >= 1:
            down -= 1
        if up < high:
            up += 1
        image_split1 = image_split1[down:up+1, left:right+1]
        # 二值化
        new_img = cv2.adaptiveThreshold(image_split1, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 25, 15)
        # 变成10x10的正方形
        new_img = cv2.resize(new_img, (10, 10), interpolation=cv2.INTER_CUBIC)
    else:
        raise Exception('Image is None')
    return new_img
