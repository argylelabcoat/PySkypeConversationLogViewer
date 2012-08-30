#!/usr/bin/python
import sqlite3
import argparse



if __name__=="__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("path", help="path to the skype user's main.db file")
	parser.add_argument("-u","--user",type=str, help="username with whom we want a conversation log")
	parser.add_argument("-l","--list",help="list all users with whom we have communicated",action="store_true")
	args = parser.parse_args()

	con = sqlite3.connect(args.path)
	cur = con.cursor()
	
	#list partners
	getPartners = "SELECT DISTINCT(dialog_partner) FROM Messages;"
	
	#get log for partner
	getLog = """ SELECT 
					author, 
					from_dispname, 
					datetime(timestamp, 'unixepoch') as date, 
					body_xml 
				FROM Messages where dialog_partner = '{partner}' ORDER BY timestamp """
	
	if args.user:
		query = getLog.format(partner=args.user)
		cur.execute(query)
		all = cur.fetchall()
		outputfmt = "[{time}]  {name}:\n-------------------\n{message}\n-------------------\n"
		for record in all:
			if record:
				# record is tuple: (from: acct name, from: display name, timestamp, message)
				acct,display,timestamp,message = record
				messagetext = ""		
				if message:
					messagetext = message.encode('utf-8')
				print outputfmt.format(time=timestamp,name=display,message=messagetext)
				#print record
	if args.list:
		query = getPartners
		cur.execute(query)
		all = cur.fetchall()
		for record in all:
			if record[0]:
				print str(record[0])

	
