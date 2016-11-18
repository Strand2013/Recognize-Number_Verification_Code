# -*- coding: utf-8 -*-
from util import json_util, code


class Result(object):

    def __init__(self, code="1", msg="", data=""):
        self.code = code
        self.msg = msg
        self.data = data

    def to_json(self):
        return json_util.to_json(self)

if __name__ == "__main__":
    # data = {"name":"庞龙", "sex":"男"}
    result = Result(code.SUCCESS, "成功", "47849327984732984798798")
    # result = Result(code.FAIL,"失败","")
    print result.to_json()

