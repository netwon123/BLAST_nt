#!~/bin/python3
# -*- coding: utf-8 -*-

import re
import os
import json
import pprint
import random
import argparse
import subprocess

pat1=re.compile('^\s+$')

def stat_blastn_result(blastn_result, blastn_result_stat, total_reads, dict):
    map_id = {}
    nohit = 0
    with open(blastn_result, "r") as result:
        for line in result:
            if line.strip() == '# 0 hits found':
                nohit += 1
            if line.startswith(r'#'):
                continue
            temp = line.strip().split('\t')
            temp[-2] = dict[temp[-3]]
            if temp[0] in map_id.keys():
                if temp[-2] in map_id[temp[0]] :
                    continue
                else :
                    map_id[temp[0]].append( temp[-2])
            else:
                map_id[temp[0]] = [temp[-2]]
            

    specie_dict = {}
    for key in map_id.keys() :
        for specie in map_id[key] :
            if specie in specie_dict.keys() :
                specie_dict[specie] += 1
            else :
                specie_dict[specie] = 1
    specie_dict["unknown"] = nohit
    specie_dict_order=sorted(specie_dict.items(),key=lambda x:x[1],reverse = True)

    with open(blastn_result_stat,'w') as stat:
        stat.write('Species_name\tmapping_reads\ttotal_reads\tratio\n')
        n = 0
        for item in specie_dict_order :
            min_map = total_reads * 0.001
            if item[1] < min_map :
                continue
            else :
                ratio = '{:.2%}'.format(float(item[1])/total_reads)
                stat.write("{}\t{}\t{}\t{}\n".format( item[0], item[1], total_reads, ratio))
                n += 1
                if n == 10 : break
                else : continue
                
                
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input',help='input blast out file')
    parser.add_argument('-f','--file',help='input staxid-scinames file')
    parser.add_argument('-o','--output',help='output blast stat file')
    parser.add_argument('-num','--number',help='the number of blasted reads',type=int,default=10000)
    args = parser.parse_args()
    scidict = {}
    for line in open(args.file, 'r') :
        line = line.rstrip()
        if re.match(pat1, line) : continue
        array = line.split("\t");staxid = array[0];scinames = array[1]
        scidict[staxid] = scinames
        
    stat_blastn_result( args.input, args.output, args.number, scidict)


