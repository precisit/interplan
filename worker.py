#This script will do the heavy lifting
#General
import json

#Boto
import boto
from boto.sqs.connection import SQSConnection
from boto.sqs.message import Message

#MongdoDB
import pymongo
from pymongo import MongoClient
from bson import json_util
from bson.objectid import ObjectId

mongoClient = MongoClient('mongodb://localhost:27017/')
db = mongoClient['interplan']
objects = db.objects

#DynamoDBConn = boto.dynamodb.connect_to_region('eu-west-1')
conn = boto.sqs.connect_to_region('eu-west-1')
jobQueue = conn.create_queue('interplanJobQueue')

while True:
	print 'Will long-poll for message'
	m = jobQueue.read(wait_time_seconds=20)

	if m is not None:
		data = json.loads(m.get_body())
		print 'Got new Job Request: ', data
		departure = db.objects.find_one({'_id': ObjectId(data['departure']['_id'])})
		destination = db.objects.find_one({'_id': ObjectId(data['destination']['_id'])})
		jobQueue.delete_message(m)
		print '---'
