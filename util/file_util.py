# -*- coding: utf-8 -*-
#!/usr/bin/python
__author__ = 'lijunling'
import os
from PIL import Image
from numpy import *
import cv2

class FileUtil:
    def __init__(self):
        self.file = ""

    def creat_out_dir(self,img_out_dir):
        if not os.path.exists(img_out_dir):
            os.makedirs(img_out_dir)
        else:
            for file in os.listdir(img_out_dir):
                legacy_file = os.path.join(img_out_dir, file)
                #if os.path.isfile(legacy_file):
                    #os.remove(legacy_file)

    def clean_out_dir(self,img_out_dir):

        for file in os.listdir(img_out_dir):
            legacy_file = os.path.join(img_out_dir, file)
            if os.path.isfile(legacy_file):
                    os.remove(legacy_file)

    def save_img_file(self, img_array,file_dir,output_dir,pre_name=""):
        #self.creat_out_dir(file_dir)
        file_name = pre_name + os.path.basename(file_dir)
        file_full_path = os.path.join(output_dir, file_name)
        #Image.fromarray(img_array).save(file_full_path)  #保存rgb图，颜色显示不正确
        cv2.imwrite(file_full_path,img_array)
        return file_full_path


    '''文件、路径常用操作方法
    '''
    @staticmethod
    def read_file_data(filepath, delimiter):
        '''根据路径按行读取文件, 参数filepath：文件的绝对路径
        @param filepath: 读取文件的路径
        @return: 按\t分割后的每行的数据列表
        '''
        fin = open(filepath, 'r')
        for line in fin:
            try:
                line = line[:-1]
                if not line: continue
            except:
                continue

            try:
                fields = line.split(delimiter)
            except:
                continue
            # 抛出当前行的分割列表
            yield fields
        fin.close()


    @staticmethod
    def map_fields_dict_schema(fields, dict_schema):
        """根据字段的模式，返回模式和数据值的对应值；例如 fields为['a','b','c'],schema为{'name':0, 'age':1}，那么就返回{'name':'a','age':'b'}
        @param fields: 包含有数据的数组，一般是通过对一个Line String通过按照\t分割得到
        @param dict_schema: 一个词典，key是字段名称，value是字段的位置；
        @return: 词典，key是字段名称，value是字段值
        """
        pdict = {}
        for fstr, findex in dict_schema.iteritems():
            pdict[fstr] = str(fields[int(findex)])
        return pdict

    @staticmethod
    def transform_list_to_dict(para_list):
        """把['a', 'b']转换成{'a':0, 'b':1}的形式
        @param para_list: 列表，里面是每个列对应的字段名
        @return: 字典，里面是字段名和位置的映射
        """
        res_dict = {}
        idx = 0
        while idx < len(para_list):
            res_dict[str(para_list[idx]).strip()] = idx
            idx += 1
        return res_dict

    @staticmethod
    def map_fields_list_schema(fields, list_schema):
        """根据字段的模式，返回模式和数据值的对应值；例如 fields为['a','b','c'],schema为{'name', 'age'}，那么就返回{'name':'a','age':'b'}
        @param fields: 包含有数据的数组，一般是通过对一个Line String通过按照\t分割得到
        @param list_schema: 列名称的列表list
        @return: 词典，key是字段名称，value是字段值
        """
        dict_schema = FileUtil.transform_list_to_dict(list_schema)
        return FileUtil.map_fields_dict_schema(fields, dict_schema)

    # Get the all files & directories in the specified directory (path).
    @staticmethod
    def get_recursive_file_list(path):
        current_files = os.listdir(path)
        all_files = []
        for file_name in current_files:
            full_file_name = os.path.join(path, file_name)
            all_files.append(full_file_name)

            if os.path.isdir(full_file_name):
                next_level_files = FileUtil.get_recursive_file_list(full_file_name)
                all_files.extend(next_level_files)

        return all_files
