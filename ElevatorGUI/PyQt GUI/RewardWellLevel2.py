import RPi.GPIO as GPIO
import time;

HIGH = 0
LOW = 1

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
checker1 = 1
checker2 = 0
trigger3 = 23#might cause an error, 4 or 04
pump3 = 10 #might cause an error, 2 or 02
trigger4 = 24
pump4 = 11

GPIO.setup(pump3, GPIO.OUT)
GPIO.setup(trigger3, GPIO.IN)
GPIO.setup(pump4, GPIO.OUT)
GPIO.setup(trigger4, GPIO.IN)

#for outputs, 0 enables pump and 1 turns it off 

GPIO.output(pump3, LOW)
GPIO.output(pump4, LOW)


while True:
	if GPIO.input(trigger3) == True and checker1 == 1: 
		GPIO.output(pump3, HIGH)
		print "triggering reward! :)      3"
		time.sleep(1)
		GPIO.output(pump3,LOW)
		checker1 = 0
		checker2 = 1
	else:
		GPIO.output(pump4, LOW)
	if GPIO.input(trigger4) == True and checker2 == 1: 
		GPIO.output(pump4, HIGH)
		print "triggering reward again! :)     4"
		time.sleep(1)
		GPIO.output(pump4, LOW)
		checker2 = 0
		checker1 = 1
	else:
		GPIO.output(pump3, LOW)
		
