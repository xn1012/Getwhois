
import os
import sys
import datetime
reload(sys)
sys.setdefaultencoding("utf-8")

limit = 500
FileSize = 314572800

def main():
	file = raw_input("Enter .com list file name: ")
	dir = os.getcwd()
	str0 = dir + "/input/" + file 
	str1= dir + "/out/" + file + "_whois_succeed"
	fail_list = dir + '/out/' + file + "_retry"

	timestamp = datetime.datetime.now().strftime('%m%d-%H:%M')
	#if file < 300M, then combine the results 
	if os.path.getsize(str0) < FileSize:	
		with open(str1 + '_' + timestamp, 'w') as results1:
			for i in xrange(limit):
				try:
					with open(str1 + '_' + str(i),'r') as f1:
						content1 = f1.read()
						results1.write(content1)
					os.remove(str1 + '_' + str(i))
				except Exception as e:
					continue


	with open(fail_list + '_' + timestamp, 'w') as results2:
		for i in xrange(limit):
			try:
				with open(fail_list + '_' + str(i), 'r') as f2:
					content2 = f2.read()
					results2.write(content2)
				os.remove(fail_list + '_' + str(i))
			except Exception as e:
				continue


if __name__ == "__main__":
    main()
