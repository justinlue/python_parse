#!/usr/bin/env python
# encoding: utf-8
"""
@author: Elijah Luo
@file: parse.py
@time: 2018/03/02
"""
class File_act(object):

    def __init__(self, init_val, init_val2, nodes):
        self.__get_ack = self.__total_val = self.__total_last_val = self.__limit_last_val = init_val
        self.__limit_val = init_val2
        self.__nodes = nodes
        self.__count = 0
        self.__total = 0

    def __del__(self):
        pass
        # print('----deconstrcut-------')

    def set_keywords(self, keyword, keyword2, keyword3, keyword4, keyword5):
        self.__keyword = keyword
        self.__keyword2 = keyword2
        self.__keyword3 = keyword3
        self.__keyword4 = keyword4
        self.__keyword5 = keyword5

    def detail_search(self, keyword, string):
        idx = string.find(keyword)
        return idx

    def cal_val(self,
                string,
                input_idx,
                start,
                end):
        val = 0

        for i in range(start, end):
            if string[input_idx - i].isdigit() is True:
                val += int(string[input_idx - i]) * pow(10, i - 1)
        return val

    def compare_func(self,
                     a,
                     b,
                     flag):
        return (min(a, b), max(a, b))[flag == 'MAX']

    def new_find_keyword(self,
                         inputFile,
                         outputFile):
        fin = open(inputFile, 'r+')

        for eachLine in fin.readlines():
            idx = self.detail_search(self.__keyword, eachLine)
            if not idx == -1:
                sub_idx = self.detail_search(self.__keyword3, eachLine)
                if not sub_idx == -1:
                    val = self.cal_val(eachLine, sub_idx, 1, 4)
                    self.__limit_val = self.compare_func(self.__limit_val, val, 'MIN')
                    self.__get_ack += 1
                    self.__total_val += val

            idx = self.detail_search(self.__keyword2, eachLine)
            if not idx == -1:
                sub_idx = self.detail_search(self.__keyword3, eachLine)
                if not sub_idx == -1 and eachLine[sub_idx - 4] == ' ':
                    last_val = self.cal_val(eachLine, sub_idx, 1, 4)
                    self.__limit_last_val = self.compare_func(self.__limit_last_val, last_val, 'MAX')
                    self.__total_last_val += last_val

            sub_idx2 = self.detail_search(self.__keyword4, eachLine)
            if not sub_idx2 == -1:
                sub_idx3 = self.detail_search(self.__keyword3, eachLine)
                if not sub_idx3 == -1:
                    val2 = self.cal_val(eachLine, sub_idx3, 1, 2)
                    if val2 == self.__nodes:
                        self.__count = self.__count + 1

            idx = self.detail_search(self.__keyword5, eachLine)
            if not idx == -1:
                sub_idx = self.detail_search(self.__keyword3, eachLine)
                if not sub_idx == -1:
                    self.__total = self.cal_val(eachLine, sub_idx, 1, 6)

        if not self.__get_ack == 0:
            fin.write('ave of fast:' + str(self.__total_val / self.__get_ack) + 'ms' + '\n')
            fin.write('quickest:' + str(self.__limit_val) + 'ms' + '\n')
            fin.write('total: ' + str(self.__total) + '\n')
        if not self.__limit_last_val == 0:
            fin.write('slowest:' + str(self.__limit_last_val) + 'ms' + '\n')
            fin.write('times of getting all: ' + str(self.__count) + '\n')
        fin.write('times of getting ack: ' + str(self.__get_ack) + '\n')
        fin.close()
        # fout.close()
        # print(self.__get_ack)
