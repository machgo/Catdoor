import hardware
import datetime
import time
import db 



database = db.catdoorDB()

if database.getDoorLockState():
	print "Door is unlocked"
else:
	print "Door is locked"

hardw = hardware.Hardware()
hardw.activateWatchdog()
database.writeLog("Watchdog started")



while True:
	try:
		now = datetime.datetime.now()

		if hardw.isSerialPending():
			detectedSerial = hardw.getPendingSerial()
			database.writeLog("Tag detected", "Serial: {}".format(detectedSerial))

			#if detectedSerial == '756_098100641037': #for exact check of the chip-sn
			hardw.openDoor()
			database.writeLog("Door opened")
			time.sleep(10)
			while hardw.isMotionDetected():
				time.sleep(5)

			hardw.closeDoor()
			database.writeLog("Door closed")

		if hardw.isMotionDetected(): 
			if database.getDoorLockState():
				database.writeLog("Motion detected", "Door is unlocked")
				hardw.openDoor()
				database.writeLog("Door opened")
				time.sleep(10)
				while hardw.isMotionDetected():
					time.sleep(5)

				hardw.closeDoor()
				database.writeLog("Door closed")

			else:
				database.writeLog("Motion detected", "Door is locked")

		time.sleep(0.5)
	except (KeyboardInterrupt, SystemExit):
		hardw.deactivateWatchdog()
		database.writeLog("Watchdog stopped")
		break

# blubb.deactivateWatchdog()