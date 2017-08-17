# Refer to the following link for PyQt documentation:
# http://pyqt.sourceforge.net/Docs/PyQt4/classes.html
# Written for AMIS-30543 driver.

'''
At an RPM of 60 and an input of 200 steps in mode 1/1, takes motor 1 second to complete task
At an RPM of 120 and an input of 200 steps in mode 1/2, takes motor 1 second to complete task
'''
import sys
import RNELBanner_rc
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QPalette
from serial import *
#imports for multithreading
from threading import Thread, Event

import multiprocessing
import math

import socket
import os
import signal
import RPi.GPIO as GPIO
##### imports for picamera
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
from scipy.misc import imresize

import globalvars

import struct

import Queue
##### end

minHeight, maxHeight = 0, 200000

#global doorclose
#doorclose = True

try:
    arduino = Serial('/dev/ttyACM0', 9600)
    print("successfully connected to orig arduino!")
except:
    arduino = None
    pass

try:
    arduinoservodoor = Serial('/dev/ttyACM1', 9600)
    print("successfully connected to servo arduino!")
except:
    arduinoservodoor = None
    pass
    
try:
    arduinoCapSense = Serial('/dev/ttyACM2', 115200)
    print("successfully connected to cap sensor arduino!")
except:
    arduinoCapSense = None
    pass    

#doorclose = True
target = open("/home/kemerelab/Desktop/CapSenseData.out", 'w')

class Capacitance(QtCore.QThread):
#   def __init__(self, threadID, name):
#      Thread.__init__(self)
#      self.threadID = threadID
#      self.name = capacitiveSensorThread
   
   def run(self):
        while globalvars.quitThread == False:
            if (arduinoCapSense is not None): 
                arduinoCapSense.flushInput()
                capdatatotal = arduinoCapSense.readline()
                target.write(capdatatotal)
                self.emit(QtCore.SIGNAL('CAP'), capdatatotal)
                time.sleep(1.5)

class Ui_Form(QtGui.QWidget):
    def __init__(self):
        super(Ui_Form, self).__init__()
        self.currentPosition = 0
        self.level_position = {1:0, 2:1000, 3:2000}

#        self.doorclose = True
        self.setupUi()
    
    
    def closeEvent(self, event):
        target.close()
        globalvars.quitThread = True
        time.sleep(1)
        t2.join()
        print "User has clicked the red x on the main window"
        event.accept()
	

    def setupUi(self):


        #self.threadclass = level()
        #self.threadclass.start()
      
        #self.connect(self, QtCore.SIGNAL('LEVEL'), self.threadclass) 

        self.setWindowTitle("RNEL Elevator Controller")
        rowSpacer = QtGui.QSpacerItem(1, 20)
        columnSpacer = QtGui.QSpacerItem(50, 1)

        # Highlight input that is currently selected
        self.setFocusPolicy(QtCore.Qt.ClickFocus)

        # Create UI elements
        label_banner = QtGui.QLabel()
        label_banner.setText("")
        label_banner.setPixmap(QtGui.QPixmap(":/RNELicon/RNELBanner.png"))

        font = QtGui.QFont("Helvetica", 12, 75)
        font.setBold(True)
        label_motorState = QtGui.QLabel("Stepper Motor Parameters")
        label_motorState.setFont(font)

        label_time = QtGui.QLabel("Time Between Levels (seconds):")
        label_steps = QtGui.QLabel("Distance (in):")
        label_wheeldiameter = QtGui.QLabel("Wheel Diameter (in)")
        label_direction = QtGui.QLabel("Direction:")
        label_mode = QtGui.QLabel("Mode:")
        #label_torque = QtGui.QLabel("Torque:")
		
        label_capacitance = QtGui.QLabel("Capacitance: ") #LOOK HERE	
        label_capacitance.setFont(font)

        self.capacitance = QtGui.QLCDNumber(self) #LOOK HERE 
        self.capacitance.setFont(font)
        palette = QPalette()
       # palette.setBrush(QtGui.QPalette.Light, QtCore.Qt.black)
        brush = QtGui.QBrush(QtGui.QColor(0,0,0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        self.capacitance.setPalette(palette)

        self.capacitance.setDigitCount(8)
        self.threadclass = Capacitance()
        self.threadclass.start()
		
        self.connect(self.threadclass, QtCore.SIGNAL('CAP'), self.updateCapacitance)        
        
        self.capacitance.display(0) # just so something is there
                
        self.lineEdit_time = QtGui.QLineEdit()
        self.lineEdit_time.setMaximumSize(QtCore.QSize(100, 30))
        self.lineEdit_time.setText("0")
        self.lineEdit_distance = QtGui.QLineEdit()
        self.lineEdit_distance.setMaximumSize(QtCore.QSize(100, 30))
        self.lineEdit_distance.setText("0")
        self.lineEdit_wheeldiameter = QtGui.QLineEdit()
        self.lineEdit_wheeldiameter.setText("1")
        self.comboBox_direction = QtGui.QComboBox()
        self.comboBox_direction.addItems(["Up", "Down"])
        self.comboBox_mode = QtGui.QComboBox()
        self.comboBox_mode.addItems(["1/1", "1/2", "1/4", "1/8", "1/16", "1/32", "1/64", "1/128"])
        self.comboBox_mode.setCurrentIndex(0)
        #self.comboBox_torque = QtGui.QComboBox()
        #self.comboBox_torque.addItems(["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%"])
        #self.comboBox_torque.setCurrentIndex(4)

        #Preset Levels >>> assign each to a 12" distance later

        self.preset_checkbox = QtGui.QCheckBox("Use preset elevator levels")
        self.preset_checkbox.setCheckState(False)
        self.preset_checkbox.setTristate(False)
        label_level = QtGui.QLabel("Level:")
        self.comboBox_level = QtGui.QComboBox()
        self.comboBox_level.addItems(["1", "2", "3"])
        self.comboBox_level.setEnabled(False)

        label_assign = QtGui.QLabel("Assign position to level?")
        self.btn_assign = QtGui.QPushButton("Assign")
        self.btn_assign.setEnabled(False)

        self.btn_run = QtGui.QPushButton("Run")
        self.btn_doorstat = QtGui.QPushButton("Open/Close")
        self.progress_bar = QtGui.QProgressBar()
        self.btn_doorstat = QtGui.QPushButton("Open/Close")

        label_history = QtGui.QLabel("Command History")
        label_history.setFont(font)
        self.command_history = QtGui.QPlainTextEdit()
        self.command_history.setMaximumSize(QtCore.QSize(1000, 500))
        self.command_history.setReadOnly(True)
        self.command_history.appendPlainText("Note: The speed will be scaled according to the microstepping mode.")
        self.command_history.appendPlainText("Note: The time and distance inputs must be positive integers. Numbers that are not integers will be rounded down.")
        self.command_history.appendPlainText("")

        font = QtGui.QFont("Helvetica", 12)
        label_instructions = QtGui.QLabel("Please visit the following site for instructions:")
        label_instructions.setFont(font)

        label_website = QtGui.QLabel()
        label_website.setFont(font)
        label_website.setText("<a href=\"https://github.com/kemerelab/Elevator/\">Elevator Maze</a>")
        label_website.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        label_website.setOpenExternalLinks(True)

        # Format UI elements
        formLayout = QtGui.QFormLayout()
        formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        formLayout.setLabelAlignment(QtCore.Qt.AlignLeft)
        formLayout.addRow(label_time, self.lineEdit_time)
        formLayout.addRow(label_steps, self.lineEdit_distance)
        formLayout.addRow(label_direction, self.comboBox_direction)
        formLayout.addRow(label_mode, self.comboBox_mode)
        #formLayout.addRow(label_torque, self.comboBox_torque)
        formLayout.addRow(label_wheeldiameter, self.lineEdit_wheeldiameter)
       

        formLayout2 = QtGui.QFormLayout()
        formLayout2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        formLayout2.setLabelAlignment(QtCore.Qt.AlignLeft)
        formLayout2.addRow(label_level, self.comboBox_level)

        formLayout2.addRow(label_capacitance, self.capacitance) #LOOK HERE

        verticalLayout = QtGui.QVBoxLayout()
        verticalLayout.addWidget(self.preset_checkbox)
        verticalLayout.addLayout(formLayout2)
        verticalLayout.addStretch()
        verticalLayout.addWidget(label_assign)
        verticalLayout.addWidget(self.btn_assign, 0, QtCore.Qt.AlignHCenter)

        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.addLayout(formLayout)
        horizontalLayout.addSpacerItem(columnSpacer)
        horizontalLayout.addLayout(verticalLayout)

        verticalLayout2 = QtGui.QVBoxLayout(self)
        verticalLayout2.setContentsMargins(30, 20, 30, 20)
        verticalLayout2.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        verticalLayout2.addWidget(label_banner, 0, QtCore.Qt.AlignHCenter)
        verticalLayout2.addSpacerItem(rowSpacer)
        verticalLayout2.addWidget(label_motorState)
        verticalLayout2.addLayout(horizontalLayout)
        verticalLayout2.addWidget(self.btn_run, 0, QtCore.Qt.AlignHCenter)
        verticalLayout2.addWidget(self.btn_doorstat, 0, QtCore.Qt.AlignRight)
        verticalLayout2.addWidget(self.progress_bar)
        verticalLayout2.addSpacerItem(rowSpacer)
        formLayout3 = QtGui.QFormLayout()
        verticalLayout2.addLayout(formLayout3)


        formLayout3.addRow(label_capacitance, self.capacitance) #LOOK HERE
     
        verticalLayout2.addWidget(label_history)
        verticalLayout2.addWidget(self.command_history)
        verticalLayout2.addSpacerItem(rowSpacer)
        verticalLayout2.addWidget(label_instructions)
        verticalLayout2.addWidget(label_website)



        self.btn_run.clicked.connect(self.collectMotorData)
        self.btn_doorstat.clicked.connect(self.sendServoData)
        self.preset_checkbox.stateChanged.connect(self.updateUI)
        self.comboBox_level.currentIndexChanged.connect(self.updateUI)
        self.btn_assign.clicked.connect(self.assignPosition)
        self.btn_assign.clicked.connect(self.updateUI)


    def updateCapacitance(self, val):
        self.capacitance.display(val)
    
    def calculateSteps (self):
        """
        Distance to be traveled divided by the circumference of the wheel (distance
        covered in one rotation) and multiplied by 200 (number of steps in one 
        rotation of the stepper) in order to find number of steps that need to be
        taken to reach desired location.
        """
        print(float(self.lineEdit_distance.text()))
        self.steppersteps = (float(self.lineEdit_distance.text()) / (math.pi * float(self.lineEdit_wheeldiameter.text()))) * (200 * float(self.comboBox_mode.currentText()[2:]))
        print(self.steppersteps)
        return self.steppersteps
    
    def delay(self):
        """
        Total time for a level change divided by 2 times the number of steps 
        required to get the desired distance change (to account for rests between
        steps) and the mode (to account for microstepping).
        """
        #Delay times are approximations as the steps will be rounded later
        self.delaytime = float(self.lineEdit_time.text()) / (2 * float(self.steppersteps))
        self.delaytime *= 1000
        print("delay:", self.delaytime)
        return self.delaytime
        
    def reqRPM(self):
        """
        Find RPM based off of number of steps needed to move a desired distance 
        times mode, and divided by 200
        """
        reqspeed = (self.steppersteps)/(200 * int(self.comboBox_mode.currentText()[2:]))
        reqspeed_valid = True
        if reqspeed > 200 or reqspeed < 0:
            reqspeed_valid = False
        print(reqspeed)
        return reqspeed, reqspeed_valid

    def collectMotorData(self):
        
        #speed, speed_valid = QtCore.QString.toFloat(self.lineEdit_speed.text())
        #torque = str(self.comboBox_torque.currentText()[0])

        # If preset levels are used, calculate steps and direction

        #### NEEDS TO BE REDONE********

        #Not using preset levels

        if self.preset_checkbox.checkState() == 2:
            steps_valid = True
            steps, direction = self.level_calculations()
        else:
            #steps, steps_valid = QtCore.QString.toFloat(self.lineEdit_distance.text())
            steps = int(self.calculateSteps())
            direction = str(self.comboBox_direction.currentText())
            if direction == "Up" and steps >= maxHeight - self.currentPosition:
                steps_valid = True
            elif direction == 'Down' and steps <= self.currentPosition - minHeight:
                steps_valid = True
            else:
                steps_valid = False
        
        speed, speed_valid = self.reqRPM()
        
        stepdelay = self.delay()
        
        #if speed_valid == False or steps_valid == False:
         #   self.errorMessage(0)
        #if speed == 0 and speed_valid == True:
         #   self.errorMessage(1)
        #if speed > 200 or speed < 0:
         #   self.errorMessage(2)
            #self.level_position(2)
          #  speed = 0
           # steps = 0
        #speed = int(speed)
        #if(speed != 0):
            #if steps == 0 and steps_valid == True:
                #if self.preset_checkbox.checkState() == 0:
                 #   self.errorMessage(3)
                #if self.preset_checkbox.checkState() == 2:
               #     self.errorMessage(6)
            #if steps < 0:
             #   self.errorMessage(8)
              #  steps = 0
        #steps = int(steps)

        # Do not step past the top and bottom of the maze
        if direction == "Up" and speed != 0:
            if steps > maxHeight - self.currentPosition:
                self.errorMessage(4)
                steps = maxHeight - self.currentPosition
            self.currentPosition += int(steps)
        if direction == "Down" and speed != 0:
            if steps > self.currentPosition - minHeight:
                self.errorMessage(5)
                steps = self.currentPosition - minHeight
            self.currentPosition -= int(steps)

        # Using a microstepping mode of 1/2, for example, halves the number of steps
        # Multiply the number of steps by the reciprocal of the mode
        # This will not affect position tracking as it occurs after position tracking
        #print (mode)
        self.sendMotorData(str(speed), str(int(self.steppersteps)), self.comboBox_mode.currentText()[2:], direction, str(stepdelay))
        
    def sendMotorData(self, speed, steps, mode, direction, delay):
        self.btn_run.setEnabled(False)

        #while len(speed) < 4:
        #    speed = "0" + speed

        #while len(steps) < 8:
        #    steps = "0" + steps
        #while len(mode) < 3:
        #    mode = "0" + mode
        #while len(delay) < 6:
        #    delay = "0" + delay

        data = str('x'+speed+'x'+steps+'x'+mode+'x'+delay+'x'+direction)
        print("stepper data:", data)
        self.command_history.appendPlainText(data)
        self.command_history.appendPlainText("Estimated time required (seconds): " + self.lineEdit_time.text())

        # self.sendServoData()

        try:
            
            arduino.write(data)
            self.update_progress(int(self.steppersteps))
            
            #arduino.write("On")
            
            # In a separate thread, block new inputs until Arduino is ready
            #if self.steps != 0:
                #self.progress_bar.setRange(0, self.steps)
                #self.motor_progress = update_thread(self.steps)
                #self.motor_progress.start()
                #self.motor_progress.bar_value.connect(self.update_progress)
            #else:
                #self.update_progress(0)
        except:
            self.command_history.appendPlainText("The Arduino is not connected.")
            self.btn_run.setEnabled(True)
		#### I think hall effect sensor reading should go here
        self.command_history.appendPlainText("Current position: " + str(self.currentPosition))
        self.command_history.appendPlainText("")
	
    def sendServoData(self):
        if globalvars.doorclose:
            try:
                arduinoservodoor.write("0")
                globalvars.doorclose = not globalvars.doorclose
                if(globalvars.doorclose):
                    print("Door Closed")
                else:
                    print("Door Open")
                if(arduinoCapSense is not None): 
                    target.write("door open\n")
            except:
                self.command_history.appendPlainText("Error reading from servo arduino\n")
        else:	
            try:
                arduinoservodoor.write("90")
                globalvars.doorclose = not globalvars.doorclose
                if(globalvars.doorclose):
                    print("Door Closed")
                else:
                    print("Door Open")
                try:
                    #while True:
                    if(arduinoCapSense is not None):
                        arduinoCapSense.flushInput()
                        capdata = arduinoCapSense.readline()
                        target.write(capdata)
                        target.write("door closed\n")
                    #target.write("\n")
                        print capdata
                        #values = line.decode('ascii').split(':')
                        #print arduinoCapSense.readline()
                        #print (values)
                  #  time.sleep(0.001)
                    #for byte in arduinoCapSense.read():
                        #print(ord(byte))
                        #byte_range = bytearray(b'\x85W\xe2\xa2I')
                        #date_header = struct.unpack('>BL', byte_range)
                except:
                    self.command_history.appendPlainText("Error writing to capacitive sensor arduino\n")
            except:
                self.command_history.appendPlainText("Error writing to servo arduino\n")

    def level_calculations(self):
        # This method is called in collectMotorData() and updateUI()
        current_level = int(self.comboBox_level.currentText())
        #self.emit(QtCore.SIGNAL('LEVEL'), current_level)
		
        steps = abs(self.currentPosition - self.level_position[current_level])
        if self.currentPosition > self.level_position[current_level]:
            direction = "Down"
        else:
            direction = "Up"
        return steps, direction

    def assignPosition(self):
        # Reassign elevator levels if necessary
        current_level = int(self.comboBox_level.currentText())
        difference = self.currentPosition - self.level_position[current_level]
        if difference != 0:        
            for level in self.level_position.keys():
                self.level_position[level] += difference
            self.command_history.appendPlainText("New level positions:")
        else:
            self.errorMessage(7)
            self.command_history.appendPlainText("Current level positions:")

        self.command_history.appendPlainText("Level 1: " + str(self.level_position[1]))
        self.command_history.appendPlainText("Level 2: " + str(self.level_position[2]))
        self.command_history.appendPlainText("Level 3: " + str(self.level_position[3]))
        self.command_history.appendPlainText("")

    def updateUI(self):
        steps, direction = self.level_calculations()
        # If preset levels are used, disable corresponding manual inputs
        if self.preset_checkbox.checkState() == 0:
            self.lineEdit_distance.setEnabled(True)
            self.lineEdit_distance.setText("0")
            self.comboBox_direction.setEnabled(True)
            self.comboBox_level.setEnabled(False)
            self.btn_assign.setEnabled(False)
        if self.preset_checkbox.checkState() == 2:
            self.lineEdit_distance.setEnabled(False)
            self.lineEdit_distance.setText(str(steps))
            self.comboBox_direction.setEnabled(False)
            if direction == "Up":
                self.comboBox_direction.setCurrentIndex(0)
            else:
                self.comboBox_direction.setCurrentIndex(1)
            self.comboBox_level.setEnabled(True)
            self.btn_assign.setEnabled(True)

    def errorMessage(self, num):
        invalid_box = QtGui.QMessageBox()
        invalid_box.setIcon(QtGui.QMessageBox.Warning)

        if num == 0:
            invalid_box.setText("<br>Invalid input(s).")
            invalid_box.setInformativeText("<big>Inputs must be numbers.")
        if num == 1:
            invalid_box.setText("<br>The speed has not been set.")
            invalid_box.setInformativeText("<big>Please set a speed to start the motor.")
        if num == 2:
            invalid_box.setText("<br>The speed cannot be set.")
            invalid_box.setInformativeText("<big>The speed must be greater than 0 but less than the maximum RPM of 150. The steps have been set to 0. Please try again at a lower speed.")           
        if num == 3:
            invalid_box.setText("<br>The distance has not been set.")
            invalid_box.setInformativeText("<big>Please set a distance to start the motor.") 
        if num == 4:
            invalid_box.setText("<br>Distance exceeds maze height.")
            invalid_box.setInformativeText("<big>The elevator will stop at the top of the maze.")
        if num == 5:
            invalid_box.setText("<br>Distance exceeds bottom of maze.")
            invalid_box.setInformativeText("<big>The elevator will stop at the bottom of the maze.")
        if num == 6:
            invalid_box.setText("<br>The distance cannot be set.")
            invalid_box.setInformativeText("<big>The elevator is already on this level.")  
        if num == 7:
            invalid_box.setText("<br>The levels cannot be assigned.")
            invalid_box.setInformativeText("<big>This level is already assigned to the current position.")
        if num == 8:
            invalid_box.setText("<br>The distance cannot be set.")
            invalid_box.setInformativeText("<big>The number of steps must be greater than 0.")             

        invalid_box.exec_()

    def update_progress(self, num):
        self.progress_bar.setValue(num)
        #self.btn_run.setText(str(num) + "/" + str(int(self.steppersteps)))

        # Allow new input when motor is done stepping
        if num == int(self.steppersteps):
            self.btn_run.setText("Run")
            self.btn_run.setEnabled(True)
            self.progress_bar.reset()
            #if self.preset_checkbox.checkState() == 2:
            self.updateUI()


class update_thread(QtCore.QThread):
    bar_value = QtCore.pyqtSignal(int)

    def __init__(self, steps):
        super(update_thread, self).__init__()
        self.steps = steps
    
    def run(self):
        # Track steps completed by reading serial port       
        all_entries = []
        step_entry = []
        lencount = len(all_entries)
        count = 0
        while len(all_entries) < self.steps:
            if lencount == len(all_entries):
                count += 1
                if count > 5:
                    self.bar_value.emit(self.steps)
                    break
            lencount = len(all_entries)
            for byte in arduino.read():                
                count = 0                
                #print (byte)
                step_entry.append(byte)
                #print (step_entry)
                
                #length of previous all_entries
                #compare to current length
                #if value is same increment counter
                #update lencount               
                if byte == '\n':
                    all_entries.append(step_entry)
                    #print(all_entries)
                    self.bar_value.emit(len(all_entries))
                    step_entry = []
            #print (len(all_entries),"moo", count)
            

class level(QtCore.QThread): #shows what level we are on and will run the reward wells
	
	def run (self):
		
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		checker1 = 1
		checker2 = 0
		trigger1 = 26
		pump1 = 13
		trigger2 = 21
		pump2 = 16

		GPIO.setup(pump1, GPIO.OUT)
		GPIO.setup(trigger1, GPIO.IN)
		GPIO.setup(pump2, GPIO.OUT)
		GPIO.setup(trigger2, GPIO.IN)

		#for outputs, 0 enables pump and 1 turns it off 

		while True:
			if GPIO.input(trigger1) == True and checker1 == 1: 
				GPIO.output(pump1, 0)
				print "triggering reward! :)"
				time.sleep(5)
				GPIO.output(pump1,1)
				checker1 = 0
				checker2 = 1
			else:
				GPIO.output(pump2,1)
			if GPIO.input(trigger2) == True and checker2 == 1: 
				GPIO.output(pump2, 0)
				print "triggering reward again! :)"
				time.sleep(5)
				GPIO.output(pump2,1)
				checker2 = 0
				checker1 = 1
			else:
				GPIO.output(pump1,1)



class receiving(QtCore.QThread):
	def run(self):
		UDP_IPr = "127.0.0.1"
		UDP_PORTr = 5005
		
		sockr = socket.socket(socket.AF_INET, # Internet
		                     socket.SOCK_DGRAM) # UDP
		sockr.bind((UDP_IPr, UDP_PORTr))
		while True:
			data, addr = sockr.recvfrom(1024) # buffer size is 1024 bytes
			data = float (data)
			self.emit(QtCore.SIGNAL('CAP'), data)

#def collectServoData(self, q):
#    doorclose = self.doorclose
#    q.put(doorclose)    

def callPiCamDisplay():
	os.system('python PiCamDisplay.py')

#def callRewardWell1():
#	os.system('python RewardWellLevel1.py')

#def callRewardWell2():
#	os.system('python RewardWellLevel2.py')

#def callRewardWell3():
#	os.system('python RewardWellLevel3.py')

#def callRewardWell():
	#os.system('python RewardWell.py')

def callRewardWells():
    HIGH = 0
    LOW = 1

#    doorclose = Event()
#    if not obj:
#        doorclose.set()
#    elif obj:
#        doorclose.clear()

#    print obj
#    print doorclose
    
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    wellnum = 0
    checker1 = 1
    checker2 = 1
    checker3 = 1
    checker4 = 1
    checker5 = 1
    checker6 = 1
    trigger1 = 15
    pump1 = 17
    trigger2 = 18
    pump2 = 22
    trigger3 = 23#might cause an error, 4 or 04
    pump3 = 10 #might cause an error, 2 or 02
    trigger4 = 24
    pump4 = 11
    trigger5 = 25
    pump5 = 13 	
    trigger6 = 8
    pump6 = 26

    cap_resetpin = 21
    GPIO.setup(cap_resetpin, GPIO.OUT)

    GPIO.setup(pump1, GPIO.OUT)
    GPIO.setup(trigger1, GPIO.IN)
    GPIO.setup(pump2, GPIO.OUT)
    GPIO.setup(trigger2, GPIO.IN)
    GPIO.setup(pump3, GPIO.OUT)
    GPIO.setup(trigger3, GPIO.IN)
    GPIO.setup(pump4, GPIO.OUT)
    GPIO.setup(trigger4, GPIO.IN)
    GPIO.setup(pump5, GPIO.OUT)
    GPIO.setup(trigger5, GPIO.IN)
    GPIO.setup(pump6, GPIO.OUT)
    GPIO.setup(trigger6, GPIO.IN)

    #for outputs, 0 enables pump and 1 turns it off 

    GPIO.output(pump1, LOW)
    GPIO.output(pump2, LOW)
    GPIO.output(pump3, LOW)
    GPIO.output(pump4, LOW)
    GPIO.output(pump5, LOW)
    GPIO.output(pump6, LOW)
    GPIO.output(cap_resetpin, LOW)
    

    while globalvars.quitThread == False:
        #print obj
        time.sleep(0.05)
        if globalvars.doorclose:

#            doorclose.set()

            if wellnum == 1:
                checker2 = 1
                wellnum = 0
                #print checker2
            elif wellnum == 2:
                checker1 = 1
                wellnum = 0
                #print checker1
            elif wellnum == 3:
                checker4 = 1
                wellnum = 0
                #print checker4
            elif wellnum == 4:
                checker3 = 1
                wellnum = 0
                #print checker3
            elif wellnum == 5:
                checker6 = 1
                wellnum = 0
                #print checker6
            elif wellnum == 6:
                checker5 = 1
                wellnum = 0
                #print checker5
        
        elif not globalvars.doorclose and wellnum == 0:

#            doorclose.clear()
            trig1input = GPIO.input(trigger1)
            #print(trig1input)
            trig2input = GPIO.input(trigger2)
            #print(trig2input)
            if trig1input == True and checker1 == 1: 
                GPIO.output(pump1, HIGH)
                GPIO.output(cap_resetpin, HIGH)
                print "triggering reward! :)      1"
                checker2 = 0	    
                time.sleep(1)
                GPIO.output(pump1, LOW)
                GPIO.output(cap_resetpin, LOW)
                checker1 = 0
                wellnum = 1
    #            print checker2
#                doorclose.wait()
                checker2 = 1
                print checker2
                
            
            elif trig2input == True and checker2 == 1: 
                GPIO.output(pump2, HIGH)
                GPIO.output(cap_resetpin, HIGH)
                print "triggering reward! :)     2"
                checker1 = 0        
                time.sleep(1)
                GPIO.output(pump2, LOW)
                GPIO.output(cap_resetpin, LOW)
                checker2 = 0
                wellnum = 2
    #            print checker1
                print wellnum
    #            doorclose.wait()
                checker1 = 1
    #            print checker1
            
            elif GPIO.input(trigger3) == True and checker1 == 3: 
                GPIO.output(pump3, HIGH)
                GPIO.output(cap_resetpin, HIGH)
                print "triggering reward! :)      3"
                checker4 = 0	    
                time.sleep(1)
                GPIO.output(pump3, LOW)
                GPIO.output(cap_resetpin, LOW)
                checker3 = 0
                wellnum = 3
                print wellnum
    #            print checker4
    #            doorclose.wait()
                checker4 = 1
    #            print checker4
                
            elif GPIO.input(trigger4) == True and checker4 == 1: 
                GPIO.output(pump4, HIGH)
                GPIO.output(cap_resetpin, HIGH)
                print "triggering reward! :)     4"
                checker3 = 0        
                time.sleep(1)
                GPIO.output(pump4, LOW)
                GPIO.output(cap_resetpin, LOW)
                checker4 = 0
                wellnum = 4
    #            print checker3
#                doorclose.wait()
                checker3 = 1
                print checker3
                
            elif GPIO.input(trigger5) == True and checker5 == 1: 
                GPIO.output(pump5, HIGH)
                GPIO.output(cap_resetpin, HIGH)
                print "triggering reward! :)      5"
                checker6 = 0	    
                time.sleep(1)
                GPIO.output(pump5, LOW)
                GPIO.output(cap_resetpin, LOW)
                checker5 = 0
                wellnum = 5
    #            print checker6
#                doorclose.wait()
                checker6 = 1
                print checker6
                
            elif GPIO.input(trigger6) == True and checker6 == 1: 
                GPIO.output(pump6, HIGH)
                GPIO.output(cap_resetpin, HIGH)
                print "triggering reward! :)     6"
                checker5 = 0        
                time.sleep(1)
                GPIO.output(pump6, LOW)
                GPIO.output(cap_resetpin, LOW)
                checker6 = 0
                wellnum = 6
    #            print checker5
#                doorclose.wait()
                checker5 = 1
                print checker5
                
t2 = Thread(target = callRewardWells, args = ())           

if __name__ == '__main__':

#    p = multiprocessing.Process(target = callPiCamDisplay)
#    p.start()
	#time.sleep(5)
	#os.kill(p.pid, signal.SIGKILL)
#	q = multiprocessing.Process(target = callRewardWell1)
#	q.start()

#	w = multiprocessing.Process(target = callRewardWell2)
#	w.start()

#	e = multiprocessing.Process(target = callRewardWell3)
#	e.start()
    #global doorclose
    globalvars.doorclose = True
   
    #print globalvars.doorclose in globals()
    #print "It's okay if it's false b/c you have import access to it"
        
    app = QtGui.QApplication(sys.argv)
    ex = Ui_Form()
    ex.show()
    
    ex.raise_()
    
#    q = Queue.Queue()
    
#    t1 = Thread(target = collectServoData, args = (ex.doorclose))
    #t2 = Thread(target = callRewardWells, args = ())
#    t1.start()
    t2.start()


#    ex.raise_()

    sys.exit(app.exec_())
    #target.close()
    #print "closed!"
#    t1.join()
    #t2.join()
	

