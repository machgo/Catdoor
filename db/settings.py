from pymongo import MongoClient
import datetime

connection = MongoClient('localhost', 27017)

db = connection.catdoor

runtime = db.runtime
runtime.remove()

post = {"name": "settings",
		"balou_id": "123456789123456",
		"last_update": datetime.datetime.utcnow()			
		}
post_id = runtime.insert(post)
print 'Settings-ID: {}'.format(post_id)

post = {"name": "schedule",
		"sunrise": datetime.datetime.utcnow(),
		"sundawn": datetime.datetime.utcnow(),
		"opentime": datetime.datetime.utcnow(),
		"closetime": datetime.datetime.utcnow(),
		"last_update": datetime.datetime.utcnow()	
		}
post_id = runtime.insert(post)
print 'Schedule-ID: {}'.format(post_id)

post = {"name": "balou",
		"balou_state": "indoor",
		"last_update": datetime.datetime.utcnow()			
		}
post_id = runtime.insert(post)
print 'Balou-ID: {}'.format(post_id)

post = {"name": "door",
		"door_state": "unlocked",
		"last_update": datetime.datetime.utcnow()			
		}
post_id = runtime.insert(post)
print 'Door-ID: {}'.format(post_id)

