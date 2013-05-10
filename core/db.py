from pymongo import MongoClient
import datetime

class catdoorDB:
	def openConnection(self):
		connection = MongoClient('catdoor', 27017)
		db = connection.catdoor
		return db

	def getDoorLockState(self):
		db = self.openConnection()
		runtime = db.runtime
		doc = runtime.find_one({"name": "schedule"})

		opentime = doc['opentime']
		closetime = doc['closetime']
		nowtime = datetime.datetime.utcnow()

		if opentime.time() < nowtime.time() and closetime.time() > nowtime.time():
			return True
		else:
			return False

	def writeLog(self, action, details='no details'):
		db = self.openConnection()
		logs = db.logs

		logentry = {"action": action,
		"details": details,
		"timestamp": datetime.datetime.utcnow()	
		}
		logentry_id = logs.insert(logentry)

		print "Logentry, action: {}, details: {}, entry_id: {}".format(action, details, logentry_id)