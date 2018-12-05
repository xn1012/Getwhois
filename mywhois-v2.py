#!/usr/bin/env python
#--*-- coding:utf-8 --*--  

import whois
import json
import os
import sys
import getopt
import collections
import socket
import multiprocessing
from threading import Thread, Lock
from Queue import Queue
import datetime
import time
import types
reload(sys)
sys.setdefaultencoding("utf-8")

limit = 500
file = None
#source file<300M, combine succeed results
FileSize = 314572800
sub_num = multiprocessing.cpu_count()
dir0 = os.getcwd()
q = Queue()
q_clear = Queue()



def mksubfile(lines, sfile, sub):
	dfile  = sfile + '_' + str(sub)
	print( "make sub file:{}".format(sub))
	with open(dfile, 'w') as fout:
		fout.writelines(lines)
	sub = sub + 1
	return sub

#full path file name 
def splitfile(file):
	print("\n splitting the file now ...")

	time_start = time.time()
	with open(file, 'r') as f0:
		for i, line in enumerate(f0):
			pass
	line_cnt = i + 1

	line_size = line_cnt / sub_num
	print("\n Total lines cnt: {}".format(line_cnt))

	sub = 0
	lines = []
	with open(file, 'r') as f0:
		for eachline in f0:	
			if len(lines) == line_size:
				if sub + 1 < int(sub_num):
					sub = mksubfile(lines, file, sub)
					lines = []
			else:
				pass
			lines.append(eachline)

		if len(lines) != 0:
			mksubfile(lines, file,sub)
		time_end = time.time()
		cost = time_end - time_start
		print("\n Split Done , cost {}".format(cost))

	return line_cnt


#file is subfile name
def Worker(i,file):
	domains = {}
	domains_failed = {}
	global q

	str1 = dir0 + "/out2/" + file + "_succeed_" + str(i)
	fail_list = dir0 + "/out2/" + file + "_retry_" + str(i)
	
	while True:
		domain = q.get()

		try:
			result = whois.whois(domain)
			#result = {"country":"test", "domain":domain, "updated_date":"null","city":"null", "expiration_date":"test","creation_date":"test"}

		except Exception as e:
			print("error:{}, at domain: {}".format(e, domain))
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

def Worker_helper(sub):
	global q

	subfile = file + '_' + str(sub)
	str0 = dir0 + '/input/' + subfile

	try:
		with open(str0, 'r')as f:
			for eachline in f:
				domain = eachline.strip()
				q.put(domain)

	except Exception as e:
		print("open subfile:{} error:{}".format(sub, e))
		exit()

	threads = [Thread(target=Worker, args=(i,subfile)) for i in xrange(limit)]
	map(lambda x:x.setDaemon(True),threads)
	map(lambda x:x.start(),threads)
	q.join()
	time.sleep(5)

	str1 = dir0 + "/out2/" + subfile + "_succeed"
	fail_list = dir0 + "/out2/" + subfile + "_retry"

	with open(str1, 'w') as results1:
		for i in xrange(limit):
			try:
				with open(str1 + '_' + str(i),'r') as f1:
					content1 = f1.read()
					results1.write(content1)
			except Exception as e:
				continue

	with open(fail_list, 'w') as results2:
		for i in xrange(limit):
			try:
				with open(fail_list + '_' + str(i), 'r') as f2:
					content2 = f2.read()
					results2.write(content2)
			except Exception as e:
				continue
	print("\n-----sub process {} is finished-----".format(sub))



def main(argv):
	global file,limit
	
	#parse the input parameters
	try:
		opts,args = getopt.getopt(argv, "-h-f:-t:", ["help","file=", "tlimit="])
	except getopt.GetoptError:
		print("test.py -f <inputfile>  -t <threadlimit>")
		sys.exit()

	for opt_name,opt_value in opts:
		if opt_name in ('-h','--help'):
			print("test.py -f <inputfile>  -t <threadlimit>")
			sys.exit()
		elif opt_name in ('-f','--file'):
			file = opt_value
		elif opt_name in ('-t','--tlimit'):
			limit = int(opt_value)
		else:
			print("test.py -f <inputfile> -t <threadlimit>")

	str0 = dir0 + '/input/' + file
	total_lines = splitfile(str0)
	
	#pool number default equal to cpu kernels, print the res
	time_start = time.time()
	pool = multiprocessing.Pool(sub_num)
	for i in xrange(sub_num):
		pool.apply_async(Worker_helper, (i,)) 
	pool.close()
	pool.join()

	time_end = time.time()
	cost1 = time_end - time_start
		
	path = dir0 + '/out2/'
	str1 = dir0 + '/out2/' + file + '_succeed'
	fail_list = dir0 + '/out2/' + file  + '_retry'
	log = dir0 + '/out2/' + file + '.log'
	#combine the result files
	
	print("\n-----combining the results now...-----")
	time_start = time.time()
	timestamp = datetime.datetime.now().strftime('%m%d')
	#if file < 300M, combining the succeed results
	if os.path.getsize(str0) < FileSize:
		with open(str1, 'w') as results1:
			for i in xrange(sub_num):
				try:
					with open(path + file + '_' + str(i) + '_succeed','r') as f1:
						content1 = f1.read()
						results1.write(content1)
				except Exception as e:
					continue

	with open(fail_list, 'w') as results2:
		for i in xrange(sub_num):
			try:
				with open(path + file + '_' + str(i) + '_retry','r') as f2:
					content2 = f2.read()
					results2.write(content2)
			except Exception as e:
				continue
	time_end = time.time()
	cost2 = time_end - time_start
	print("\nfile:{}, Total lines:{}".format(file, total_lines))
	print("\nV2:Total time used to query and save: {}, combine:{}".format(cost1,cost2))
    with open(log, 'w') as flog:
    	flog.write("\nmywhois-V2: file {}, total lines {}, query time: {} s, combine time: {} s".format(file, total_lines, cost1, cost2))
	Clear_helper()


def Clear_helper():
	#remov subfiles and _succeed & _retry
	global q_clear
	str0 = dir0 + '/input/' + file

	time_start = time.time()
	#remove mid files by multi-thread at /out2/
	for j in xrange(limit):
		q_clear.put(j)

	threads = [Thread(target=Clear, args=(file,)) for j in xrange(limit)]
	map(lambda x:x.setDaemon(True),threads)
	map(lambda x:x.start(),threads)
	q.join()
	time.sleep(5)

	for i in xrange(sub_num):
		subfile = dir0 + '/input/' + file + '_' + str(i)
		str1 = dir0 + '/out2/' + file + '_' + str(i) + '_succeed'
		str2 = dir0 + '/out2/' + file + '_' + str(i) + '_retry'
		#if file < 300M, results have combined,so del the sub succeed files
		if os.path.getsize(str0) < FileSize:	
			try:
				os.remove(str1)
			except Exception as e:
				pass
		try:
			os.remove(str2)
		except Exception as e:
			pass
		try:
			os.remove(subfile)
		except Exception as e:
			pass

	time_end = time.time()
	cost = time_end - time_start
	print("\nV2: clear work have done on file {},cost:{}!".format(file, cost))

def Clear(file):
	global q_clear
	while True:
		i = q_clear.get()

		for j in xrange(sub_num):
			subfile = dir0  + '/out2/' + file + '_' + str(j)
			try:
				os.remove(subfile +  '_succeed_' + str(i))
			except Exception as e:
				pass
			try:
				os.remove(subfile + '_retry_' + str(i))
			except Exception as e:
				pass
			#print("file{} sub: {}'s {}/500  files deleted".format(file, j, i))
		q_clear.task_done()


if __name__ == "__main__":
    main(sys.argv[1:])