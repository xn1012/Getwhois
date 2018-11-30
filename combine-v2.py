
import os
import sys
import datetime
import multiprocessing
reload(sys)
sys.setdefaultencoding("utf-8")

limit = 500
FileSize = 314572800
dir0 = os.getcwd()
sub_num = multiprocessing.cpu_count()

def main():
	file = raw_input("input the orignal file name:")
	str_final= dir0 + "/out2/" + file + "_succeed"
	fail_final = dir0 + '/out2/' + file + "_retry"


	timestamp = datetime.datetime.now().strftime('%m%d')

	# for sub in xrange(sub_num):
	# 	subfile = file + '_' + str(sub)
	# 	str0 = dir0 + '/input/' + subfile

	# 	str1 = dir0 + "/out2/" + subfile + "_succeed"
	# 	fail_list = dir0 + "/out2/" + subfile + "_retry"

	# 	with open(str1, 'w') as results1:
	# 		for i in xrange(limit):
	# 			try:
	# 				with open(str1 + '_' + str(i),'r') as f1:
	# 					content1 = f1.read()
	# 					results1.write(content1)
	# 			except Exception as e:
	# 				print("err info: {} at {}_{}".format(e,str1,i))

	# 	with open(fail_list, 'w') as results2:
	# 		for i in xrange(limit):
	# 			try:
	# 				with open(fail_list + '_' + str(i), 'r') as f2:
	# 					content2 = f2.read()
	# 					results2.write(content2)
	# 			except Exception as e:
	# 				print("err info: {} at {}_{}".format(e,fail_list,i))


	if os.path.getsize(dir0+ '/input/' + file) < FileSize:
		with open(str_final, 'w') as results1:
			for i in xrange(sub_num):
				try:
					with open(dir0 + '/out2/' + file + '_' + str(i) + '_succeed','r') as f1:
						content1 = f1.read()
						results1.write(content1)
				except Exception as e:
					continue

	with open(fail_final, 'w') as results2:
		for i in xrange(sub_num):
			try:
				with open(dir0 + '/out2/' + file + '_' + str(i) + '_retry','r') as f2:
					content2 = f2.read()
					results2.write(content2)
			except Exception as e:
				continue

	print("Work done!")

if __name__ == "__main__":
    main()
