#!/usr/bin/env python

import hardware
import datetime
import time
import db
import sys
import atexit
from daemon import Daemon

class MyDaemon(Daemon):
    def run(self):

        hardw.activateWatchdog()
        database.writeLog("Watchdog started")

        while True:
            time.sleep(0.5)
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



if __name__ == "__main__":
    daemon = MyDaemon('/home/pi/catdoor/core/daemon-catdoor.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            database = db.catdoorDB()
            hardw = hardware.Hardware()
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            database = db.catdoorDB()
            hardw = hardware.Hardware()

            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)