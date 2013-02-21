import RPi.GPIO as GPIO
import time
import serial

irsensor_in = 18

sleep_out = 23
direction_out = 21
step_out = 22

motor_delay = 0.0005

tag_length = 11
balou_tag = "04009EC1F1\r"

	port='/dev/ttyAMA0',
	baudrate=9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)

def read_line():
	ret = ser.read(1)
	while ser.inWaiting() > 0:
		char = ser.read(1)
		ret += char
		if char == '\r':
			return ret

def sleepStepper():
	GPIO.output(sleep_out, GPIO.LOW)

def awakeStepper():
	GPIO.output(sleep_out, GPIO.HIGH)

def reset():
	sleepStepper()
	GPIO.output(direction_out, GPIO.LOW)
	GPIO.output(step_out, GPIO.LOW)

def doStep(delay):
                GPIO.output(step_out, GPIO.HIGH)
                time.sleep(delay)
                GPIO.output(step_out, GPIO.LOW)
                time.sleep(delay)

def forward(delay, steps):
	GPIO.output(direction_out, GPIO.HIGH)
	for i in range(0, steps):
		doStep(delay)

def backward(delay, steps):
        GPIO.output(direction_out, GPIO.LOW)
        for i in range(0, steps):
                doStep(delay)

def checkMotion():
	print GPIO.input(irsensor_in)
	return GPIO.input(irsensor_in)

def openDoor():
	awakeStepper()
	multi = 7
	forward(motor_delay, multi*800)
	time.sleep(1)
	print "forward"
	# while checkMotion():
	# 	time.sleep(0.5)

	backward(motor_delay, multi*800)
	time.sleep(1)
	print "backward"
	sleepStepper()



GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

GPIO.setup(irsensor_in, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(sleep_out, GPIO.OUT)
GPIO.setup(direction_out, GPIO.OUT)
GPIO.setup(step_out, GPIO.OUT)

# ser.open()
# ser.isOpen()
# ser.write('SD2\r')
# time.sleep(0.1)
# response = read_line()
# print response

reset()

while True:

	# ser.write('RAT\r')
	# time.sleep(0.1)

	# response = ser.read(16)

	# print response

	# if response == '?1\r':
		# time.sleep (0.2)
	# else:
		# openDoor()
	GPIO.output(direction_out, GPIO.HIGH)
	# if checkMotion():
	openDoor()

	# time.sleep(0.2)
	








