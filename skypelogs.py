#!/usr/bin/python
import sqlite3
import argparse

def getLog(partner, path):
	con = sqlite3.connect(path)
	cur = con.cursor()
	#
	log = []
	#get log for partner
	getLog = """ SELECT 
					author, 
					from_dispname, 
					datetime(timestamp, 'unixepoch') as date, 
					body_xml 
				FROM Messages where dialog_partner = '{partner}' ORDER BY timestamp """
	query = getLog.format(partner=partner)
	cur.execute(query)
	all = cur.fetchall()
	for record in all:
		if record:
			# record is tuple: (from: acct name, from: display name, timestamp, message)
			acct,display,timestamp,message = record
			messagetext = ""		
			if message:
				messagetext = message.encode('utf-8')
			log.append( {'time':timestamp, 'name':display, 'message':messagetext } )
	con.close()
	return log

def getPartners(path):	
	con = sqlite3.connect(path)
	cur = con.cursor()
	#
	partners = []
	#list partners
	getPartners = "SELECT DISTINCT(dialog_partner) FROM Messages;"
	query = getPartners
	cur.execute(query)
	all = cur.fetchall()
	for record in all:
		if record[0]:
			partners.append(str(record[0]))
	con.close()
	return partners



if __name__=="__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("path", help="path to the skype user's main.db file")
	parser.add_argument("-u","--user",type=str, help="username with whom we want a conversation log")
	parser.add_argument("-l","--list",help="list all users with whom we have communicated",action="store_true")
	args = parser.parse_args()

	
	if args.user:
		outputfmt = "[{time}]  {name}:\n-------------------\n{message}\n-------------------\n"
		log = getLog(args.user,args.path)
		for record in log:
			print outputfmt.format(\
				time=record['time'],\
				name=record['name'],\
				message=record['message'])
	if args.list:
		partners = getPartners(args.path)
		for partner in partners:
			print partner 

	
