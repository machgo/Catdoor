from ConfigParser import SafeConfigParser
import threading
import time
import RPi.GPIO as GPIO

class WatchdogThread(threading.Thread):
    def __init__(self, hardware):
        self.exitFlag = False
        self.hardware = hardware
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if GPIO.input(self.hardware.pin_irsensor_in):
                self.hardware.motionDetectedBool = True

            if self.exitFlag:
                break

            time.sleep(1)

    def exit(self):
        self.exitFlag = True


class Hardware:
    motionDetectedBool = False

    def __init__(self):

        self.loadConfig()
        self.initializeHardware()

    def loadConfig(self):
        parser = SafeConfigParser()
        parser.read('config.ini')

        self.pin_irsensor_in = parser.getint('pin_settings', 'irsensor_in')
        self.pin_buzzer_out = parser.getint('pin_settings', 'buzzer_out')
        self.pin_direction_out = parser.getint('pin_settings', 'direction_out')
        self.pin_step_out = parser.getint('pin_settings', 'step_out')
        self.pin_sleep_out = parser.getint('pin_settings', 'sleep_out')

        self.motor_delay = parser.getfloat('motor_settings', 'delay')

    def initializeHardware(self):
        GPIO.setwarnings(False)
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.pin_irsensor_in, GPIO.IN)

        GPIO.setup(self.pin_sleep_out, GPIO.OUT)
        GPIO.setup(self.pin_direction_out, GPIO.OUT)
        GPIO.setup(self.pin_step_out, GPIO.OUT)
        GPIO.setup(self.pin_buzzer_out, GPIO.OUT)

        self.sleepStepper()
        GPIO.output(self.pin_direction_out, GPIO.LOW)
        GPIO.output(self.pin_step_out, GPIO.LOW)
        GPIO.output(self.pin_buzzer_out, GPIO.LOW)
        GPIO.setwarnings(True)



    def sleepStepper(self):
        GPIO.output(self.pin_sleep_out, GPIO.LOW)

    def awakeStepper(self):
        GPIO.output(self.pin_sleep_out, GPIO.HIGH)

    def doStep(self,delay):
        GPIO.output(self.pin_step_out, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(self.pin_step_out, GPIO.LOW)
        time.sleep(delay)

    def openDoor(self):
        self.awakeStepper()
        steps = 5950
        GPIO.output(self.pin_direction_out, GPIO.HIGH)
        for i in range(0, steps):
            self.doStep(self.motor_delay)
        self.sleepStepper()

    def closeDoor(self):
        self.doShortBeeps(5)
        self.awakeStepper()
        steps = 5950
        GPIO.output(self.pin_direction_out, GPIO.LOW)

        for i in range(0, steps):
            self.doStep(self.motor_delay)

        self.sleepStepper();

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
        self.workerThread.exit()
