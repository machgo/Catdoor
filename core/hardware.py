from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
from configparser import SafeConfigParser
import threading
import time
import RPi.GPIO as GPIO
import logging

class WatchdogThread(threading.Thread):
    def __init__(self, hardware):
        self.exitFlag = False
        self.hardware = hardware
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if GPIO.input(self.hardware.pin_irsensor_in):
                self.hardware.motionDetectedBool = True

            if GPIO.input(self.hardware.pin_irsensor2_in):
                self.hardware.motionDetectedBool = True

            if self.exitFlag:
                break

            time.sleep(1)

    def exit(self):
        self.exitFlag = True


class Hardware:
    motionDetectedBool = False

    def __init__(self):
        logging.debug('Loading Config....')
        self.loadConfig()
        logging.debug('Hardware init...')
        self.initializeHardware()
        logging.debug('Hardware ready.')

    def loadConfig(self):
        parser = SafeConfigParser()
        parser.read('/opt/Catdoor/core/config.ini')

        self.pin_irsensor_in = parser.getint('pin_settings', 'irsensor_in')
        self.pin_irsensor2_in = parser.getint('pin_settings', 'irsensor2_in')
        self.pin_buzzer_out = parser.getint('pin_settings', 'buzzer_out')

        self.motor_delay = parser.getfloat('motor_settings', 'delay')
        self.motor_distance = parser.getint('motor_settings', 'distance')

    def initializeHardware(self):
        self.mh = Adafruit_MotorHAT()
        self.myStepper = self.mh.getStepper(200,1)
        self.myStepper.setSpeed(255)

        GPIO.setwarnings(False)
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.pin_irsensor_in, GPIO.IN)
        GPIO.setup(self.pin_irsensor2_in, GPIO.IN)
        GPIO.setup(self.pin_buzzer_out, GPIO.OUT)

        GPIO.output(self.pin_buzzer_out, GPIO.LOW)
        GPIO.setwarnings(True)

    def openDoor(self):
        steps = self.motor_distance
        self.myStepper.step(steps, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.INTERLEAVE)

    def closeDoor(self):
        self.doShortBeeps(5)
        steps = self.motor_distance
        self.myStepper.step(steps, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.INTERLEAVE)

    def doShortBeeps(self, num):
        for i in range(0, num):
            self.beep()

    def beep(self):
        GPIO.output(self.pin_buzzer_out, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(self.pin_buzzer_out, GPIO.LOW)
        time.sleep(0.05)

    def isMotionDetected(self):
        if self.motionDetectedBool:
            self.motionDetectedBool = False
            return True
        else:
            return False

    def resetMotionDetected(self):
        self.motionDetectedBool = False

    def activateWatchdog(self):
        self.workerThread = WatchdogThread(self)
        self.workerThread.start()

    def deactivateWatchdog(self):
        self.mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
        self.workerThread.exit()
