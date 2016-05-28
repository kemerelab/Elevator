# Refer to the following link for PyQt documentation
# http://pyqt.sourceforge.net/Docs/PyQt4/classes.html

import sys
import RNELBanner_rc
from PyQt4 import QtCore, QtGui
from serial import *

#arduino = Serial('/dev/cu.usbmodem1411', 115200)

class Ui_Form(QtGui.QWidget):
    def __init__(self):
        super(Ui_Form, self).__init__()
        self.currentPosition = 0
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("RNEL Elevator Controller")
        spacerItem = QtGui.QSpacerItem(1, 20)

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
        label_motorState.setIndent(26)

        label_speed = QtGui.QLabel("Speed (RPM):")
        label_steps = QtGui.QLabel("Distance (inches):")
        label_direction = QtGui.QLabel("Direction:")
        label_mode = QtGui.QLabel("Mode:")

        self.lineEdit_speed = QtGui.QLineEdit()
        self.lineEdit_speed.setMaximumSize(QtCore.QSize(111, 27))
        self.lineEdit_speed.setText("0")
        self.lineEdit_distance = QtGui.QLineEdit()
        self.lineEdit_distance.setMaximumSize(QtCore.QSize(111, 27))
        self.lineEdit_distance.setText("0")
        self.comboBox_direction = QtGui.QComboBox()
        self.comboBox_direction.setMaximumSize(QtCore.QSize(111, 27))
        self.comboBox_direction.addItems(["Up", "Down"])
        self.comboBox_mode = QtGui.QComboBox()
        self.comboBox_mode.setMaximumSize(QtCore.QSize(111, 27))
        self.comboBox_mode.addItems(["1/1", "1/2", "1/4", "1/8", "1/16", "1/32", "1/64", "1/128"])

        btn_run = QtGui.QPushButton("Run")
        btn_run.setMaximumSize(QtCore.QSize(50, 30))

        font = QtGui.QFont("Helvetica", 11)
        label_instructions = QtGui.QLabel("Please visit the following site for instructions:")
        label_instructions.setFont(font)

        label_website = QtGui.QLabel()
        label_website.setFont(font)
        label_website.setText("<a href=\"https://github.com/kemerelab/Elevator/\">Elevator Maze</a>")
        label_website.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        label_website.setOpenExternalLinks(True)

        formLayout = QtGui.QFormLayout()
        formLayout.setLabelAlignment(QtCore.Qt.AlignLeft)
        formLayout.addRow(label_speed, self.lineEdit_speed)
        formLayout.addRow(label_steps, self.lineEdit_distance)
        formLayout.addRow(label_direction, self.comboBox_direction)
        formLayout.addRow(label_mode, self.comboBox_mode)

        # Format UI elements
        verticalLayout = QtGui.QVBoxLayout(self)
        verticalLayout.setContentsMargins(30, 20, 30, 20)
        verticalLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        verticalLayout.addWidget(label_banner)
        verticalLayout.addSpacerItem(spacerItem)
        verticalLayout.addWidget(label_motorState)
        verticalLayout.addLayout(formLayout)
        verticalLayout.setAlignment(formLayout, QtCore.Qt.AlignLeft)
        verticalLayout.addWidget(btn_run)
        verticalLayout.setAlignment(btn_run, QtCore.Qt.AlignHCenter)
        verticalLayout.addSpacerItem(spacerItem)
        verticalLayout.addWidget(label_instructions)
        verticalLayout.addWidget(label_website)

        btn_run.clicked.connect(self.sendMotorData)

    def sendMotorData(self):
        minHeight, maxHeight = 0, 200
        speed, speed_valid = QtCore.QString.toFloat(self.lineEdit_speed.text())
        distance, distance_valid = QtCore.QString.toFloat(self.lineEdit_distance.text())
        direction = self.comboBox_direction.currentText()

        # Display error message for invalid inputs
        invalid_box = QtGui.QMessageBox()
        invalid_box.setIcon(QtGui.QMessageBox.Warning)
        if speed_valid == False or distance_valid == False:
            invalid_box.setText("<br>Invalid input(s).")
            invalid_box.setInformativeText("<big>Inputs must be numbers.")
            invalid_box.exec_()

        mode = self.comboBox_mode.currentText()[2:]
        while len(mode) < 3:
            mode = "0" + mode

        # Warn user if speed has not been set
        if speed == 0 and speed_valid == True:
            invalid_box.setText("<br>The speed has not been set.")
            invalid_box.setInformativeText("<big>Please set a speed to start the motor.")
            invalid_box.exec_()

        # RPMs of higher than 43 will result in skipped steps; set upper limit
        if speed > 43:
            invalid_box.setText("<br>Maximum RPM exceeded.")
            invalid_box.setInformativeText("<big>Please use a speed no greater than 43 RPM to avoid skipped steps.")
            invalid_box.exec_()
            speed = 0

        # set limits depending on height of maze
        if direction == "Up" and speed != 0:
            if distance > maxHeight - self.currentPosition:
                invalid_box.setText("<br>Distance exceeds maze height.")
                invalid_box.setInformativeText("<big>The elevator will stop at the top of the maze.")
                invalid_box.exec_()
                distance = maxHeight - self.currentPosition
            self.currentPosition += distance
        if direction == "Down" and speed != 0:
            if distance > self.currentPosition - minHeight:
                invalid_box.setText("<br>Distance exceeds bottom of maze.")
                invalid_box.setInformativeText("<big>The elevator will stop at the bottom of the maze.")
                invalid_box.exec_()
                distance = self.currentPosition - minHeight
            self.currentPosition -= distance

        speed = str(int(speed))
        while len(speed) < 4:
            speed = "0" + speed

        # steps_perInch depends on pulley diameter; using NEMA23 drive shaft diameter (6.35mm) for now
        steps_perInch = 254.647771437
        steps = distance * steps_perInch
        steps = str(int(steps))
        while len(steps) < 6:
            steps = "0" + steps

        data = 'x'+speed+'x'+steps+'x'+mode+'x'+direction

        #arduino.write(str(data)) 
        print str(data)
        print "Distance: ", distance
        print "Current Position: ", self.currentPosition       

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = Ui_Form()
    ex.show()
    ex.raise_()
    sys.exit(app.exec_())
