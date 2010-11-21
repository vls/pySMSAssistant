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

limit = 50
txNum = "10657558022909"
if(e32.in_emulator()):
	txNum = "700"

def get_period_time_stamp():
	t = datetime.datetime.now()
	t = t - datetime.timedelta(days = 2)
	t = t.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
	stamp = time.mktime(t.timetuple())
	return stamp

def delete_msg():
	stamp = get_period_time_stamp()
	
	inb = inbox.Inbox()
	count = 0
	i = 0
	for id in inb.sms_messages():
		if(i > limit):
			print "Exceed limit"
			break
		i+=1
		if(inb.address(id) != txNum):
			continue
		
		if(inb.time(id) < stamp):
			inb.delete(id)
			count += 1
	
	return count
    


try:
    print "haha"
    print delete_msg()
except:
    import sys
    import traceback
    import appuifw
    cla, exc, trbk = sys.exc_info()
    excName = cla.__name__
    try:
        excArgs = exc.args
    except KeyError:
        excArgs = "<no args>"
    excTb = traceback.format_tb(trbk, 5)
    errorString = repr(excName) + '-' + repr(excArgs) + '-' + repr(excTb) + '\n'
    print errorString
    appuifw.note(u'Application errors, see log file for more information', "error")
    file = open(u'C:\\Log.txt','a')
    file.write(errorString)
    file.close()
    raise