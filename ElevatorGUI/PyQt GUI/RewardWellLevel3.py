import RPi.GPIO as GPIO
import time;

HIGH = 0
LOW = 1

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
checker1 = 1
checker2 = 0
trigger5 = 25
pump5 = 13 	
trigger6 = 8
pump6 = 26

GPIO.setup(pump5, GPIO.OUT)
GPIO.setup(trigger5, GPIO.IN)
GPIO.setup(pump6, GPIO.OUT)
GPIO.setup(trigger6, GPIO.IN)

#for outputs, 0 enables pump and 1 turns it off 

GPIO.output(pump5, LOW)
GPIO.output(pump6, LOW)


while True:
	if GPIO.input(trigger5) == True and checker1 == 1: 
		GPIO.output(pump5, HIGH)
		print "triggering reward! :)	5"
		time.sleep(1)
		GPIO.output(pump5,LOW)
		checker1 = 0
		checker2 = 1
	else:
		GPIO.output(pump6,LOW)
	if GPIO.input(trigger6) == True and checker2 == 1: 
		GPIO.output(pump6, HIGH)
		print "triggering reward again! :)		6"
		time.sleep(1)
		GPIO.output(pump6,LOW)
		checker2 = 0
		checker1 = 1
	else:
		GPIO.output(pump5,LOW)
