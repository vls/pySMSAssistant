 # -*- coding: utf-8 -*-
import appuifw, e32

import sys, os
try:
    raise Exception
except Exception:
    mydir = os.path.dirname(sys.exc_info()[2].tb_frame.f_code.co_filename)
if not mydir:
    mydir = os.getcwd()

sys.path.append(mydir)


import sms

app_lock = e32.Ao_lock()
happenList = []
def quit():
	global app_lock
	app_lock.signal()



def select_handler():
	global happenList
	txt = items[lb.current()][0] + u" selected"
	time_list = sms.get_time_list(happenList[lb.current()][2].id_list)
	appuifw.note(happenList[lb.current()][2].msg + "|" + "|".join(time_list))

def process_msg():
	sms.process_msg()
	items = get_listbox_items()
	appuifw.app.body.set_list(items)
	appuifw.note(u"preprocessing completed")

def read_all():
	count = sms.read_all()
	appuifw.note(u"%d items set readed" % count)

def delete_msg():
	count = sms.delete_msg()
	appuifw.note(u"%d items deleted" % count)

def clean_db():
	sms.clean_db()
	items = get_listbox_items()
	appuifw.app.body.set_list(items)
	appuifw.note(u"clean db succeeded")

def init_db():
	sms.init_db()
	items = get_listbox_items()
	appuifw.app.body.set_list(items)
	appuifw.note(u"init db succeeded")
	

def get_listbox_items():
	global happenList
	try:
		happenList = sms.select_top_db()
	except SymbianError,e:
		if(e.errno == -1):
			sms.init_db()
			happenList = sms.select_top_db()

	items = [u"%d|" % x[0] + x[2].msg for x in happenList]

	if(len(items) == 0):
		items.append(u"无记录")
	
	return items
	
appuifw.app.exit_key_handler = quit	
items = get_listbox_items()
lb = appuifw.Listbox(items, select_handler)
appuifw.app.body = lb
appuifw.app.menu = [(u"预处理短信", process_msg), (u"删除12小时前短信", delete_msg), (u"标记所有已读", read_all), (u"清理DB 2天前记录", clean_db), (u"清空DB", init_db)]

app_lock.wait()