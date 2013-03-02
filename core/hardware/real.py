from ConfigParser import SafeConfigParser
import threading
import time
import datetime
import serial
import RPi.GPIO as GPIO

class CustomSerial(serial.Serial):
	def readLine(self):
		ret = self.read(1)
		while self.inWaiting() > 0:
			char = self.read(1)
			ret += char
			if char == '\r':
				return ret	

class WatchdogThread(threading.Thread):
	def __init__(self, hardware):
		self.exitFlag = False
		self.hardware = hardware
		self.ser = hardware.ser
		threading.Thread.__init__(self)

	def run(self):
		while True:
			if self.hardware.ser.inWaiting() > 0:
				self.hardware.pendingSerialValue = self.hardware.ser.readLine()
				self.hardware.pendingSerialBool = True

			self.hardware.motionDetectedBool = GPIO.input(self.hardware.pin_irsensor_in)

			if self.exitFlag == True:
				break

			time.sleep(0.5)

	def exit(self):
		self.exitFlag = True


class Hardware:
	ser = None
	pendingSerialBool = False
	pendingSerialValue = None
	motionDetectedBool = False

	def __init__(self):

		self.loadConfig()
		self.initializeHardware()
		self.configureSerialReader()


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

	def configureSerialReader(self):	
		self.ser = CustomSerial(port='/dev/ttyAMA0', baudrate=9600, parity=serial.PARITY_NONE,	stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
		self.ser.open()

		print "\nchecking version..."
		self.ser.write('VER\r')
		time.sleep(0.1)
		response = self.ser.readLine()
		print "VERSION is {}\n".format(response)

		print "setting up for fxd-b-tags..."
		self.ser.write('SD2\r')
		time.sleep(0.1)
		response = self.ser.readLine()
		print "set with response: \n{}\n".format(response)

		print "measure frequency..."
		self.ser.write('MOF\r')
		time.sleep(0.1)
		response = self.ser.readLine()
		print "frequency: \n{}\n".format(response)

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
		multi = 7
		GPIO.output(self.pin_direction_out, GPIO.HIGH)
		for i in range(0, multi*850):
			self.doStep(self.motor_delay)
		self.sleepStepper();

	def closeDoor(self):
		self.doShortBeeps(5)
		self.awakeStepper()
		multi = 7
		GPIO.output(self.pin_direction_out, GPIO.LOW)
		for i in range(0, multi*850):
			self.doStep(self.motor_delay)
		self.sleepStepper();
		
	def doShortBeeps(self, num):
		for i in range(0,num):
			self.beep()

	def beep(self):
		print "beeping..."
		GPIO.output(self.pin_buzzer_out, GPIO.HIGH)
		time.sleep(0.1)
		GPIO.output(self.pin_buzzer_out, GPIO.LOW)
		time.sleep(0.05)

	def isSerialPending(self):
		return self.pendingSerialBool

	def isMotionDetected(self):
		if self.motionDetectedBool:
			self.motionDetectedBool = false
			return True;
		else:
			return False;

	def activateWatchdog(self):
		self.workerThread = WatchdogThread(self)
		self.workerThread.start()

	def deactivateWatchdog(self):		
		self.workerThread.exit()

	def getPendingSerial(self):
		self.pendingSerialBool = False
		return self.pendingSerialValue


blubb = Hardware()
blubb.activateWatchdog()
print datetime.datetime.now()
print "stated watchdog"


while True:
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
		blubb.closeDoor()

	time.sleep(0.5)

blubb.deactivateWatchdog()


