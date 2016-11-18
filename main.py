# -*- coding: utf-8 -*-
"""
@author: surui
"""

import os, time, logging, traceback, sys
from util import code
from util.result import Result
import cv2
from cutting.cut_to_4 import Cut_picture
from cutting.recut import recut
from preprocess.remove_noiseback import remove_noiseback
from recognition.detect_number_cnn import Num_recog


class Number_recognition(object):

    def __init__(self):
        self.recognize = Num_recog()

    def preprocess(self,img):
        img = remove_noiseback(img)
        img_src, img_list = Cut_picture().vcode_split(img)
        img_list = map(recut, img_list)
        return img_src,img_list

    def input_file(self, path):
        img = cv2.imread(path,0)
        return img

    def main(self,path):
        img = self.input_file(path)
        img_src ,img_list = self.preprocess(img)
        result = []
        for img in img_list:
            self.recognize.load_model_predict(img)
            finall_result = self.recognize.load_model_predict(img)
            result.append(finall_result)
        str_result = ''.join(result)
        return str_result

# if __name__ == '__main__':
#     num_recog = Number_recognition()
#     path = '/home/hadoop/Desktop/test_all'
#     filelist = os.listdir(path)
#     right = 0
#     for file in filelist:
#         src_name = file.split('.')[0]
#         result = num_recog.main(os.path.join(path,file))
#         print src_name,result
#         if int(src_name) == int(result):
#             right += 1
#         else:
#             continue
#     right_rate = float(right)/len(filelist)
#     print ('rate is {}%'.format(right_rate*100))



if __name__ == "__main__":
    result = Result()
    img_type = sys.argv[1]
    img_file = sys.argv[2]
    # img_type = "file"
    # img_file = "D:/machine_learning/recognization/insurance_doc/1.jpg"
    try:
        num_recog = Number_recognition()
        predict_data = num_recog.main(img_file)
        data = {'captcha': predict_data}
        result.code = code.SUCCESS
        result.msg = "success"
        result.data = data
    except Exception, e:
        exstr = traceback.format_exc()
        logging.info('#####系统异错误error:%s', exstr)
        result.code = code.FAIL
        result.msg = sys.exc_info()
    print result.to_json()