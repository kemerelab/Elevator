import RPi.GPIO as GPIO
import time;

HIGH = 0
LOW = 1

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
checker1 = 1
checker2 = 0
trigger1 = 15
pump1 = 17
trigger2 = 18
pump2 = 22

GPIO.setup(pump1, GPIO.OUT)
GPIO.setup(trigger1, GPIO.IN)
GPIO.setup(pump2, GPIO.OUT)
GPIO.setup(trigger2, GPIO.IN)

#for outputs, 0 enables pump and 1 turns it off 

 
GPIO.output(pump1, LOW)
GPIO.output(pump2, LOW)


while True:
	if GPIO.input(trigger1) == True and checker1 == 1: 
		GPIO.output(pump1, HIGH)
		print "triggering reward! :)      1"
		time.sleep(1)
		GPIO.output(pump1, LOW)
		checker1 = 0
		checker2 = 1
	else:
		GPIO.output(pump2, LOW)
	if GPIO.input(trigger2) == True and checker2 == 1: 
		GPIO.output(pump2, HIGH)
		print "triggering reward again! :)     2"
		time.sleep(1)
		GPIO.output(pump2, LOW)
		checker2 = 0
		checker1 = 1
	else:
		GPIO.output(pump1, LOW)
		

