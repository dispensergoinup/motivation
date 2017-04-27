from dbadaptortest import Database
from datetime import datetime
import argparse
import xml.etree.ElementTree as et

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

def generateReport(db):
	def goalSection(goal):
		return et.Element('br')
		
	#outfile = r'/home/cmocho/public_html/weightloss/index.htm'
	outfile = r'index.htm'
	
	root = et.Element('html')
	html = et.ElementTree(element=root)
	
	head = et.Element('head')
	meta = et.Element('meta')
	meta.attrib['name'] = "viewport"
	meta.attrib['content'] = "width=device-width, initial-scale=1"
	head.append(meta)
	
	body = et.Element('body')
	
	goals = db.getGoals()
	for goal in goals:
		body.append(goalSection(goal))
	
	foot = et.Element('br')
	foot.text = str(datetime.now())
	
	body.append(foot)
	
	root.append(head)
	root.append(body)
	
	html.write(outfile)
	
parser = argparse.ArgumentParser(description='Run Motivator Commands')
parser.add_argument('--action', help='Define the action')

args = parser.parse_args()
	
d = Database()
	
if args.action == 'bank':
	updateBank(d)
elif args.action == 'report':
	generateReport(d)

d.closeDB()