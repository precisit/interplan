#DB Importer for CSV data from: http://ssd.jpl.nasa.gov/sbdb_query.cgi

import sys
import re

#MongdoDB
import pymongo
from pymongo import MongoClient
from bson import json_util
from bson.objectid import ObjectId

mongoClient = MongoClient('mongodb://localhost:27017/')
db = mongoClient['interplan']
objects = db.objects

if len(sys.argv) < 2:
	print 'Usage: parsedatabase.py FILENAME'
	raise SystemExit
 
prog = re.compile(r"^(\d*)\s*(\w*)\s*(.*)")

with open(str(sys.argv[1])) as f:
	next(f)
	for line in f:
		data = line.split(',')
		name = data[0]
		res = prog.match(name.replace('"','').strip())
		#print res.group(0), '-', res.group(1), '-', res.group(2), '-', res.group(3)
		dbdata = dict()
		dbdata['full_name'] = res.group(0)
		dbdata['number'] = res.group(1)
		dbdata['name'] = res.group(2).lower()
		dbdata['discover'] = res.group(3)
		dbdata['a'] = data[1]
		dbdata['e'] = data[2]
		dbdata['i'] = data[3]
		dbdata['om'] = data[4]
		dbdata['w'] = data[5]
		dbdata['q'] = data[6]
		dbdata['ad'] = data[7]
		dbdata['per_y'] = data[8]
		dbdata['data_arc'] = data[9]
		dbdata['condition_code'] = data[10]
		dbdata['n_obs_used'] = data[11]
		dbdata['n_del_obs_used'] = data[12]
		dbdata['n_dop_obs_used'] = data[13]
		dbdata['H'] = data[14]
		dbdata['diameter'] = data[15]
		dbdata['extent'] = data[16]
		dbdata['albedo'] = data[17]
		dbdata['rot_per'] = data[18]
		dbdata['GM'] = data[19]
		dbdata['BV'] = data[20]
		dbdata['UB'] = data[21]
		dbdata['IR'] = data[22]
		dbdata['pec_B'] = data[23]
		dbdata['spec_T'] = data[24]
		dbdata['epoch_mjd'] = data[25]
		dbdata['ma'] = data[31].strip()
		objects.insert(dbdata)

