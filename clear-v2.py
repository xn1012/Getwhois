import os
from threading import Thread
from Queue import Queue
import multiprocessing

limit = 500
#source file<300M, combine succeed results
FileSize = 314572800
sub_num = multiprocessing.cpu_count()
dir0 = os.getcwd()
q = Queue()

def Clear(file):
	global q
	while True:
		i = q.get()
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

		q.task_done()



def main():	
	global q

	file = raw_input("Enter file name: ")
	str0 = dir0 + '/input/' + file

	#remove mid files at /out2/
	for j in xrange(limit):
		q.put(j)

	threads = [Thread(target=Clear, args=(file,)) for j in xrange(limit)]
	map(lambda x:x.setDaemon(True),threads)
	map(lambda x:x.start(),threads)
	q.join()

	#remov subfiles and _succeed & _retry
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
		print("remove subfile{} and its secceed&retry files\n".format(i))


	print("clear work have done on file {}!".format(file))


if __name__ == "__main__":
    main()
