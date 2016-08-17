import sys
import RNELBanner_rc
from PyQt4 import QtCore, QtGui
from serial import *

try:
    arduino = Serial('/dev/cu.usbmodem1411', 9600)
except:
    pass

class Ui_Form(QtGui.QWidget):
    def __init__(self):
        super(Ui_Form, self).__init__()
        self.currentPosition = 0
        self.level_position = {1:0, 2:1000, 3:2000}
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("RNEL Servo Controller")
        rowSpacer = QtGui.QSpacerItem(1, 20)
        columnSpacer = QtGui.QSpacerItem(40, 1)

        # Highlight input that is currently selected
        self.setFocusPolicy(QtCore.Qt.ClickFocus)

        # Create UI elements
        label_banner = QtGui.QLabel()
        label_banner.setText("")
        label_banner.setPixmap(QtGui.QPixmap(":/RNELicon/RNELBanner.png"))

        font = QtGui.QFont("Helvetica", 12, 75)
        font.setBold(True)
        label_motorState = QtGui.QLabel("Servo Motor Parameters")
        label_motorState.setFont(font)

        font = QtGui.QFont("Helvetica", 9, 75)
        door1_checkbox = QtGui.QCheckBox("Door 1 (Servos A/B)")
        door2_checkbox = QtGui.QCheckBox("Door 2 (Servos C/D)")
        door3_checkbox = QtGui.QCheckBox("Door 3 (Servos E/F)")
        door4_checkbox = QtGui.QCheckBox("Door 4 (Servos G/H)")
        door5_checkbox = QtGui.QCheckBox("Door 5 (Servos I/J)")
        door6_checkbox = QtGui.QCheckBox("Door 6 (Servos K/L)")
        door7_checkbox = QtGui.QCheckBox("Door 7 (Servos M/N)")
        door8_checkbox = QtGui.QCheckBox("Door 8 (Servos O/P)")
        self.checkbox_dict = {0: door1_checkbox, 1: door2_checkbox, 2: door3_checkbox, 3: door4_checkbox, 4: door5_checkbox, 5: door6_checkbox, 6: door7_checkbox, 7: door8_checkbox}

        door1_status = QtGui.QLabel("Degrees: 0")
        door2_status = QtGui.QLabel("Degrees: 0")
        door3_status = QtGui.QLabel("Degrees: 0")
        door4_status = QtGui.QLabel("Degrees: 0")
        door5_status = QtGui.QLabel("Degrees: 0")
        door6_status = QtGui.QLabel("Degrees: 0")
        door7_status = QtGui.QLabel("Degrees: 0")
        door8_status = QtGui.QLabel("Degrees: 0")
        self.status_dict = {0: door1_status, 1: door2_status, 2: door3_status, 3: door4_status, 4: door5_status, 5: door6_status, 6: door7_status, 7: door8_status}

        label_degree = QtGui.QLabel("Degrees (0-90):")
        self.lineEdit_degree = QtGui.QLineEdit()
        self.lineEdit_degree.setMaximumSize(QtCore.QSize(100, 30))
        self.lineEdit_degree.setText("0")

        btn_open = QtGui.QPushButton("Open")
        btn_close = QtGui.QPushButton("Close")
        btn_run = QtGui.QPushButton("Run")

        # Format UI elements
        formLayout = QtGui.QFormLayout()
        formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        formLayout.setLabelAlignment(QtCore.Qt.AlignLeft)
        formLayout.addRow(label_degree, self.lineEdit_degree)

        verticalLayout = QtGui.QVBoxLayout()
        for i in range(8):
            verticalLayout.addWidget(self.checkbox_dict[i])

        verticalLayout2 = QtGui.QVBoxLayout()
        for i in range(8):
            verticalLayout2.addWidget(self.status_dict[i])

        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.addLayout(verticalLayout)
        horizontalLayout.addSpacerItem(columnSpacer)
        horizontalLayout.addLayout(verticalLayout2)

        horizontalLayout2 = QtGui.QHBoxLayout()
        horizontalLayout2.addWidget(btn_open)
        horizontalLayout2.addWidget(btn_close)

        horizontalLayout3 = QtGui.QHBoxLayout()
        horizontalLayout3.addLayout(formLayout)
        horizontalLayout3.addWidget(btn_run)

        verticalLayout3 = QtGui.QVBoxLayout(self)
        verticalLayout3.setContentsMargins(30, 20, 30, 20)
        verticalLayout3.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        verticalLayout3.addWidget(label_banner, 0, QtCore.Qt.AlignHCenter)
        verticalLayout3.addSpacerItem(rowSpacer)
        verticalLayout3.addWidget(label_motorState)
        verticalLayout3.addLayout(horizontalLayout)
        verticalLayout3.addLayout(horizontalLayout2)
        verticalLayout3.addLayout(horizontalLayout3)

        btn_open.clicked.connect(self.door_open)
        btn_close.clicked.connect(self.door_close)
        btn_run.clicked.connect(self.door_degrees)

    def door_open(self):
        self.sendMotorData("20")

    def door_close(self):
        self.sendMotorData("70")

    def door_degrees(self):
        degrees, degrees_valid = QtCore.QString.toFloat(self.lineEdit_degree.text())
        degrees = int(degrees)

        if degrees > 90 or degrees < 0 or degrees_valid == False:
            return
        self.sendMotorData(str(degrees))

    def sendMotorData(self, degrees):
        data = ""
        for i in range(8):
            if self.checkbox_dict[i].checkState() == 2:
                self.status_dict[i].setText("Degrees: " + degrees)
            data += str(self.checkbox_dict[i].checkState())

        while len(degrees) < 3:
            degrees = "0" + degrees
        data += "x" + degrees

        try:
            arduino.write(data)
        except:
            pass

        print data

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = Ui_Form()
    ex.show()
    ex.raise_()
    sys.exit(app.exec_())