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
		self.json = json.load(open('reports.json','r'))
		self.reports = []
		for report in self.json:
			report['time'] = datetime.strptime(report['time'],'%Y-%m-%d %H:%M:%S')
			#Convert to UTC
			report['time'] = report['time']-timedelta(hours=DB_TZ_OFFSET)
			self.reports.append(report)
	
	def getReports(self, type, start, end):
		r = []
		for report in self.reports:
			if report['type'] == type and report['time'] >= start and report['time'] <= end:
				r.append(report)
		
		return r
				
d = Database()
r = d.getReports('cal',datetime.utcnow()-timedelta(days=120),datetime.utcnow())
s = 0
for report in r:
	s+=report['value']
print s/len(r)