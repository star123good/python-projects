# -*- coding: utf-8 -*-
from requests.auth import HTTPBasicAuth
import requests
from xml.dom.minidom import parse, parseString
import time
import MySQLdb as DBA
import email
import datetime
import time
import traceback
import unicodedata as ud
import smtplib
import datext_mailer
import logging


import xml.etree.ElementTree as ET

#accident_url = 'https://datex.trafikverket.se/d2ClientPull/situationpullserverBA/2_0/AccidentService/AccidentService.asmx/getDatex2Data'

accident_url = 'https://datex.trafikverket.se/D2ClientPull/SituationPullServerBA/2_3/Accident'

user_name = ''
password = ''
filename = 'getDatex2Data.xml'
chunk_size = 1024
namespace = "{http://datex2.eu/schema/2/2_0}"

host = 'localhost'
dbname = 'trafik'
dbuser = 'root'
dbpwd = 'trafik123'
logging.basicConfig(filename='clientpull.log', level=logging.DEBUG,format='%(asctime)s %(message)s')


def ct(dt):
	print dt.isoformat()
	return dt.isoformat()

def get_formatted_date(dat):
        strs = dat
	strs = strs[::-1].replace(':','',1)[::-1]
	print strs
	tz = strs[-5:]
	print tz
	dat1 = datetime.datetime.strptime(strs[:-5],"%Y-%m-%dT%H:%M:%S.%f")
	nowtuple = dat1.timetuple()
	nowtimestamp = time.mktime(nowtuple)
	str1 = email.utils.formatdate(nowtimestamp)
	print str1
	#str1 = str1[:-5] + tz
	#print str1
	date_tuple = email.utils.parsedate_tz(str1)
	print date_tuple
	if date_tuple:
		tmp_date = email.utils.mktime_tz(date_tuple)
		tmp_date = datetime.datetime.fromtimestamp(tmp_date)
		print tmp_date
	return ct(tmp_date)

def get_formatted_date_nomicro(dat):
        strs = dat
	strs = strs[::-1].replace(':','',1)[::-1]
	print strs
	tz = strs[-5:]
	print tz
	dat1 = datetime.datetime.strptime(strs[:-5],"%Y-%m-%dT%H:%M:%S")
	nowtuple = dat1.timetuple()
	nowtimestamp = time.mktime(nowtuple)
	str1 = email.utils.formatdate(nowtimestamp)
	print str1
	#str1 = str1[:-5] + tz
	#print str1
	date_tuple = email.utils.parsedate_tz(str1)
	print date_tuple
	if date_tuple:
		tmp_date = email.utils.mktime_tz(date_tuple)
		tmp_date = datetime.datetime.fromtimestamp(tmp_date)
		print tmp_date
	return ct(tmp_date)

def get_db():
    conn = DBA.connect(host=host, user=dbuser, passwd=dbpwd, db=dbname,charset="utf8", use_unicode=True)
    return conn

def gettagname(tag):
	return namespace + tag

def write_to_file(filename, data):
	with open(filename, 'wb') as fd:
		for chunk in data.iter_content(chunk_size):
			fd.write(chunk)
def getTextFromTag(elem):
	if elem is None:
		return ''
	else:
		return elem.text

def getGroupOfLocationsProp(groupOfLocations,prop):
	val = ''
	try:
		val = getTextFromTag(list(groupOfLocations.iter(gettagname(prop)))[0])
	except:
		val = ''
	return val

def insert_situation_text(conn,c,SituationId, lang,msg,commentType):
	try:
		qs = "INSERT INTO SituationRecordText(SituationId, Language, Text, Type) VALUES (%s,%s,%s,%s)"
		c.execute(qs, (SituationId, lang, msg, commentType))
	except Exception:
		error_stack = traceback.format_exc()
		print error_stack
		pass
	conn.commit()

def operation_mode_text(conn,c,SituationId,lang,msg,commentType):
	query = "SELECT COUNT(*) FROM SituationRecordText where SituationId=%s and Language=%s and Text=%s and Type=%s"
	c.execute(query,(SituationId, lang, msg, commentType))
	result = c.fetchall()
	ret = 0
	for row in result:
		if row[0] == 0:
			ret = 0
			print 'pp1'
		else:
			ret = 1
			print 'pp2'
	return ret


def insert_situation(conn,c,SituationId, SituationRecordId, Type, overallSeverity,informationStatus, confidentiality,situationRecordCreationTime, situationRecordVersionTime,situationRecordFirstSupplierVersionTime, probabilityOfOccurrence,severity, overallStartTime,overallEndTime, numberOfLanesRestricted,trafficConstrictionType, latitude,longitude, roadNumber,countyNumber, carriageway,lengthAffected, accidentType,County):
	try:
		qs = "INSERT INTO SituationRecord(SituationId, SituationRecordId, Type, overallSeverity,informationStatus, confidentiality,situationRecordCreationTime, situationRecordVersionTime,situationRecordFirstSupplierVersionTime, probabilityOfOccurrence,severity, overallStartTime,overallEndTime, numberOfLanesRestricted,trafficConstrictionType, latitude,longitude, roadNumber,countyNumber, carriageway,lengthAffected, accidentType,County) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		c.execute(qs, (SituationId, SituationRecordId, Type, overallSeverity,informationStatus, confidentiality,situationRecordCreationTime, situationRecordVersionTime,situationRecordFirstSupplierVersionTime, probabilityOfOccurrence,severity, overallStartTime,overallEndTime, numberOfLanesRestricted,trafficConstrictionType, latitude,longitude, roadNumber,countyNumber, carriageway,lengthAffected, accidentType,County))
	except Exception:
		error_stack = traceback.format_exc()
		print error_stack
		pass
	conn.commit()


def operation_mode(conn,c,SituationId, SituationRecordId, Type, overallSeverity,informationStatus, confidentiality,situationRecordCreationTime, situationRecordVersionTime,situationRecordFirstSupplierVersionTime, probabilityOfOccurrence,severity, overallStartTime,overallEndTime, numberOfLanesRestricted,trafficConstrictionType, latitude,longitude, roadNumber,countyNumber, carriageway,lengthAffected, accidentType,County):
        query1 = "SELECT COUNT(*) FROM SituationRecord where SituationId = %s"
        query = "SELECT SituationRecordId, Type, overallSeverity,informationStatus, confidentiality,situationRecordCreationTime, situationRecordVersionTime,situationRecordFirstSupplierVersionTime, probabilityOfOccurrence,severity, overallStartTime,overallEndTime, numberOfLanesRestricted,trafficConstrictionType, latitude,longitude, roadNumber,countyNumber, carriageway,lengthAffected, accidentType,County FROM SituationRecord where SituationId=%s and SituationRecordId=%s and  Type=%s and  overallSeverity=%s and informationStatus=%s and  confidentiality=%s and situationRecordCreationTime=%s and  situationRecordVersionTime=%s and situationRecordFirstSupplierVersionTime=%s and  probabilityOfOccurrence=%s and severity=%s and  overallStartTime=%s and overallEndTime=%s and  numberOfLanesRestricted=%s and trafficConstrictionType=%s and  latitude=%s and longitude=%s and  roadNumber=%s and countyNumber=%s and  carriageway=%s and lengthAffected=%s and  accidentType=%s and County = %s"
	c.execute(query,(SituationId, SituationRecordId, Type, overallSeverity,informationStatus, confidentiality,situationRecordCreationTime, situationRecordVersionTime,situationRecordFirstSupplierVersionTime, probabilityOfOccurrence,severity, overallStartTime,overallEndTime, numberOfLanesRestricted,trafficConstrictionType, latitude,longitude, roadNumber,countyNumber, carriageway,lengthAffected, accidentType,County))
	result = c.fetchall()
	ret = 0
	if result is None or len(result) == 0:
		ret = 1
                print SituationId
		c.execute(query1,[SituationId])
		result = c.fetchall()
		for row in result:
			if row[0] == 0:
				ret = 0
				print 'sp0'
		print 'sp1'
	else:
		for row in result:
			print 'sp2'
			ret = 2
	return ret


def update_situation(conn,c,SituationId, SituationRecordId, Type, overallSeverity,informationStatus, confidentiality,situationRecordCreationTime, situationRecordVersionTime,situationRecordFirstSupplierVersionTime, probabilityOfOccurrence,severity, overallStartTime,overallEndTime, numberOfLanesRestricted,trafficConstrictionType, latitude,longitude, roadNumber,countyNumber, carriageway,lengthAffected, accidentType,County):
	try:
		qs = "UPDATE SituationRecord SET SituationRecordId=%s,  Type=%s,  overallSeverity=%s, informationStatus=%s,  confidentiality=%s, situationRecordCreationTime=%s,  situationRecordVersionTime=%s, situationRecordFirstSupplierVersionTime=%s,  probabilityOfOccurrence=%s, severity=%s,  overallStartTime=%s, overallEndTime=%s,  numberOfLanesRestricted=%s, trafficConstrictionType=%s,  latitude=%s, longitude=%s,  roadNumber=%s, countyNumber=%s,  carriageway=%s, lengthAffected=%s,  accidentType=%s, County = %s WHERE SituationId = %s"
		c.execute(qs, (SituationRecordId, Type, overallSeverity,informationStatus, confidentiality,situationRecordCreationTime, situationRecordVersionTime,situationRecordFirstSupplierVersionTime, probabilityOfOccurrence,severity, overallStartTime,overallEndTime, numberOfLanesRestricted,trafficConstrictionType, latitude,longitude, roadNumber,countyNumber, carriageway,lengthAffected, accidentType,County,SituationId))
	except Exception:
		error_stack = traceback.format_exc()
		print error_stack
		pass
	conn.commit()

def swedish(english):
	tree2 = ET.parse('translate.txt')
	root2 = tree2.getroot()
        sweden = english 
        for elem in root2.iter('data'):
            eng = elem.find('eng').text 
            if eng.lower() == english.lower():
                sweden = elem.find('swed').text 
        return sweden


resp = requests.get(accident_url, auth=HTTPBasicAuth(user_name, password))
write_to_file(filename, resp)
logging.info('New Cycle starting')
logging.info('Response from getDatex2Data')
logging.info(resp.text)
filename = 'getDatex2Data.xml'
tree = ET.parse(filename)
root = tree.getroot()
#logging.info("Root text" + root.text)
situations = root.findall("./{http://datex2.eu/schema/2/2_0}payloadPublication/{http://datex2.eu/schema/2/2_0}situation")
logging.info("Situations are")
logging.info(situations)
conn = get_db()
c = conn.cursor()
for situation in situations:
	logging.info('Situation Starts')
	situation_id = situation.attrib['id']
	logging.info("situation_id: " + situation_id)
	overallSeverity = getTextFromTag(situation.find(gettagname('overallSeverity')))
	situationVersionTime = getTextFromTag(situation.find(gettagname('situationVersionTime')))
	logging.info("overallSeverity: " + overallSeverity)
	logging.info("situationVersionTime: " + situationVersionTime)
	informationStatus = getTextFromTag(situation.find('./'+ gettagname('headerInformation')+'/' + gettagname('informationStatus')))
	confidentiality = getTextFromTag(situation.find('./'+ gettagname('headerInformation')+'/' + gettagname('confidentiality')))
	situationRecord = situation.find('./'+ gettagname('situationRecord'))
	Type = situationRecord.attrib['{http://www.w3.org/2001/XMLSchema-instance}type']
	SituationRecordId = situationRecord.attrib['id']
	situationRecordCreationTime = get_formatted_date(getTextFromTag(situationRecord.find('./'+ gettagname('situationRecordCreationTime'))))
	logging.info("Type: " + Type)
	logging.info("SituationRecordId: " + SituationRecordId)
	logging.info("situationRecordCreationTime: " + situationRecordCreationTime)
	print situationRecordCreationTime
	situationRecordVersionTime = get_formatted_date(getTextFromTag(situationRecord.find('./'+ gettagname('situationRecordVersionTime'))))
	logging.info("situationRecordVersionTime: " + situationRecordVersionTime)
	print situationRecordVersionTime
	situationRecordFirstSupplierVersionTime = get_formatted_date(getTextFromTag(situationRecord.find('./'+ gettagname('situationRecordFirstSupplierVersionTime'))))
	logging.info("situationRecordFirstSupplierVersionTime: " + situationRecordFirstSupplierVersionTime)
	print situationRecordFirstSupplierVersionTime
	probabilityOfOccurrence = getTextFromTag(situationRecord.find('./'+ gettagname('probabilityOfOccurrence')))
	logging.info("probabilityOfOccurrence: " + probabilityOfOccurrence)
	print probabilityOfOccurrence
	severity = getTextFromTag(situationRecord.find('./'+ gettagname('severity')))
	logging.info("severity: " + severity)
	print severity
	overallStartTime = get_formatted_date_nomicro(getTextFromTag(situationRecord.find('./'+ gettagname('validity') + '/'+ gettagname('validityTimeSpecification') +'/'+ gettagname('overallStartTime'))))
	logging.info("overallStartTime: " + overallStartTime)
	print overallStartTime
	overallEndTime = get_formatted_date_nomicro(getTextFromTag(situationRecord.find('./'+ gettagname('validity') + '/'+ gettagname('validityTimeSpecification') +'/'+ gettagname('overallEndTime'))))
	logging.info("overallEndTime: " + overallEndTime)
	print overallEndTime
	numberOfLanesRestricted = getTextFromTag(situationRecord.find('./'+ gettagname('impact') + '/'+ gettagname('numberOfLanesRestricted')))
	if numberOfLanesRestricted is None or numberOfLanesRestricted  == '':
		numberOfLanesRestricted = -1
	logging.info("numberOfLanesRestricted: " + str(numberOfLanesRestricted))
	print numberOfLanesRestricted
	trafficConstrictionType = getTextFromTag(situationRecord.find('./'+ gettagname('impact') + '/'+ gettagname('trafficConstrictionType')))
	logging.info("trafficConstrictionType: " + trafficConstrictionType)
	print trafficConstrictionType
	groupOfLocations = situationRecord.find('./'+ gettagname('groupOfLocations'))

	latitude = getGroupOfLocationsProp(groupOfLocations,'latitude')
	logging.info("latitude: " + latitude)
	print latitude
	longitude = getGroupOfLocationsProp(groupOfLocations,'longitude')
	logging.info("longitude: " + longitude)
	print longitude
	roadNumber = getGroupOfLocationsProp(groupOfLocations,'roadNumber')
	logging.info("roadNumber: " + roadNumber)
	print roadNumber
	countyNumber = getGroupOfLocationsProp(groupOfLocations,'countyNumber')
	logging.info("countyNumber: " + countyNumber)
	print countyNumber
	carriageway = getGroupOfLocationsProp(groupOfLocations,'carriageway')
	logging.info("carriageway: " + carriageway)
	print carriageway
	lengthAffected = getGroupOfLocationsProp(groupOfLocations,'lengthAffected')
	logging.info("lengthAffected: " + lengthAffected)
	print lengthAffected

	accidentType = getTextFromTag(situationRecord.find('./'+ gettagname('accidentType')))
	logging.info("accidentType: " + accidentType)
	print accidentType
        County = ''
	country_full = ''
	try:
	    country = 'http://nominatim.openstreetmap.org/search.php?q=%s,%s&format=xml' %(latitude,longitude)
    	    print country
	    resp = requests.get(country)
	    filename = 'country.xml'
	    write_to_file(filename, resp)
	    #logging.info("Response from openstreetmap")
	    #logging.info(resp.text.encode('utf-8'))
	    tree = ET.parse(filename)
	    root = tree.getroot()
	    country_full = root.find('./place').attrib['display_name']
	    logging.info("country_full: " + country_full)
	    tokens = country_full.split(',')
	    tree1 = ET.parse('co.txt')
	    root1 = tree1.getroot()
	    comp = root1.text
	    print comp
	    for item in tokens:
		item = ud.normalize('NFC', unicode(item))
		comp = ud.normalize('NFC', comp) 
		if comp in item:
			County = item
	    print country_full
	    print situation_id
        except:
	    logging.info("Exception in getting county information")
	mail_needed = 0
	opmode = operation_mode(conn,c,situation_id, SituationRecordId, Type, overallSeverity,informationStatus, confidentiality,situationRecordCreationTime, situationRecordVersionTime,situationRecordFirstSupplierVersionTime, probabilityOfOccurrence,severity, overallStartTime,overallEndTime, numberOfLanesRestricted,trafficConstrictionType, latitude,longitude, roadNumber,countyNumber, carriageway,lengthAffected, accidentType,country_full)
	if opmode == 0:
		insert_situation(conn,c,situation_id, SituationRecordId, Type, overallSeverity,informationStatus, confidentiality,situationRecordCreationTime, situationRecordVersionTime,situationRecordFirstSupplierVersionTime, probabilityOfOccurrence,severity, overallStartTime,overallEndTime, numberOfLanesRestricted,trafficConstrictionType, latitude,longitude, roadNumber,countyNumber, carriageway,lengthAffected, accidentType,country_full)
		mail_needed = 1
	elif opmode == 1:
		update_situation(conn,c,situation_id, SituationRecordId, Type, overallSeverity,informationStatus, confidentiality,situationRecordCreationTime, situationRecordVersionTime,situationRecordFirstSupplierVersionTime, probabilityOfOccurrence,severity, overallStartTime,overallEndTime, numberOfLanesRestricted,trafficConstrictionType, latitude,longitude, roadNumber,countyNumber, carriageway,lengthAffected, accidentType,country_full)
		mail_needed = 1
	else:
		print 'SituationRecord already exist'
	generalPublicComments = situationRecord.findall('./'+ gettagname('generalPublicComment'))
	where = ''
	message = ''
	for generalPublicComment in  generalPublicComments:
		commentType = getTextFromTag(generalPublicComment.find('./'+ gettagname('commentType') )) 
		logging.info("commentType: " + commentType)
		print commentType
		values = generalPublicComment.findall('./'+ gettagname('comment') + '/'+ gettagname('values'))
		for elem in values:
			for val in elem.iter(gettagname('value')):
				lang = val.attrib['lang']
				msg = val.text
				logging.info("lang: " + lang)
				logging.info("msg: " + msg)
				omt = operation_mode_text(conn,c,situation_id,lang,msg,commentType)
				if commentType == 'locationDescriptor':
					where = msg
				elif commentType == 'description':
					message = msg

				if omt == 0:
					insert_situation_text(conn,c,situation_id,lang,msg,commentType)
					mail_needed = 1
				else:
					print 'SituationRecordText already exist'

	source = situationRecord.findall('./'+ gettagname('source')+'/'+gettagname('sourceName')+'/'+gettagname('values'+'/'+gettagname('value')))
	for elem in source:
		lang = elem.attrib['lang']
		msg = elem.text
		typ = 'source'
		logging.info("typ: " + typ)
		logging.info("lang: " + lang)
		logging.info("msg: " + msg)
		omt = operation_mode_text(conn,c,situation_id,lang,msg,typ)
		if omt == 0:
			insert_situation_text(conn,c,situation_id,lang,msg,typ)
		else:
			print 'SituationRecordText already exist'
	toaddrs  = ['handelseinformation@nyhetsfotograf.se','trafikverket@dagsmedia.se']
        if Type.lower() == 'accident':
            Type = 'Olycka'
        trafficConstrictionType = swedish(trafficConstrictionType)
	if mail_needed == 1:
		datext_mailer.send_mail(toaddrs,situationRecordCreationTime,overallEndTime,Type,roadNumber,County,where,message,trafficConstrictionType,latitude,longitude,country_full)
	logging.info('Situation End')
conn.close()
logging.info('Cycle completed')




