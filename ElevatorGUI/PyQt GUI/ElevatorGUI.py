# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ElevatorController.ui'
#
# Created: Fri Jun  5 10:36:55 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import sys
from serial import *

arduino = Serial('/dev/ttyACM1', 115200)

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)

    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(271, 427)
        Form.setMouseTracking(False)
        Form.setFocusPolicy(QtCore.Qt.NoFocus)
        self.formLayout_2 = QtGui.QFormLayout(Form)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.frame = QtGui.QFrame(Form)
        self.frame.setFrameShape(QtGui.QFrame.Panel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout = QtGui.QGridLayout(self.frame)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.btn_run = QtGui.QPushButton(self.frame)
        self.btn_run.setMaximumSize(QtCore.QSize(162, 27))
        self.btn_run.setObjectName(_fromUtf8("btn_run"))
        self.gridLayout.addWidget(self.btn_run, 3, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.label_instructions = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_instructions.setFont(font)
        self.label_instructions.setObjectName(_fromUtf8("label_instructions"))
        self.verticalLayout_5.addWidget(self.label_instructions)
        self.label_website = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_website.setFont(font)
        self.label_website.setMouseTracking(True)
        self.label_website.setOpenExternalLinks(True)
        self.label_website.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.label_website.setObjectName(_fromUtf8("label_website"))
        self.verticalLayout_5.addWidget(self.label_website)
        self.gridLayout.addLayout(self.verticalLayout_5, 5, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 4, 0, 1, 1)
        self.label_banner = QtGui.QLabel(self.frame)
        self.label_banner.setMaximumSize(QtCore.QSize(219, 102))
        self.label_banner.setText(_fromUtf8(""))
        self.label_banner.setPixmap(QtGui.QPixmap(_fromUtf8(":/RNELicon/RNELBanner.png")))
        self.label_banner.setScaledContents(True)
        self.label_banner.setObjectName(_fromUtf8("label_banner"))
        self.gridLayout.addWidget(self.label_banner, 0, 0, 1, 1)
        self.widget = QtGui.QWidget(self.frame)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.formLayout_4 = QtGui.QFormLayout(self.widget)
        self.formLayout_4.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_4.setMargin(0)
        self.formLayout_4.setObjectName(_fromUtf8("formLayout_4"))
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.formLayout_4.setItem(1, QtGui.QFormLayout.LabelRole, spacerItem2)
        self.label_motorState = QtGui.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.label_motorState.setFont(font)
        self.label_motorState.setObjectName(_fromUtf8("label_motorState"))
        self.formLayout_4.setWidget(2, QtGui.QFormLayout.SpanningRole, self.label_motorState)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_speed = QtGui.QLabel(self.widget)
        self.label_speed.setObjectName(_fromUtf8("label_speed"))
        self.verticalLayout.addWidget(self.label_speed)
        self.label_steps = QtGui.QLabel(self.widget)
        self.label_steps.setObjectName(_fromUtf8("label_steps"))
        self.verticalLayout.addWidget(self.label_steps)
        self.label_direction = QtGui.QLabel(self.widget)
        self.label_direction.setObjectName(_fromUtf8("label_direction"))
        self.verticalLayout.addWidget(self.label_direction)
        self.label_mode = QtGui.QLabel(self.widget)
        self.label_mode.setObjectName(_fromUtf8("label_mode"))
        self.verticalLayout.addWidget(self.label_mode)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.formLayout_3 = QtGui.QFormLayout()
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.lineEdit_speed = QtGui.QLineEdit(self.widget)
        self.lineEdit_speed.setMaximumSize(QtCore.QSize(111, 27))
        self.lineEdit_speed.setPlaceholderText(_fromUtf8(""))
        self.lineEdit_speed.setObjectName(_fromUtf8("lineEdit_speed"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.lineEdit_speed)
        self.lineEdit_steps = QtGui.QLineEdit(self.widget)
        self.lineEdit_steps.setMaximumSize(QtCore.QSize(111, 27))
        self.lineEdit_steps.setObjectName(_fromUtf8("lineEdit_steps"))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.LabelRole, self.lineEdit_steps)
        self.comboBox_direction = QtGui.QComboBox(self.widget)
        self.comboBox_direction.setMaximumSize(QtCore.QSize(111, 27))
        self.comboBox_direction.setObjectName(_fromUtf8("comboBox_direction"))
        self.comboBox_direction.addItem(_fromUtf8(""))
        self.comboBox_direction.addItem(_fromUtf8(""))
        self.formLayout_3.setWidget(3, QtGui.QFormLayout.SpanningRole, self.comboBox_direction)
        self.comboBox_mode = QtGui.QComboBox(self.widget)
        self.comboBox_mode.setMaximumSize(QtCore.QSize(111, 27))
        self.comboBox_mode.setObjectName(_fromUtf8("comboBox_mode"))
        self.comboBox_mode.addItem(_fromUtf8(""))
        self.comboBox_mode.addItem(_fromUtf8(""))
        self.comboBox_mode.addItem(_fromUtf8(""))
        self.comboBox_mode.addItem(_fromUtf8(""))
        self.formLayout_3.setWidget(4, QtGui.QFormLayout.SpanningRole, self.comboBox_mode)
        self.horizontalLayout.addLayout(self.formLayout_3)
        self.formLayout_4.setLayout(3, QtGui.QFormLayout.LabelRole, self.horizontalLayout)
        self.gridLayout.addWidget(self.widget, 1, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.SpanningRole, self.frame)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "RNEL Elevator Controller", None))
        self.btn_run.setText(_translate("Form", "Run", None))
        self.label_instructions.setText(_translate("Form", "Please visit the following site for instructions :", None))
        self.label_website.setText(_translate("Form", "http://www.fakewebsite.com", None))
        self.label_motorState.setText(_translate("Form", "    Stepper Motor State", None))
        self.label_speed.setText(_translate("Form", "Speed:", None))
        self.label_steps.setText(_translate("Form", "Steps:", None))
        self.label_direction.setText(_translate("Form", "Direction:", None))
        self.label_mode.setText(_translate("Form", "Mode:", None))
        self.lineEdit_speed.setText(_translate("Form", "100", None))
        self.lineEdit_steps.setText(_translate("Form", "200", None))
        self.comboBox_direction.setItemText(0, _translate("Form", "Forward", None))
        self.comboBox_direction.setItemText(1, _translate("Form", "Backward", None))
        self.comboBox_mode.setItemText(0, _translate("Form", "Double", None))
        self.comboBox_mode.setItemText(1, _translate("Form", "Single", None))
        self.comboBox_mode.setItemText(2, _translate("Form", "Microstep", None))
        self.comboBox_mode.setItemText(3, _translate("Form", "Interleave", None))
        self.btn_run.clicked.connect(self.sendMotorData)

    def sendMotorData(self):
        speed_string = "0123"
        steps_string = "0123"
        direction_string = "Y"
        mode_string = "Z"
        data = ""

        speed = self.lineEdit_speed.text()
        steps = self.lineEdit_steps.text()
        direction = self.comboBox_direction.currentText()[0]
        mode = self.comboBox_mode.currentText()[0]

        if len(speed) == 1:
            speed_string = speed_string.replace('3', speed, 1)
            speed_string = speed_string.replace('12', '00', 1)
        elif len(speed) == 2:
            speed_string = speed_string.replace('23', speed, 1)
            speed_string = speed_string.replace('1', '0', 1)
        elif len(speed) == 3:
            speed_string = speed_string.replace('123', speed, 1)
        elif len(speed) == 4:
            speed_string = speed_string.replace('0123', speed, 1)

        if len(steps) == 1:
            steps_string = steps_string.replace('3', steps, 1)
            steps_string = steps_string.replace('12', '00', 1)
        elif len(steps) == 2:
            steps_string = steps_string.replace('23', steps, 1)
            steps_string = steps_string.replace('1', '0', 1)
        elif len(steps) == 3:
            steps_string = steps_string.replace('123', steps, 1)
        elif len(steps) == 4:
            steps_string = steps_string.replace('0123', steps, 1)


        direction_string = direction_string.replace('Y', direction[0], 1)
        mode_string = mode_string.replace('Z', mode[0], 1)

        data = 'x'+speed_string+'x'+steps_string+'x'+direction_string+'x'+mode_string 

        arduino.write(str(data)) 
        print str(data)

import RNELBanner_rc

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = Ui_Form()
    ex.show()
    sys.exit(app.exec_())