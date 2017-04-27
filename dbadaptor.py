import sys
sys.path.insert(0, '/home/cmocho/scripts/')
import mysql.connector
from datetime import datetime, timedelta

DB_TZ_OFFSET = -4

class Database():
	def __init__(self):
		self.config = 'dbconfig.txt'
		self.loadConfig()
		self.cnx = mysql.connector.connect(user=self.user, password=self.password,host=self.host,database=self.db)
		self.cursor = self.cnx.cursor()

	def loadConfig(self):
		conf = open(self.config,'r')
		conf = conf.read().splitlines()
		self.user = conf[0]
		self.password = conf[1]
		self.host = conf[2]
		self.db = conf[3]
		
	
	def getReports(self, type, start, end):
		#Convert to local
		start=start+timedelta(hours=DB_TZ_OFFSET)
		end=end+timedelta(hours=DB_TZ_OFFSET)
		query = ("SELECT id,time,type,value FROM reports WHERE type = %s AND time BETWEEN %s AND %s")
		self.cursor.execute(query,(type,start,end))
		r = []
		for id,time,type,value in self.cursor:
			nr = {}
			#Convert to UTC
			nr['time'] = time-timedelta(hours=DB_TZ_OFFSET)
			nr['id'] = id
			nr['type'] = type
			nr['value'] = value
			r.append(nr)
		
		return r
			
	def getGoals(self):
		query = ("SELECT id,type,name,bestcase,worstcase,minreports,timeframe,units FROM goals")
		self.cursor.execute(query)
		r = []
		for id,type,name,bestcase,worstcase,minreports,timeframe,units in self.cursor:
			nr = {}
			#Convert to UTC
			nr['name'] = name
			nr['id'] = id
			nr['type'] = type
			nr['bestcase'] = bestcase
			nr['worstcase'] = worstcase
			nr['minreports'] = minreports
			nr['timeframe'] = timedelta(days=timeframe)
			nr['units'] = units
			r.append(nr)
		
		return r
		
	def writeBank(self,type, value):
		query = ("INSERT INTO bank (value, type) VALUES (%s, %s)")
		self.cursor.execute(query,(value,type))
		
	def getBank(self,type):
		query = ("SELECT id,time,type,value FROM bank WHERE type = %s ORDER BY time DESC LIMIT 1")
		self.cursor.execute(query,(type,))
		bank = None
		for id,time,type,value in self.cursor:
			bank = {}
			bank['id'] = id
			bank['time'] = time-timedelta(hours=DB_TZ_OFFSET)
			bank['type'] = type
			bank['value'] = value
			break
		
		return bank
		
	def closeDB(self):
		self.cursor.close()
		self.cnx.close()


