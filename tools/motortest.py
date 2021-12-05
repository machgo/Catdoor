import RPi.GPIO as GPIO
import time


class Motor:
    def initializeHardware(self):
        self.pin_sleep_out = 23
        self.pin_step_out = 22
        self.pin_direction_out = 17
        self.pin_ms1_out = 4
        self.pin_ms2_out = 25

        self.pin_buzzer_out = 24

        GPIO.setwarnings(False)
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.pin_sleep_out, GPIO.OUT)
        GPIO.setup(self.pin_direction_out, GPIO.OUT)
        GPIO.setup(self.pin_step_out, GPIO.OUT)
        GPIO.setup(self.pin_ms1_out, GPIO.OUT)
        GPIO.setup(self.pin_ms2_out, GPIO.OUT)
        GPIO.setup(self.pin_buzzer_out, GPIO.OUT)

        self.sleepStepper()
        GPIO.output(self.pin_direction_out, GPIO.LOW)
        GPIO.output(self.pin_step_out, GPIO.LOW)
        GPIO.output(self.pin_buzzer_out, GPIO.LOW)
        self.setEighthStepMode()
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

    def openAndCloseDoor(self, numSteps, delay):
        self.awakeStepper()
        GPIO.output(self.pin_direction_out, GPIO.HIGH)
        for i in range(0, numSteps):
            self.doStep(delay)

        time.sleep(1)

        GPIO.output(self.pin_direction_out, GPIO.LOW)
        for i in range(0, numSteps):
            self.doStep(delay)
        self.sleepStepper()

    def setFullStepMode(self):
        GPIO.output(self.pin_ms1_out, GPIO.LOW)
        GPIO.output(self.pin_ms2_out, GPIO.LOW)

    def setHalfStepMode(self):
        GPIO.output(self.pin_ms1_out, GPIO.HIGH)
        GPIO.output(self.pin_ms2_out, GPIO.LOW)

    def setQuarterStepMode(self):
        GPIO.output(self.pin_ms1_out, GPIO.LOW)
        GPIO.output(self.pin_ms2_out, GPIO.HIGH)

    def setEighthStepMode(self):
        GPIO.output(self.pin_ms1_out, GPIO.HIGH)
        GPIO.output(self.pin_ms2_out, GPIO.HIGH)


delay = 0.0016
distance = 725

mot = Motor()
mot.initializeHardware()

# print ("doing 1/1 steps")
# mot.setFullStepMode()
# mot.openAndCloseDoor(distance*1, delay/1)
# time.sleep(2)

# print ("doing 1/2 steps")
# mot.setHalfStepMode()
# mot.openAndCloseDoor(distance*2, delay/2)
# time.sleep(2)

print ("doing 1/4 steps")
mot.setQuarterStepMode()
mot.openAndCloseDoor(distance*4, delay/4)
time.sleep(2)

print ("doing 1/8 steps")
mot.setEighthStepMode()
mot.openAndCloseDoor(distance*8, delay/8)
time.sleep(2)

