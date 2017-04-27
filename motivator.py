from dbadaptor import Database
from datetime import datetime
import argparse

def updateBank(db):
	print "Updating Bank"
	datenow = datetime.utcnow()
	#datenow = datetime.strptime('2017-04-13 06:00:00','%Y-%m-%d %H:%M:%S')
	goals = db.getGoals()
	for goal in goals:
		print "Checking goal %s"%goal['name']
		bank = db.getBank(goal['type'])
		if bank is None:
			continue
		elif datenow.date()-goal['timeframe'] >= bank['time'].date():
			print "Goal %s in range, updating..."%goal['name']
			reports = db.getReports(goal['type'],datenow-goal['timeframe'],datenow)
			total = 0
			for report in reports:
				total += report['value']
			
			diff = total - goal['bestcase']
			if goal['bestcase'] < goal['worstcase']:
				diff *= -1
			
			bank['value'] += diff
			print goal['name'],total,bank['value']
			db.writeBank(goal['type'],bank['value'])

parser = argparse.ArgumentParser(description='Run Motivator Commands')
parser.add_argument('--action', help='Define the action')

args = parser.parse_args()
	
d = Database()
	
if args.action == 'bank':
	updateBank(d)

d.closeDB()