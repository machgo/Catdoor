from bottle import Bottle, run, static_file, request
from pymongo import MongoClient
import json
import datetime

connection = MongoClient('localhost', 27017)
db = connection.catdoor

app = Bottle()

@app.get('/')
def hello():
	return static_file('index.html','static')

@app.get('/schedule')
def GetSchedule():
	schedule = db.runtime.find_one({"name": "schedule"})
	ret = {"opentime": unix_time_millis(schedule['opentime']),
			"closetime": unix_time_millis(schedule['closetime'])}
	return ret

@app.get('/balou')
def GetBalou():
	balou = db.runtime.find_one({"name": "balou"})
	ret = {"balou_state": balou['balou_state'],
			"last_update": unix_time_millis(balou['last_update'])}
	return ret

@app.get('/door')
def GetDoor():
	door = db.runtime.find_one({"name": "door"})
	ret = {"door_state": door['door_state'],
			"last_update": unix_time_millis(door['last_update'])}
	return ret

@app.put('/door')
def PutDoor():
	door = db.runtime.find_one({"name": "door"})
	door['door_state'] = request.forms.door_state
	door['last_update'] = datetime.datetime.utcnow()

	db.runtime.save(door)
	return 0

def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()

def unix_time_millis(dt):
    return unix_time(dt) * 1000.0

run(app, host='0.0.0.0', port=8080, debug=True)
