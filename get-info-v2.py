#!/usr/bin/env python
#--*-- coding:utf-8 --*--  

import os
import json
import sys
import types
import codecs
import time

#source file<300M, combine succeed results
FileSize = 314572800
dir0 = os.getcwd()

def main():
	file = raw_input("please input the origal file name at /input/: ")
	num = raw_input("please input the sub_num: ")
	sub_num = int(num)
	str0 = dir0 + '/input/' + file

	directory = dir0 + '/info/'
	if not os.path.exists(directory):
		os.makedirs(directory)

	#get the org , registrar, emails record, to each file
	for sub in xrange(sub_num):
		subfile = file + '_' + str(sub) + '_succeed'
		org = []
		registrar = []
		emails = []
		with open(subfile, 'r') as f0:
			for eachline in f0:
				record = json.loads(eachline.strip())
				#each line in the file has only one domain record
				try:
					for key1 in record.keys():
						whois = record[key1]
						#whois information dict
						for key2 in whois.keys():
							if key2 == "org":	
								if not whois[key2]:
									org.append("null\n")
								elif isinstance(whois[key2], types.ListType):
									for i,val in enumerate(whois[key2]):
										item = val.encode('utf-8')
										org.append(item + '\n')
								else:
									item = whois[key2].encode('utf-8')
									org.append(item + '\n')

							elif key2 == "registrar":	
								if not whois[key2]:
									registrar.append("null\n")
								else:
									item = whois[key2].encode('utf-8')
									registrar.append(item + '\n')

							elif key2 == "emails":	
								if not whois[key2]:
									emails.append("null\n")
								elif isinstance(whois[key2], types.ListType):
									for i, val in enumerate(whois[key2]):
										item = val.encode('utf-8')
										emails.append(item + '\n')
								else:
									item = whois[key2].encode('utf-8')
									emails.append(item + '\n')
								print(item + '\n')
										
				except Exception as e:
					print("\nerror {} occured at {}".format(e, whois["domain_name"]))
					with open('./info/' + file + '_' + 'retry', 'a') as fout4:
						fout4.write(eachline)

		with open('./info/' + file + '_' + 'org', 'a') as fout1:
			fout1.writelines(org)
		with open('./info/' + file + '_' + 'registrar', 'a') as fout2:
			fout2.writelines(registrar)
		with open('./info/' + file + '_' + 'emails', 'a') as fout3:
			fout3.writelines(emails)


if __name__ == "__main__":
    main()