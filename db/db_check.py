from pymongo import MongoClient
import datetime

connection = MongoClient('localhost', 27017)
db = connection.catdoor

print 'Checking settings in database...'

runtime = db.runtime
doc = runtime.find_one({"name": "schedule"})

opentime = doc['opentime']
closetime = doc['closetime']
nowtime = datetime.datetime.now()

if opentime.time() < nowtime.time() and closetime.time() > nowtime.time():
	print "door is open..."
else:
	print "door is closed..."


print opentime