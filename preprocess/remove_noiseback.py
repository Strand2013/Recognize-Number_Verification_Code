# -*- coding: utf-8 -*-
"""
@author: surui
"""

import cv2
import os


def remove_noiseback(image):
    '''参数只有 image'''
    if image is not None:
        retval, dst = cv2.threshold(image, 0, 255, cv2.THRESH_OTSU)
    else:
        raise Exception('image is None')
    return dst
