# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ElevatorController_v2.ui'
#
# Created: Tue Jun  9 12:11:32 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

import sys
import RNELBanner_rc
from PyQt4 import QtCore, QtGui
from serial import *

arduino = Serial('/dev/cu.usbmodem1411', 115200)

class Ui_Form(QtGui.QWidget):
    def __init__(self):
        super(Ui_Form, self).__init__()
        self.currentPosition = 0
        self.setupUi()

    def setupUi(self):
        self.resize(285, 455)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setWindowTitle("RNEL Elevator Controller")

        frame = QtGui.QFrame(self)
        formLayout_2 = QtGui.QFormLayout(self)
        formLayout_2.addRow(frame)

        btn_run = QtGui.QPushButton("Run", frame)
        btn_run.setMaximumSize(QtCore.QSize(162, 27))

        font = QtGui.QFont()
        font.setPointSize(11)
        label_instructions = QtGui.QLabel("Please visit the following site for instructions:", frame)
        label_instructions.setFont(font)

        label_website = QtGui.QLabel(frame)
        label_website.setFont(font)
        label_website.setText("<a href=\"https://github.com/kemerelab/Elevator/\">Elevator Maze</a>")
        label_website.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        label_website.setOpenExternalLinks(True)

        verticalLayout_5 = QtGui.QVBoxLayout()
        verticalLayout_5.addWidget(label_instructions)
        verticalLayout_5.addWidget(label_website)

        label_banner = QtGui.QLabel(frame)
        label_banner.setMaximumSize(QtCore.QSize(219, 102))
        label_banner.setText("")
        label_banner.setPixmap(QtGui.QPixmap(":/RNELicon/RNELBanner.png"))
        label_banner.setScaledContents(True)

        widget = QtGui.QWidget(frame)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)

        font.setPointSize(12)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        label_motorState = QtGui.QLabel("Stepper Motor Parameters", widget)
        label_motorState.setFont(font)

        formLayout_4 = QtGui.QFormLayout(widget)
        formLayout_4.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        formLayout_4.setMargin(0)
        formLayout_4.addItem(spacerItem)
        formLayout_4.addRow(label_motorState)

        label_speed = QtGui.QLabel("Speed:", widget)
        label_steps = QtGui.QLabel("Distance:", widget)
        label_direction = QtGui.QLabel("Direction:", widget)
        label_mode = QtGui.QLabel("Mode:", widget)

        verticalLayout = QtGui.QVBoxLayout()
        verticalLayout.addWidget(label_speed)
        verticalLayout.addWidget(label_steps)
        verticalLayout.addWidget(label_direction)
        verticalLayout.addWidget(label_mode)

        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.addLayout(verticalLayout)
        formLayout_4.setLayout(3, QtGui.QFormLayout.LabelRole, horizontalLayout)

        self.lineEdit_speed = QtGui.QLineEdit(widget)
        self.lineEdit_speed.setMaximumSize(QtCore.QSize(111, 27))
        self.lineEdit_speed.setText("0")
        self.lineEdit_distance = QtGui.QLineEdit(widget)
        self.lineEdit_distance.setMaximumSize(QtCore.QSize(111, 27))
        self.lineEdit_distance.setText("0")
        self.comboBox_direction = QtGui.QComboBox(widget)
        self.comboBox_direction.setMaximumSize(QtCore.QSize(111, 27))
        self.comboBox_direction.addItems(["Up", "Down"])
        self.comboBox_mode = QtGui.QComboBox(widget)
        self.comboBox_mode.setMaximumSize(QtCore.QSize(111, 27))
        self.comboBox_mode.addItems(["1/1", "1/2", "1/4", "1/8", "1/16", "1/32", "1/64", "1/128"])
        label_in = QtGui.QLabel("in.", widget)
        label_RPM = QtGui.QLabel("RPM", widget)

        formLayout_3 = QtGui.QFormLayout()
        formLayout_3.addRow(self.lineEdit_speed, label_RPM)
        formLayout_3.addRow(self.lineEdit_distance, label_in)
        formLayout_3.addRow(self.comboBox_direction)
        formLayout_3.addRow(self.comboBox_mode)
        horizontalLayout.addLayout(formLayout_3)

        gridLayout = QtGui.QGridLayout(frame)
        gridLayout.addWidget(label_banner, 0, 0, 1, 1)
        gridLayout.addWidget(widget, 1, 0, 1, 1, QtCore.Qt.AlignHCenter)
        gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        gridLayout.addWidget(btn_run, 3, 0, 1, 1, QtCore.Qt.AlignHCenter)
        gridLayout.addItem(spacerItem, 4, 0, 1, 1)
        gridLayout.addLayout(verticalLayout_5, 5, 0, 1, 1)

        btn_run.clicked.connect(self.sendMotorData)

    def sendMotorData(self):
        minHeight, maxHeight = 0, 200
        speed, speed_valid = QtCore.QString.toFloat(self.lineEdit_speed.text())
        distance, distance_valid = QtCore.QString.toFloat(self.lineEdit_distance.text())
        direction = self.comboBox_direction.currentText()

        invalid_box = QtGui.QMessageBox()
        invalid_box.setIcon(QtGui.QMessageBox.Warning)
        if speed_valid == False or distance_valid == False:
            invalid_box.setText("Invalid input(s).")
            invalid_box.setInformativeText("The motor will receive the default values of 0.")
            invalid_box.exec_()

        mode = self.comboBox_mode.currentText()[2:]
        while len(mode) < 3:
            mode = "0" + mode

        # RPMs of higher than 43 will result in skipped steps; set upper limit
        if speed > 43:
            speed = 0

        speed = str(int(speed))
        while len(speed) < 4:
            speed = "0" + speed

        # set limits depending on height of maze
        if direction == "Up":
            if distance > maxHeight - self.currentPosition:
                invalid_box.setText("Distance exceeds maze height.")
                invalid_box.setInformativeText("The elevator will move to the top of the maze.")
                invalid_box.exec_()
                distance = maxHeight - self.currentPosition
            self.currentPosition += distance
        if direction == "Down":
            if distance > self.currentPosition - minHeight:
                invalid_box.setText("Distance exceeds bottom of maze.")
                invalid_box.setInformativeText("The elevator will move to the bottom of the maze.")
                invalid_box.exec_()
                distance = self.currentPosition - minHeight
            self.currentPosition -= distance

        # steps_perInch depends on pulley diameter; using NEMA23 drive shaft diameter (6.35mm) for now
        steps_perInch = 254.647771437
        steps = distance * steps_perInch
        steps = str(int(steps))
        while len(steps) < 6:
            steps = "0" + steps

        data = 'x'+speed+'x'+steps+'x'+mode+'x'+direction

        arduino.write(str(data)) 
        print str(data)
        print "Distance: ", distance
        print "Current Position: ", self.currentPosition       

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = Ui_Form()
    ex.show()
    ex.raise_()
    sys.exit(app.exec_())
