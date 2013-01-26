import RPi.GPIO as GPIO
import time

closed_in = 24
opened_in = 26
irsensor_in = 22

sleep_out = 19
direction_out = 21
step_out = 23

motor_delay = 0.0005

def reset():
	GPIO.output(sleep_out, GPIO.LOW)
	GPIO.output(direction_out, GPIO.LOW)
	GPIO.output(step_out, GPIO.LOW)

def sleepStepper():
	GPIO.output(sleep_out, GPIO.LOW)

def awakeStepper():
	GPIO.output(sleep_out, GPIO.HIGH)

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


GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)

GPIO.setup(closed_in, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(opened_in, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(irsensor_in, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(sleep_out, GPIO.OUT)
GPIO.setup(direction_out, GPIO.OUT)
GPIO.setup(step_out, GPIO.OUT)

reset()

while True:
	awakeStepper()
	motion = GPIO.input(irsensor_in)
	closed = GPIO.input(closed_in)
	opened = GPIO.input(opened_in)

	multi = 2

	if motion:
		forward(motor_delay, multi*1600)
		time.sleep(1)
		backward(motor_delay, multi*1600)
		time.sleep(1)

	sleepStepper()

	time.sleep(0.2)
