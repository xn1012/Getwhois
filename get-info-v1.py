import os
import json
import sys
import types
import codecs
import time
reload(sys)
sys.setdefaultencoding("utf-8")

dir0 = os.getcwd()

def main():
	file = raw_input("please input the output file name at ./")

	directory = './info'
	if not os.path.exists(directory):
		os.makedirs(directory)

	org = []
	registrar = []
	emails = []
	#get the org , registrar, emails record, to each file		
	with open(file, 'r') as f0:
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

	with open('./info/' + file + '_' + 'org', 'w') as fout1:
		fout1.writelines(org)
	with open('./info/' + file + '_' + 'registrar', 'w') as fout2:
		fout2.writelines(registrar)
	with open('./info/' + file + '_' + 'emails', 'w') as fout3:
		fout3.writelines(emails)


if __name__ == "__main__":
    main()