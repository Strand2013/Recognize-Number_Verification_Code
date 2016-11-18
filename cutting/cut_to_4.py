# -*- coding: utf-8 -*-
"""
@author: surui
"""
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
import time

class Cut_picture(object):

    @staticmethod
    def vcode_split(image):
        image_test = image.copy()
        image_split1 = image.copy()
        image_test = np.where(image_test >= 250, 0, 1)
        tx = np.sum(image_test, axis=0)
        ty = np.sum(image_test, axis=1)
        left = np.nonzero(tx)[0][0]
        right = np.nonzero(tx)[0][-1]
        up = np.nonzero(ty)[0][-1]
        down = np.nonzero(ty)[0][0]
        if down >= 0:
            down -= 1
        if up < image_test.shape[0]:
            up += 1
        if right < image_test.shape[1]:
            right += 1
        if left >= 0:
            left -= 1
        image_split1 = image_split1[down:up+1, left:right+1]  # 缩小边界
        high, width = image_split1.shape
        standard = width / 4
        image_test = image_split1.copy()
        image_split2 = image_split1.copy()
        image_test = np.where(image_test >= 250, 0, 1)
        tx = np.sum(image_test, axis=0)
        s = 3
        mi = min(tx[standard - s:standard + s])
        split_dot1 = standard - s + np.where(tx[standard - s:standard + s] == mi)[0][-1]
        mi = min(tx[2 * standard - s:2 * standard + s])
        split_dot2 = 2 * standard - s + np.where(tx[2 * standard - s:2 * standard + s] == mi)[0][0]
        mi = min(tx[3 * standard - s:3 * standard + s])
        split_dot3 = 3 * standard - s + np.where(tx[3 * standard - s:3 * standard + s] == mi)[0][0]
        distance2 = split_dot2 - split_dot1
        if 5 < distance2 and distance2 < 12:
            pass
        else:
            mid = int((split_dot3 + split_dot1) / 2)
            mi = min(tx[mid-2:mid+2])
            split_dot2 = mid + np.where(tx[mid-2:mid+2] == mi)[0][0]
        sub_img1 = image_split2[:, 0:split_dot1].copy()
        sub_img2 = image_split2[:, split_dot1:split_dot2].copy()
        sub_img3 = image_split2[:, split_dot2:split_dot3].copy()
        sub_img4 = image_split2[:, split_dot3+1:width].copy()
        return image_split1,[sub_img1, sub_img2, sub_img3, sub_img4]