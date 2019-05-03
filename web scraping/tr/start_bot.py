import schedule
import time,sys,re,os
from xml.dom.minidom import parse, parseString



def job1():
	full_path = os.path.realpath(__file__)
	curr_dir = os.path.dirname(full_path)
	bot_name =  os.path.basename(curr_dir)
	print "Staring Datext Bot with name %s" %(bot_name)
	os.chdir(r"%s" %(curr_dir))
	os.system("python clientpull.py")

job1()
schedule.every(1).minutes.do(job1)

while True:
	schedule.run_pending()
	time.sleep(1)
