import hardware
import datetime
import time

blubb = hardware.Hardware()
blubb.activateWatchdog()
print datetime.datetime.now()
print "stated watchdog"


while True:
	try:
		if blubb.isSerialPending():
			print datetime.datetime.now()
			print "tag detected"
			detectedSerial = blubb.getPendingSerial()
			print detectedSerial

			if detectedSerial == '756_098100641037':
				blubb.openDoor()
				time.sleep(10)
				blubb.closeDoor()

		if blubb.isMotionDetected():
			print datetime.datetime.now()
			print "motion detected"
			blubb.openDoor()
			time.sleep(10)
			while blubb.isMotionDetected():
				time.sleep(5)

			blubb.closeDoor()

		time.sleep(0.5)
	except (KeyboardInterrupt, SystemExit):
		blubb.deactivateWatchdog()
		break

# blubb.deactivateWatchdog()