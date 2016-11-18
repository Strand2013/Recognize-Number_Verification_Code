# -*- coding: utf-8 -*-
"""
@author: surui
"""
from __future__ import division, print_function, absolute_import
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.normalization import local_response_normalization
from tflearn.layers.estimator import regression
import numpy
import os


class Num_recog(object):

    def __init__(self):
        #self.train_path = ""
        #self.verify_path = verify_path
        #self.verify_path = ""
        #self.samples_num = 1480
        self.verify_num = 4
        self.img_size = 10
        self.num_classes = 10
        self.model = self.build_cnn_model()
        self.base_dir = os.path.dirname(__file__)
        self.model.load(os.path.join(self.base_dir,'model.tfl'))


    # Building convolutional network
    def build_cnn_model(self):
        # Building convolutional network
        network = input_data(shape=[None, 10, 10, 1], name='input')
        network = conv_2d(network, 8, 3, activation='relu', regularizer="L2")
        # network = max_pool_2d(network, 2)
        network = local_response_normalization(network)
        network = conv_2d(network, 16, 3, activation='relu', regularizer="L2")
        # network = max_pool_2d(network, 2)
        network = local_response_normalization(network)
        network = fully_connected(network, 128, activation='tanh')
        network = dropout(network, 0.9)
        network = fully_connected(network, 256, activation='tanh')
        network = dropout(network, 0.9)
        network = fully_connected(network, 10, activation='softmax')
        network = regression(network, optimizer='adam', learning_rate=0.0001,
                             loss='categorical_crossentropy', name='target')
        model = tflearn.DNN(network, tensorboard_verbose=1, tensorboard_dir="/tmp/2class_logs/")
        return model


    def my_predict(self, model, input_X):
        num = numpy.shape(input_X)[0]
        shape = [num, -1]
        result = model.predict(input_X)
        result = numpy.reshape(result, shape)
        class_result = numpy.zeros([num], dtype='uint8')
        proba_result = numpy.zeros([num], dtype='float')
        for i in range(num):
            tmp = result[i, :]
            class_result[i] = numpy.argmax(tmp)
            proba_result[i] = max(tmp)
        return [class_result, proba_result]


    def load_model_predict(self,img):
        raw_img = numpy.zeros([1, 10, 10], dtype='uint8')
        raw_img[0, :, :] = img
        raw_img = raw_img.reshape([1, 10, 10, 1])
        class_result, prob_result = self.my_predict(self.model, raw_img)
        return str(class_result[0])





