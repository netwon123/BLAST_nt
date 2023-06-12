#! /usr/bin/env python3

#################################################################
# Extract a certain number sequences from fastq or fasta file   #
# Author: zhaohuiyao                                            #
# Date: 2022/08/26                                              #
#################################################################

import argparse
import sys
import os
import re
import random
import time



pat1=re.compile('^\s+$')

def std( level, message ):
    now_time = time.strftime("%Y-%m-%d %H:%M:%S")
    string = '{0} - {1} - {2}\n'.format( now_time, level, message )
    if level == 'ERROR':
        sys.stderr.write( string )
    else :
        sys.stdout.write( string )


def file_exists( file_or_dir ) :
    target = os.path.abspath( file_or_dir )
    if not os.path.exists( target ) :
        std( 'ERROR', '{0} is not exists , program EXIT'.format( target ) )
        sys.exit(0)
    else :
        std( 'INFO', '{0} is exists'.format( target) )
        return target


def extrac_file(infile,N,outfile,mode):
	row_index = 0;seq_dict={};IN=open(infile,"r")
	for line in IN :
		if re.match(pat1, line) : continue  
		row_index += 1
		if mode == "fq" :
			if row_index % 4 == 1: name = line.replace('@', '>');seq_dict[name]=""
			if row_index % 4 == 2: seq_dict[name]=line
		if mode == "fa" :
			if row_index % 2 == 1: name = line.replace('@', '>');seq_dict[name]=""
			if row_index % 2 == 0: seq_dict[name]=line
	keys=list(seq_dict.keys());length=len(keys);read_list=random.sample(range(0, length), N)
	for var in read_list:
		outfile.write("{}{}".format( keys[var],seq_dict[keys[var]]))
	return "good"

def main():
	parser = argparse.ArgumentParser(description='Extract a certain number sequences from fastq or fasta file')
	parser.add_argument('-i','--input',help='input fq/fa file1',required=True)
	parser.add_argument('-I','--INPUT',help='input fq/fa file2(PE data)',required=False)
	parser.add_argument('-o','--output',help='output directory',required=True)
	parser.add_argument('-out_name',help='output fastq file name',required=True)
	parser.add_argument('-f','--file',help='the type of input file(fa/fq, default=fq)',required=False,default='fq')
	parser.add_argument('-n','--number',help='extract number',required=True,type=int)
	args=parser.parse_args()
	
	number = args.number
	filename = os.path.splitext(os.path.basename(args.input))[0]
	file_exists(args.input)
	out = os.path.join(args.output, args.out_name + '_' + str(number) + '.fa')
	OUT = open(out,"w")

	if args.file == "fq" :
		if not args.INPUT :
			print ("one fastq file");extrac_file(args.input,number,OUT,args.file)
		else:
			file_exists(args.INPUT);print ("two fastq file");number=int(number/2)
			extrac_file(args.input,number,OUT,args.file);extrac_file(args.INPUT,number,OUT,args.file)

	if args.file == "fa" :
		if not args.INPUT :
			print ("one fasta file");extrac_file(args.input,number,OUT,args.file)
		else:
			file_exists(args.INPUT);print ("two fasta file");number=int(number/2)
			extrac_file(args.input,number,OUT,args.file);extrac_file(args.INPUT,number,OUT,args.file)
	
	OUT.close()

if __name__ == '__main__':
	main()
