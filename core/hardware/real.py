from ConfigParser import SafeConfigParser
import threading
import time
import serial
import RPi.GPIO as GPIO

class WatchdogThread(threading.Thread):
	def __init__(self, ser):
		self.exitFlag = False
		self.ser = ser
		threading.Thread.__init__(self)

	def run(self):
		while True:
			print "Thread running"
			if self.ser.inWaiting() > 0:
				self.pendingSerialValue = self.ser.readLine()
				self.pendingSerialBool = True

			if self.exitFlag == True:
				break

			time.sleep(0.5)

	def exit(self):
		self.exitFlag = True

	
			


class CustomSerial(serial.Serial):
	def readLine(self):
		ret = self.read(1)
		while self.inWaiting() > 0:
			char = self.read(1)
			ret += char
			if char == '\r':
				return ret	

class Hardware:

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
		GPIO.cleanup()
		GPIO.setmode(GPIO.BCM)

		GPIO.setup(self.pin_irsensor_in, GPIO.IN, pull_up_down=GPIO.PUD_UP)

		GPIO.setup(self.pin_sleep_out, GPIO.OUT)
		GPIO.setup(self.pin_direction_out, GPIO.OUT)
		GPIO.setup(self.pin_step_out, GPIO.OUT)
		GPIO.setup(self.pin_buzzer_out, GPIO.OUT)

		self.sleepStepper()
		GPIO.output(self.pin_direction_out, GPIO.LOW)
		GPIO.output(self.pin_step_out, GPIO.LOW)
		GPIO.output(self.pin_buzzer_out, GPIO.LOW)

	def configureSerialReader():	
		self.ser = CustomSerial(port='/dev/ttyAMA0', baudrate=9600, parity=serial.PARITY_NONE,	stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
		self.ser.open()
		self.ser.isOpen()
		self.ser.write('SD2\r') #configure the type of the rfid-tag
		time.sleep(0.1)
		response = serial_read_line()

	def sleepStepper(self):
		GPIO.output(self.pin_sleep_out, GPIO.LOW)

	def awakeStepper(self):
		GPIO.output(self.pin_sleep_out, GPIO.HIGH)

	def openDoor(self):
		pass
	def closeDoor(self):
		pass
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

	def activateWatchdog(self):
		self.workerThread = WatchdogThread(self.ser)
		self.workerThread.start()

	def deactivateWatchdog(self):		
		self.workerThread.exit()

	def getPendingSerial(self):
		self.pendingSerialBool = False
		return self.pendingSerialValue


blubb = Hardware()
blubb.activateWatchdog()
time.sleep(6)
blubb.deactivateWatchdog()
