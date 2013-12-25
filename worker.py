#This script will do the heavy lifting
#Keplerian solver
import math
import operator
import datetime
from datetime import datetime
from datetime import timedelta
from PyKEP import *

#General
import json

#Boto
import boto
from boto.sqs.connection import SQSConnection
from boto.sqs.message import Message

#Tornado (initially blocking HTTP requests, later vision is to have calculations nonblocking in ioloop)
import tornado.httpclient as httpclient

#MongdoDB
import pymongo
from pymongo import MongoClient
from bson import json_util
from bson.objectid import ObjectId

mongoClient = MongoClient('mongodb://localhost:27017/')
db = mongoClient['interplan']
objects = db.objects

#TODO: Write lightweight library for storing auth info + sending/recieving info using REST 
#Question: Possible to make functions become non-blocking (long polling), calling a function when resuts are ready?? 
# 1) Get planet / asteroid objects from the information
# 2) Set up the calculations (dates, etc)
# 3) Perform calculations and every 1% report status + latest pixels to QUEUE
# 4) Future: Cache orbital results. 
# 5) Replace SQS Longpolling and REST Post through my server to a WEBSOCKET interface in Python OR a REST CALLBACK solution in Python (better??) - REST call to tell server I'm ready to recieve.

# MAJOR BUG NOW: Too much data - server side binning of data or other smart way of compressing data flow ?? 

#Set up nonblocking HTTP client
http_client = httpclient.HTTPClient()

#Set up AWS SQS
conn = boto.sqs.connect_to_region('eu-west-1')
jobQueue = conn.create_queue('interplanJobQueue')

#Function to validate incoming data and add zeroes where needed
required = ['epoch_mjd', 'a', 'e', 'i', 'om', 'w', 'ma', 'GM']
def checkData(data):
	for item in required:
		if data[item] == '':
			data[item] = '0'

resFactor = 5;

#TODO: Remake into nonblocking ioloop
while True:
	print 'Will long-poll for message'
	m = jobQueue.read(wait_time_seconds=20)

	if m is not None:
		data = json.loads(m.get_body())
		jobQueue.delete_message(m)
		print 'Got new Job Request: ', data
		dep = db.objects.find_one({'_id': ObjectId(data['departure']['_id'])})
		des = db.objects.find_one({'_id': ObjectId(data['destination']['_id'])})

		depDia = 10.0;
		if dep['diameter']:
			depDia = float(dep['diameter']) / 2.0
		checkData(dep)
		depObject = planet(epoch(float(dep['epoch_mjd']),epoch.epoch_type.MJD), (float(dep['a']) * AU, float(dep['e']), float(dep['i'])*DEG2RAD, float(dep['om'])*DEG2RAD, float(dep['w'])*DEG2RAD, float(dep['ma'])*DEG2RAD), MU_SUN, 0.001 + float(dep['GM']), depDia, depDia*1.1)

		desDia = 100;
		if des['diameter']:
			desDia = float(des['diameter']) / 2.0
		checkData(des)
		desObject = planet(epoch(float(des['epoch_mjd']),epoch.epoch_type.MJD), (float(des['a']) * AU, float(des['e']), float(des['i'])*DEG2RAD, float(des['om'])*DEG2RAD, float(des['w'])*DEG2RAD, float(des['ma'])*DEG2RAD), MU_SUN, 0.001 + float(des['GM']), desDia, desDia*1.1)

		#TODO: Remove verification ??? OR KEEP IT LOGS - KEWLT 
		print depObject, desObject

		start = datetime.strptime(data['windowStart'], '%Y-%m-%d')
		start -= timedelta(days=1)
		stop = datetime.strptime(data['windowStop'], '%Y-%m-%d')
		stop += timedelta(days=1)
		windowDuration = (stop-start).days
		travelMin = data['minTT']
		travelMax = data['maxTT']

		print 'start time: ',start
		print 'end time',stop
		print 'duration: ', windowDuration

		dataBuf = []
		calcCounter = 0;

		for windowDay in range(0,windowDuration/resFactor):
			t0 = start + timedelta(days=resFactor*windowDay)
			epoch0 = epoch_from_string(t0.isoformat(' '))

			for missionDay in range(travelMin/resFactor, travelMax/resFactor):
				t1 = t0 + timedelta(days=resFactor*missionDay)
				epoch1 = epoch_from_string(t1.isoformat(' '))
				transitTime = epoch1.mjd2000 - epoch0.mjd2000

				r0, v0 = depObject.eph(epoch0)
				r1, v1 = desObject.eph(epoch1)

				l = lambert_problem(r0, r1, transitTime*DAY2SEC, MU_SUN)
				depV = l.get_v1()

				dv = tuple(map(operator.sub, depV[0], v0))
				depRelV = 0
				for x in dv:
					depRelV += x*x
				depRelV = math.sqrt(depRelV)
				depC3 = depRelV**2/1000.0**2

				outData = [ [ windowDay*resFactor, missionDay*resFactor ], round(depC3,1) ]
				dataBuf.append(outData)

				calcCounter += 1

				#TODO: PERCENTAGE COUNTER MESSAGES 
				if calcCounter%100 == 0:
					print 100.0*windowDay*resFactor/windowDuration
					try:
						print 'WILL SEND A'
						response = http_client.fetch(httpclient.HTTPRequest(url="https://api.jsflow.com/v1/user/%s/%s" % (data['fromId'], 'dataPoint'), method='POST', body=json.dumps(dataBuf), validate_cert=False, auth_username='0d0bc8630706bf0fc8c1e9a2', auth_password='4qKcmmFCOjliJ7I1S6CkbsGnR8Q='))
						print response.body
					except httpclient.HTTPError, e:
					    print "Error:", e
					dataBuf = []
			
		print 'done!'

		try:
			print 'WILL SEND B'
			response = http_client.fetch(httpclient.HTTPRequest(url="https://api.jsflow.com/v1/user/%s/%s" % (data['fromId'], 'dataPoint'), method='POST', body=json.dumps(dataBuf), validate_cert=False, auth_username='0d0bc8630706bf0fc8c1e9a2', auth_password='4qKcmmFCOjliJ7I1S6CkbsGnR8Q='))
			print response.body
		except httpclient.HTTPError, e:
		    print "Error:", e





















