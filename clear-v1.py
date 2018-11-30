import os
from threading import Thread
from Queue import Queue

limit = 500
#source file<300M, combine succeed results
FileSize = 314572800

def Clear(file,dir0):
	global q
	while True:
		i = q.get()

		subfile = dir0  + '/out1/' + file

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
	q = Queue()
	file = raw_input("Enter file name: ")
	dir0 = os.getcwd()

	#remove mid files at /out2/
	for j in xrange(limit):
		q.put(j)

	threads = [Thread(target=Clear, args=(file,dir0)) for i in xrange(limit)]
	map(lambda x:x.setDaemon(True),threads)
	map(lambda x:x.start(),threads)
	q.join()

	print("clear work have done on file {}!".format(file))


if __name__ == "__main__":
    main()
