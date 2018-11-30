#!/usr/bin/env python  
#--*-- coding:utf-8 --*--  

import whois
import json
import os
import sys
import getopt
import collections
import socket
from threading import Thread, Lock
from Queue import Queue
import datetime
import time
import types
reload(sys)
sys.setdefaultencoding("utf-8")


q = Queue()
limit = 500
#source file<300M, combine succeed results
FileSize = 314572800

def Worker(i,file):
	domains = {}
	domains_failed = {}

	global q
	dir = os.getcwd()
	str1 = dir + "/out1/" + file + "_succeed_" + str(i)
	fail_list = dir + '/out1/' + file + "_retry_" + str(i)
	
	while True:
		domain = q.get()

		try:
			result = whois.whois(domain)
		except socket.error as e:
			print("The socket has error :{}, at domain: {}".format(e,domain))
			with open(fail_list,'a') as retry:
				retry.write(domain + '\n')
			continue

		except Exception as e:
			print("Other error:{} occured, at domain: {}".format(e, domain))
			with open(fail_list,'a') as retry:
				retry.write(domain + '\n')
			continue

		else:
			print("The domain {}'s whois info:\n{}".format(domain,result))

			#covert the update datetime to string ready for json dumps
			if isinstance(result["updated_date"], types.ListType):
				if isinstance(result["updated_date"][0], datetime.datetime):
					strtime = result["updated_date"][0].strftime('%Y%m%d')
				else:
					strtime = result["updated_date"][0]
			elif isinstance(result["updated_date"], datetime.datetime):
				strtime = result["updated_date"].strftime('%Y%m%d')
			else:
				strtime = result["updated_date"]
			result["updated_date"] = strtime

			#covert the expiration datetime to string ready for json dumps
			if isinstance(result["expiration_date"], types.ListType):
				if isinstance(result["expiration_date"][0], datetime.datetime):
					strtime = result["expiration_date"][0].strftime('%Y%m%d')
				else:
					strtime = result["expiration_date"][0]
			elif isinstance(result["expiration_date"], datetime.datetime):
				strtime = result["expiration_date"].strftime('%Y%m%d')
			else:
				strtime = result["expiration_date"]
			result["expiration_date"] = strtime

			#covert the creation datetime to string ready for json dumps
			if isinstance(result["creation_date"], types.ListType):
				if isinstance(result["creation_date"][0], datetime.datetime):
					strtime = result["creation_date"][0].strftime('%Y%m%d')
				else:
					strtime = result["creation_date"][0]
			elif isinstance(result["creation_date"], datetime.datetime):
				strtime = result["creation_date"].strftime('%Y%m%d')
			else:
				strtime = result["creation_date"]
			result["creation_date"] = strtime

			domains[domain]= collections.OrderedDict()
			domains[domain] = result
			with open(str1, 'a') as results1:
				results1.write(json.dumps(domains) + '\n')
			domains.clear()
			
		
		finally:
			q.task_done()	




def main(argv):
	global q,limit

	try:
		opts,args = getopt.getopt(argv, "-h-f:-t:", ["help","file=", "tlimit="])
	except getopt.GetoptError:
		print("test.py -f <inputfile> -t <threadlimit>")
		sys.exit()

	for opt_name,opt_value in opts:
		if opt_name in ('-h','--help'):
			print("test.py -f <inputfile> -t <threadlimit>")
			sys.exit()
		elif opt_name in ('-f','--file'):
			file = opt_value
		elif opt_name in ('-t','--tlimit'):
			limit = int(opt_value)
		else:
			print("test.py -f <inputfile> -t <threadlimit>")
	
	time_start = time.time() 
	dir = os.getcwd()
	str0 = dir + '/input/' + file
	print("\nPut the list into the queue")
	with open(str0, 'r')as f:
		for eachline in f:
			domain = eachline.strip()
			q.put(domain)
	time_end = time.time()
	cost = time_end - time_start
	print("\nQueued time cost:{}".format(cost))

	threads = [Thread(target=Worker, args=(i,file)) for i in xrange(limit)]
	map(lambda x:x.setDaemon(True),threads)
	map(lambda x:x.start(),threads)
	q.join()

	
	str1= dir + "/out1/" + file + "_succeed"
	fail_list = dir + "/out1/" + file + "_retry"
	#combine the files on each thread
	timestamp = datetime.datetime.now().strftime('%m%d') 
	#if not >300M , combine the succeed results
	if os.path.getsize(str0) < FileSize:
		with open(str1, 'w') as results1:
			for i in xrange(limit):
				try:
					with open(str1 + '_' + str(i),'r') as f1:
						content1 = f1.read()
						results1.write(content1)
				except Exception as e:
					continue

	with open(fail_list, 'w') as results3:
		for i in xrange(limit):
			try:
				with open(fail_list + '_' + str(i), 'r') as f3:
					content3 = f3.read()
					results3.write(content3)
			except Exception as e:
				continue
	
	time_end = time.time()
	cost = time_end - time_start
	print("\nVer1:Total time used to query: {}".format(cost))
	Clear(file,str0)



def Clear(file, str0):
	print("\n---clearing the temp files---")
	dir = os.getcwd()
	str1= dir + "/out1/" + file + "_succeed"
	fail_list = dir + "/out1/" + file + "_retry"
	for i in xrange(limit):
		#if input file <300M , results combined,so del mid files 
		if os.path.getsize(str0) < FileSize:
			try:
				os.remove(str1 + '_' + str(i))
			except Exception as e:
				pass
		try:
			os.remove(fail_list + '_' + str(i))
		except Exception as e:
			pass
		#print("clear {}_{}'s succeed & retry files".format(file, i))
	print("\nclear work have done on file {}!".format(file))


if __name__ == "__main__":
    main(sys.argv[1:])