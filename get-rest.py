#!/usr/bin/env python
#--*-- coding:utf-8 --*--  
import os
import sys
import getopt



def main(argv):
    #parse the input parameters
    try:
        opts,args = getopt.getopt(argv, "-h-a:-s:", ["help","fileall=", "filesuc="])
    except getopt.GetoptError:
        print("test.py -a <input domain list>  -s <success domain list>")
        sys.exit()

    for opt_name,opt_value in opts:
        if opt_name in ('-h','--help'):
            print("test.py -a <input domain list>  -s <success domain list>")
            sys.exit()
        elif opt_name in ('-a','--fileall'):
            file1 = opt_value
        elif opt_name in ('-s','--filesuc'):
            file2 = opt_value
        else:
            print("test.py -a <input domain list>  -s <success domain list>")


    list_all = []
    with open(file1, 'r') as a:
    	for eachline in a:
    		domain = eachline.strip()
    		list_all.append(domain + '\n')

    list_suc = []
    with open(file2, 'r') as s:
    	for eachline in s:
    		domain = eachline.strip()
    		list_suc.append(domain + '\n')


    list_rest = []
    list_rest = list(set(list_all).difference(set(list_suc)))

    with open(file1 + "_rest", 'w') as f3:
    	f3.writelines(list_rest)


if __name__ == "__main__":
    main(sys.argv[1:])