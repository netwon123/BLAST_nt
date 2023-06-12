#!~/bin/python3
# -*- coding: utf-8 -*-

import re
import os
import json
import pprint
import random
import argparse
import subprocess

__author__='zhao huiyao'
__mail__= 'zhaohuiyao@snnu.edu.cn'

pat1=re.compile('^\s+$')


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter,epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
    parser.add_argument('-i','--input',help='input names.dmp file')
    parser.add_argument('-o','--output',help='output directory')
    args = parser.parse_args()
    out1 = os.path.join( args.output, "staxid-scinames.txt")
    OUT1 = open(out1, 'w')
    mydict = {}
    for line in open( args.input, 'r') :
        line = line.rstrip()
        if re.match(pat1, line) : continue
        if re.search('scientific name', line) :
            array = line.split("\t");staxid = array[0];scinames = array[2]
            OUT1.write("{}\t{}\n".format( staxid, scinames))
	
	
