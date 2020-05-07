from pyqtgraph.Qt import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import  QDial
import pyqtgraph as pg
import configs

class GuiWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(GuiWidget, self).__init__(parent = parent)
        layoutV1 = QtGui.QVBoxLayout()

        self.setWindowTitle('CCD_High_Speed_50Hz')

        #
        ################################################################################
        #
        #    Show input text function
        #
        self.label_Com_device = QtGui.QLabel('COM-device')
        self.label_Com_device.setStyleSheet('color: red')
        self.label_Com_device.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Black))
        self.lineEdit_Com_device = QtGui.QLineEdit(configs.port)

        #self.Spin
        self.Connect = QtGui.QPushButton('CONNECT')
        #self.Connect.setStyleSheet('''border-image:url("C:/Users/ceo/Desktop/CCD_High_Speed_50Hz/COM.jpg");''')
        #self.button = QPushButton("Start Progressbar")
        self.Connect.setStyleSheet("background-color:rgb(192,192,192)")

        self.label_start_time = QtGui.QLabel('T num: min 7296 <=======> 7500 max')
        self.label_start_time.setStyleSheet('color: red')
        self.label_start_time.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Black))

        self.lineEdit_Com_device = QtGui.QLineEdit(configs.port)

        #self.lineEdit_Start_time = QtGui.QLineEdit(str(configs.t_Num))
        self.lineEdit_Start_time = QtGui.QSlider(Qt.Horizontal)
        self.lineEdit_Start_time.setMinimum(int(configs.t_Num)) # value is 7296
        self.lineEdit_Start_time.setMaximum(int(configs.t_Num_max)) # value max is  7500
        self.lineEdit_Start_time.setValue(10)
        self.lineEdit_Start_time.setTickPosition(QtGui.QSlider.TicksBelow)
        self.lineEdit_Start_time.setTickInterval(0.05)

        self.label_Lower_limit_value = QtGui.QLabel('Lower limit value is from: 0')
        self.label_Lower_limit_value.setStyleSheet('color: red')
        self.label_Lower_limit_value.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Black))

        self.lineEdit_Lower_limit_value = QtGui.QSlider(Qt.Horizontal)
        self.lineEdit_Lower_limit_value.setMinimum(int(configs.lowLimVal))  # value is 0
        self.lineEdit_Lower_limit_value.setMaximum(int(configs.upperLimVal))  # value max is  21
        self.lineEdit_Lower_limit_value.setValue(0)
        self.lineEdit_Lower_limit_value.setTickPosition(QtGui.QSlider.TicksBelow)
        self.lineEdit_Lower_limit_value.setTickInterval(0.05)

        self.label_Upper_limit_value = QtGui.QLabel('Upper limit value is from: 21')
        self.label_Upper_limit_value.setStyleSheet('color: red')
        self.label_Upper_limit_value.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Black))
        #self.lineEdit_Upper_limit_value = QtGui.QLineEdit(str(configs.upperLimVal))
        self.lineEdit_Upper_limit_value = QtGui.QSlider(Qt.Horizontal)
        self.lineEdit_Upper_limit_value.setMinimum(int(configs.upperLimVal))  # value is 21
        self.lineEdit_Upper_limit_value.setMaximum(31)
        self.lineEdit_Upper_limit_value.setValue(0)
        self.lineEdit_Upper_limit_value.setTickPosition(QtGui.QSlider.TicksBelow)
        self.lineEdit_Upper_limit_value.setTickInterval(0.05)


        ############################# Qdial #################################
        self.label = QtGui.QLabel(self)
        self.label.setFont(QtGui.QFont("Sanserif", 15))
        self.dial = QDial()
        self.dial.setMaximum(0)
        self.dial.setMaximum(100)
        self.dial.setValue(30)
        self.dial.setWrapping(True)
        self.dial.valueChanged.connect(self.dialer_changed)

        self.Update = QtGui.QPushButton('Update')
        self.Update.setStyleSheet("background-color:rgb(255,255,153)")

        self.StopBtn = QtGui.QPushButton('STOP')
        self.StopBtn.setStyleSheet("background-color:rgb(255,0,0)")
        #self.button_save = QtGui.QPushButton('SAVE to CSV')

        self.label_image = QtGui.QLabel()

        layoutV1.addSpacing(40)
        layoutV1.addWidget(self.label_Com_device)
        layoutV1.addWidget(self.lineEdit_Com_device)
        layoutV1.addSpacing(10)
        layoutV1.addWidget(self.Connect)
        layoutV1.addSpacing(30)
        layoutV1.addWidget(self.label_start_time)
        layoutV1.addWidget(self.lineEdit_Start_time)
        layoutV1.addSpacing(10)

        layoutV1.addWidget(self.label_Lower_limit_value)
        layoutV1.addWidget(self.lineEdit_Lower_limit_value)
        layoutV1.addSpacing(10)

        layoutV1.addWidget(self.label_Upper_limit_value)
        layoutV1.addWidget(self.lineEdit_Upper_limit_value)
        layoutV1.addSpacing(50)
        layoutV1.addWidget(self.dial)
        layoutV1.addWidget(self.label)
        layoutV1.addSpacing(20)
        layoutV1.addWidget(self.Update)
        layoutV1.addWidget(self.StopBtn)
        layoutV1.addSpacing(30)

        layoutV1.addSpacing(100)
        layoutV1.addWidget(self.label_image)
        layoutV1.addStretch(10)

        #
        ################################################################################
        #
        #   Graph Show function
        #

        layoutH2 = QtGui.QHBoxLayout()
        self.plot1 = pg.PlotWidget(title="CCD 50Hz plot")
        self.plot2 = pg.PlotWidget(title="CCD 50Hz_filter plot")
        self.plot3 = pg.PlotWidget(title="CCD 50Hz Pixel plot")

        #self.plot4 = pg.GraphicsWindow(title="Basic plotting examples")
        #self.plot4.setWindowTitle

        layoutH2.addWidget(self.plot1)
        layoutH2.addWidget(self.plot2)
        layoutH2.addWidget(self.plot3)

        #layoutH3 = QtGui.QHBoxLayout()
        #self.plot4 = pg.PlotWidget(title="Time_Data filtered Frequency Weighting")
        #self.plot5 = pg.PlotWidget(title="Equal Sensation Curves of Vertical Whole-Body Vibration(Comfort limit)")
        #self.plot6 = pg.PlotWidget(title="VDV curve according to vibration duration")
        #layoutH3.addWidget(self.plot4)
        #layoutH3.addWidget(self.plot5)
        #layoutH3.addWidget(self.plot6)

        layoutV2 = QtGui.QVBoxLayout()
        layoutV2.addLayout(layoutH2)
        #layoutV2.addLayout(layoutH3)

        layout = QtGui.QHBoxLayout()
        layout.addLayout(layoutV1)
        layout.addLayout(layoutV2)

        layout.setStretchFactor(layoutV1, 0)
        ################### graph layout #################
        layout.setStretchFactor(layoutV2, 1)
        self.setLayout(layout)

    def dialer_changed(self):
        getValue = self.dial.value()
        self.label.setText(" Dialer Value : " + str(getValue))