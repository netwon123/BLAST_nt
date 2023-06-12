#!~/bin/python3
# -*- coding: utf-8 -*-

import re
import os
import json
import pysam
import pprint
import random
import argparse
import subprocess



def stat_blastn_result(blastn_result, blastn_result_stat, total_reads):
    map_id = {}
    nohit = 0
    with open(blastn_result, "r") as result:
        for line in result:
            if line.strip() == '# 0 hits found':
                nohit += 1
            if line.startswith(r'#'):
                continue
            temp = line.strip().split('\t')
            if temp[-3] in map_id:
                map_id[temp[-3]] += 1
            else:
                map_id.update({temp[-3]:1})
            for sub in result:
                if sub.startswith(r'#'):
                    break

    map_id['unknown'] = nohit

    with open(blastn_result_stat,'w') as stat:
        stat.write('Species_name\tmapping_reads\tratio\n')
        n = 0
        for subject, num in sorted(map_id.items(), key=lambda x:x[1], reverse=True):
            n += 1
            if n <= 10:
                ratio = '{:.2%}'.format(float(num)/total_reads)
                stat.write(str(subject)+'\t'+str(num)+'\t'+ratio+'\n')
            else:
                break
                
                
                
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input',help='input blast out file')
    parser.add_argument('-o','--output',help='output blast stat file')
    parser.add_argument('-num','--resds number',help='total reads',type=int,default=10000)
    args = parser.parse_args()
    stat_blastn_result( args.input, args.output, args.num)


