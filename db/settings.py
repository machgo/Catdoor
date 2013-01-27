from pymongo import MongoClient
import datetime

connection = MongoClient('localhost', 27017)

db = connection.catdoor

settings = db.settings
settings.remove()


post = {"balou_id": "123456789123456",
		"door_state": "unlocked",
		"balou_state": "indoor",
		"sunrise": datetime.datetime.utcnow(),
		"sundawn": datetime.datetime.utcnow(),
		"last_update": datetime.datetime.utcnow()			
		}

post_id = settings.insert(post)
print post_id

latest_settings = settings.find_one()

print latest_settings