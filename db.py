# -*- coding: utf-8 -*-
import e32db

db = e32db.Dbms()
dbv = e32db.Db_view()
dbname = u'c:\\sms.db'


def open(name=dbname):
	try:
		db.open(name)
	except:
		db.create(name)
		db.open(name)

def init_table():
	try:
		try:
			db.execute(u"DROP TABLE smslist")
		except SymbianError, e:
			if(e.errno == -1):
				pass
			else:
				raise e
		db.execute(u"CREATE TABLE smslist (id UNSIGNED INTEGER, main VARCHAR, time float, msg VARCHAR)")
		db.execute(u"CREATE UNIQUE INDEX id_index ON smslist(id)")
	except SymbianError,e:
		if(e.errno == -11):
			#table already exists
			pass
		else:
			raise e

			
def insert(id, main, time, msg):
	try:
		sql = u"INSERT INTO smslist (id, main, time, msg) VALUES (%d, '%s', %f, '%s')" % (id, main, time, msg)
		print sql		
		db.execute(sql)
	except SymbianError,e:
		if(e.errno == -11):
			pass
		else:
			raise e
		
def select_all():
	dbv.prepare(db, u"SELECT * FROM smslist")
	result = []
	for i in range(1, dbv.count_line() + 1):
		dbv.get_line()
		row = []
		for i in range(1, dbv.col_count()+1):
			row.append(dbv.col(i))
		result.append(row)
		dbv.next_line()
	return result
	

	
def clean(beforeTimeStamp):
	sql = u"DELETE FROM smslist WHERE time <= %f" % beforeTimeStamp
	print sql
	db.execute(sql)


	

 