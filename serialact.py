#!/usr/bin/env python
# encoding: utf-8
"""
@author: Elijah Luo
@file: parse.py
@time: 2018/05/02
"""
import serial
import time
import threading
from datetime import datetime

class Serial_port(object):

    def __init__(self, port, baud, waitingTime):
        try:
            self.ser = serial.Serial(port, baud, timeout = 2)
        except Exception as e:
            print(e)
        else:
            self.alive = False
            self.waitEnd = None
            self.startTime = datetime.utcnow()
            self.endTime = datetime.utcnow()
            self.lastTime = datetime.utcnow()
            self.times = 0
            self.timeout = time.time()
            self.waitingTime = waitingTime
            print('open serial successfully')
        # print(self.ser.isOpen())
    def set_keywords(self, keyword, keyword2, keyword3, keyword4, keyword5):
        self.keyword = keyword
        self.keyword2 = keyword2
        self.keyword3 = keyword3
        self.keyword4 = keyword4
        self.keyword5 = keyword5

    def __del__(self):
        pass

    def waiting(self):
        if not self.waitEnd is None:
            self.waitEnd.wait()

    def start(self, words, times):
        if self.ser.isOpen():
            try:
                self.times = times
                self.fin = open('./test_data.log', 'w')
                self.ser.write(words.encode('utf-8'))
                self.alive = True
                self.waitEnd = threading.Event()
                self.thread_read = None
                self.thread_read = threading.Thread(target = self.get_data)
                self.thread_read.setDaemon(1)
                self.thread_read.start()
            except:
                print('open error')
            else:
                print('open successfully')

    def get_data(self):
        while (self.alive == True):
            data = ''
            data = data.encode('utf-8')
            n = self.ser.inWaiting()
            if n:
                data = data + self.ser.read(n)
                strs = str(data)
                pos = strs.find(self.keyword) #clock tick tock
                pos1 = strs.find(self.keyword2)
                pos2 = strs.find(self.keyword3)
                pos_end = strs.find(self.keyword4)
                pos3 = strs.find(self.keyword5)
                if not pos is -1:
                    self.startTime = datetime.utcnow()
                if not pos1 is -1:
                    self.endTime = datetime.utcnow()
                    interval = self.endTime - self.startTime
                    self.fin.write('fast: ' + str(round(interval.microseconds / 1000)) + '$' + '\n')
                    self.timeout = time.time()
                if not pos2 is -1:
                    self.lastTime = datetime.utcnow()
                    interval = self.lastTime - self.startTime
                    self.fin.write('last: ' + str(round(interval.microseconds / 1000)) + '$' + '\n')
                    if strs[pos2 + 8 : pos2 + 10].isdigit() is True:
                        self.fin.write('another: ' + strs[pos2 + 8] + strs[pos2 + 9] + '$' + '\n')
                if not pos3 is -1:
                    if strs[pos3 + 7 : pos3 + 13].isdigit() is True:
                        self.fin.write('total: ' + strs[pos3 + 7] + strs[pos3 + 8] + strs[pos3 + 9] + strs[pos3 + 10] + strs[pos3 + 11] + strs[pos3 + 12] + '$' + '\n')

                if not pos_end is -1:
                    sub_idx = strs.find('$')
                    if not sub_idx is -1:
                        comp_num = strs[pos_end + 7 : sub_idx]
                        print(int(comp_num))
                        if int(comp_num) >= self.times:
                            time.sleep(5)
                            # respon = self.ser.inWaiting()
                            self.ser.read(self.ser.inWaiting())
                            words = 'ac$'
                            self.ser.write(words.encode('utf-8'))
                            time.sleep(3)
                            info = self.ser.read(self.ser.inWaiting())
                            print(str(info))
                            self.alive = False
                            print('count reach')
                            self.waitEnd.set()
            else:
                pass
                interval = time.time() - self.timeout
                if not interval <= self.waitingTime:
                    self.alive = False
                    print('timeout')
                    self.waitEnd.set()

    def stop(self):
        self.alive = False
        self.thread_read.join()
        print('thread join')
        if self.ser.isOpen():
            print('serial close')
            self.ser.close()
        self.fin.close()
