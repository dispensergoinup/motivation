'''
DB Adaptor - TEST VERSION
Responsible for taking stored data and converting it to generic format for the motivator.

V1.0
'''
import json
from datetime import datetime, timedelta

DB_TZ_OFFSET = -4

class Database():
	def __init__(self):
		self.jreports = json.load(open('reports.json','r'))
		self.reports = []
		for report in self.jreports:
			report['time'] = datetime.strptime(report['time'],'%Y-%m-%d %H:%M:%S')
			#Convert to UTC
			report['time'] = report['time']-timedelta(hours=DB_TZ_OFFSET)
			self.reports.append(report)
			
		self.jgoals = json.load(open('goals.json','r'))
		self.goals = []
		for goal in self.jgoals:
			goal['timeframe']=timedelta(days=goal['timeframe'])
			self.goals.append(goal)
	
	def getReports(self, type, start, end):
		r = []
		for report in self.reports:
			if report['type'] == type and report['time'] >= start and report['time'] <= end:
				r.append(report)
		
		return r
			
	def getGoals(self):
		return self.goals
		
	def writeBank(self,type, value):
		bank = json.load(open('bank.json','r'))
		bank.append({'type':type,'value':value,'time':(datetime.utcnow()+timedelta(hours=DB_TZ_OFFSET)).strftime('%Y-%m-%d %H:%M:%S')})
		json.dump(bank,open('bank.json','w'))
		
	def getBank(self,type):
		bank = json.load(open('bank.json','r'))
		date = datetime.min
		latest = None
		for item in bank:
			item['time'] = datetime.strptime(item['time'],'%Y-%m-%d %H:%M:%S')
			#Convert to UTC
			item['time'] = item['time']-timedelta(hours=DB_TZ_OFFSET)
			if item['type'] == type and item['time'] >= date:
				latest = item
				date = item['time']
		return latest
		
	def closeDB(self):
		pass
		
'''			
d = Database()
r = d.getReports('cal',datetime.utcnow()-timedelta(days=120),datetime.utcnow())
s = 0
for report in r:
	s+=report['value']
print s/len(r)
'''