 # -*- coding: utf-8 -*-
import inbox, messaging, e32
import sys, os
try:
    raise Exception
except Exception:
    mydir = os.path.dirname(sys.exc_info()[2].tb_frame.f_code.co_filename)
if not mydir:
    mydir = os.getcwd()

sys.path.append(mydir)

#sys.path.append(u"c:\\Data\\python")
import mktimefix as time
import datetime
import db
from operator import itemgetter



limit = 500
txNum = "1065502055203"
if(e32.in_emulator()):
	txNum = "700"

def read_all():
	inb = inbox.Inbox()
	msgs = inb.sms_messages()
	i = 0
	max = len(msgs)
	count = 0
	for i in range(max):
		id = msgs[i]
	
		if (i >= limit):
			break
		
		if (inb.address(id) != txNum):
			continue
		
		if(inb.unread(id)):
			# 0 = read
			inb.set_unread(id, 0)
			count += 1
	
	return count
	

def process_msg():

	db.open()
	try:
		stamp = get_period_time_stamp()
		inb = inbox.Inbox()
		i=0
		
		msgs = inb.sms_messages()
		count = len(msgs)
		for i in range(count):
			if(i >= limit):
				break
			
			id = msgs[i]
			
			if(inb.address(id) != txNum):
				continue
			
			t = inb.time(id)
			
			if(t < stamp):
				#too early msg
				break
			#print t
			#print strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
			msg = inb.content(id)
			
			msg = msg.rstrip(u"【腾讯科技】")
			
			if(msg[:4] == "2/2)"):
				continue
				
			elif(msg[:4] == "1/2)"):
				if(i != 0):
					# i != 0, indicates that we already have both two pieces of the whole message
					newmsg = msg[4:] + inb.content(msgs[i-1])[4:].rstrip(u"【腾讯科技】")
			else:
				newmsg = msg
			
			msgArr = newmsg.split("|")
			
			if(len(msgArr) >= 2):
				main = msgArr[1]
				db.insert(id, main, inb.time(id), newmsg)
			
			
	finally:
		db.db.close()

def get_period_time_stamp():
	t = datetime.datetime.now()
	t = t - datetime.timedelta(hours = 12)
	#t = t.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
	stamp = time.mktime(t.timetuple())
	return stamp
			
def delete_msg():
	stamp = get_period_time_stamp()
	
	inb = inbox.Inbox()
	count = 0
	for id in inb.sms_messages():
		if(inb.address(id) != txNum):
			continue
		
		if(inb.time(id) < stamp):
			inb.delete(id)
			count += 1
	print count
	return count
	
			
	
def clean_db():
	db.open()
	try:
		stamp = get_period_time_stamp()
		db.clean(stamp)
	finally:
		db.db.close()

def select_db():
	db.open()
	try:
		db.select_all()
	finally:
		db.db.close()

def init_db():
	db.open()
	try:
		db.init_table()
	finally:
		db.db.close()

def dictCmp(a, b):
	print a
	return a[0] < b[0]

class MsgSummary:
	def __init__(self):
		self.msg = u''
		self.prefix_msg = u''
		self.time = 0
		self.id_list = []

def get_time_list(id_list):
	inb = inbox.Inbox()
	time_list = [inb.time(id) for id in id_list]
	sorted(time_list)
	time_list = [time.strftime("%d %H:%M", time.localtime(t)) for t in time_list]
	return time_list
	
def select_top_db():
	db.open()
	dict = {}
	try:
		result = db.select_all()
		for row in result:
			if(not dict.has_key(row[1])):
				summary = MsgSummary()
				summary.msg = row[3]
				summary.prefix_msg = row[1]
				summary.time = row[2]
				summary.id_list = [row[0]]
				
				
				dict[row[1]] = [1, summary]
			else:
				dict[row[1]][0] += 1
				dict[row[1]][1].id_list.append(row[0])	
		
		happenList = []
		
		for k,v in dict.items():
			
			happenList.append((v[0], v[1].time, v[1]))
	finally:
		db.db.close()
	print happenList
	happenList = sorted(happenList, key=itemgetter(0,1) , reverse=True)
	print happenList
	return happenList

if __name__ == "__main__":
	print "sms"
	print get_period_time_stamp()
