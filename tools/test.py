import serial
import string
import io
import time
import logging
logging.basicConfig(filename='read.log',level=logging.INFO, format='%(asctime)s %(message)s')

ser = serial.Serial(
    port='/dev/ttyAMA0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)
ser.open()
ser.isOpen()


def read_line():
	ret = ser.read(1)
	while ser.inWaiting() > 0:
		char = ser.read(1)
		ret += char
		if char == '\r':
			return ret



print "\nchecking version..."
ser.write('VER\r')
time.sleep(0.1)
response = read_line()
print "VERSION is {}\n".format(response)

print "setting up for fxd-b-tags..."
ser.write('SD2\r')
time.sleep(0.1)
response = read_line()
print "set with response: \n{}\n".format(response)

print "measure frequency..."
ser.write('MOF\r')
time.sleep(0.1)
response = read_line()
print "frequency: \n{}\n".format(response)



print "waiting for BALOU...\n"
print read_line()
while True:
	while ser.inWaiting() > 0:
		print ser.read(1)



	# response = read_line() # 18 for BALOU, 12 for TESTTAG
	# print response

ser.close()

# 756_098100641037