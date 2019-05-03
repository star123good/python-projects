# -*- coding: utf-8 -*-
import smtplib

def send_mail(toaddrs,situationRecordCreationTime,overallEndTime,type,road,County,where,message,status,latitude,longitude,country_full):
	fromaddr = 'handelseinformation@dagsmedia.se'
        msg = """From: <handelseinformation@dagsmedia.se>
Content-Type: text/plain; charset="utf-8" 
To: <%s>
Subject: %s

Startid: %s
Sluttid: %s
Typ: %s
Väg: %s
Län: %s
Vart: %s
Meddelande: %s
Status: %s
Karta:https://www.google.com/maps?q=%s,%s
Position: %s
Dagsmedia Händelseinformation""" % (toaddrs,'Trafikinformation',situationRecordCreationTime,overallEndTime,type.encode('utf-8'),road.encode('utf-8'),County.encode('utf-8'),where.encode('utf-8'),message.encode('utf-8'),status.encode('utf-8'),latitude,longitude,country_full.encode('utf-8'))
        print msg
	server = smtplib.SMTP('mail.dagsmedia.se:587')  
	server.starttls()
	username = 'handelseinformation@dagsmedia.se'
	password = 'kSVvJ4AF0p'
	server.login(username,password)
	reply = server.sendmail(fromaddr, toaddrs, msg)
	server.quit()

