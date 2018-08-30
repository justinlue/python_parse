#!/usr/bin/env python
# encoding: utf-8
"""
@author: Elijah Luo
@file: parse.py
@time: 2018/26/01
"""
from fileact import File_act
from serialact import Serial_port
import getopt, sys

def usage():
    print("python parse.py -p COM22 -c calculate -n nodes -t timeout")

if __name__ == '__main__':

    opts, args = getopt.getopt(sys.argv[1:], "hp:c:n:t:")
    calculate = 0
    nodes = 0
    timeout = 0
    com=""

    for op, value in opts:
        if op == "-c":
            calculate = value
        elif op == "-n":
            nodes = value
        elif op == "-p":
            com = value
        elif op == "-t":
            timeout = value
        elif op == "-h":
            usage()
            sys.exit()

    print("calculate: " + calculate + " nodes: " + nodes + " port: " + com +
          " timeout: " + timeout)
    m_ser = Serial_port(com, 115200, int(timeout)) # last parameter is timeout
    m_ser.set_keywords('start', 'getack', 'another', 'trid = ', 'gettot')
    m_ser.start('0103ffff01010a$', calculate) # last parameter is number for calculating
    m_ser.waiting()
    m_ser.stop()

    parse = File_act(0, 1000, nodes) #set initial value and total nodes excluding switch node
    parse.set_keywords('fast: ', 'last: ', '$', 'another: ', 'total: ')
    parse.new_find_keyword('./test_data.log', './after_data.log')
