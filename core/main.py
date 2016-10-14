#!/usr/bin/env python
import os
import hardware
import datetime
import time
import db
import sys
import atexit
import logging
import traceback
from daemon import Daemon

class MyDaemon(Daemon):
    def run(self):

        hardw.activateWatchdog()
        database.writeLog("Watchdog started", 1001)

        while True:
            time.sleep(0.5)
            now = datetime.datetime.now()
            
            if len(os.listdir("/var/lib/motion/")):
                if database.getDoorLockState():
                    database.writeLog("Camera-Pic found", 1011)
                    hardw.openDoor()
                    
                    database.writeLog("Door opened", 1021)
                    time.sleep(5)
                    os.system('rm /var/lib/motion/*')

                    while len(os.listdir("/var/lib/motion/")):
                        time.sleep(5)
                        os.system('rm /var/lib/motion/*')

                    hardw.closeDoor()
                    hardw.resetMotionDetected()
                    database.writeLog("Door closed", 1022)


                else:
                    database.writeLog("Camera-Pic found", 1012)
                    os.system('rm /var/lib/motion/*')


            if hardw.isMotionDetected():
                if database.getDoorLockState():
                    database.writeLog("Motion detected", 1031)
                    hardw.openDoor()
                    database.writeLog("Door opened", 1021)
                    time.sleep(10)
                    while hardw.isMotionDetected():
                        time.sleep(5)

                    hardw.closeDoor()
                    database.writeLog("Door closed", 1022)
                    time.sleep(3)
                    hardw.resetMotionDetected()



                else:
                    database.writeLog("Motion detected", 1032)

            time.sleep(0.5)


def log_uncaught_exceptions(ex_cls, ex, tb):

    logging.critical(''.join(traceback.format_tb(tb)))
    logging.critical('{0}: {1}'.format(ex_cls, ex))


if __name__ == "__main__":

    logging.basicConfig(
            level=logging.DEBUG,
            filename='/tmp/catdoorcore.log',
            filemode='w')

    sys.excepthook = log_uncaught_exceptions

    daemon = MyDaemon('/opt/Catdoor/core/daemon-catdoor.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            logging.debug('Starting Database...')
            database = db.catdoorDB()
            logging.debug('Starting Hardware...')
            hardw = hardware.Hardware()
            logging.debug('Starting Daemon...')
            daemon.start()
            logging.debug('All started.')
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
