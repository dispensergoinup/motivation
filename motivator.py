from dbadaptortest import Database
from datetime import datetime

def updateBank(db):
	#datenow = datetime.utcnow()
	datenow = datetime.strptime('2017-04-13 06:00:00','%Y-%m-%d %H:%M:%S')
	goals = db.getGoals()
	for goal in goals:
		reports = db.getReports(goal['id'],datenow-goal['timeframe'],datenow)
		total = 0
		for report in reports:
			total += report['value']
		bank = db.getBank(goal['id'])
		diff = total - goal['bestcase']
		if goal['bestcase'] < goal['worstcase']:
			diff *= -1
		
		bank += diff
		print goal['name'],total,bank
		db.writeBank(goal['id'],bank)

d = Database()
updateBank(d)