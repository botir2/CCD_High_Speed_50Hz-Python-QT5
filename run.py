
#python imports
from pyqtgraph.Qt import QtGui, QtCore
from PyQt5.QtCore import *
import numpy as np
import pandas as pd
import pyqtgraph as pg
import sys
import serial
import scipy
import time
from scipy import signal

#application imports
from GuiWidget import *
from Parameters import *
import configs

#
################################################################################
#
#    thread class call Connection COM (configs.port)
#
def Connection(serial_port, COM):
    try:
        serial_port = serial.Serial(COM, configs.baudrate, timeout=None)
        print(configs.port, 'connected')
    except serial.SerialException:
        print('SerialException')

    if not serial_port:
        raise serial.SerialException('not found, but tried hard.')
        print("reconnct")
    return serial_port

#
################################################################################
#
#    filter functions
#
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='lowpass', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = signal.lfilter(b, a, data)
    return y

def moving_average(data_set, periods=3):
    weights = np.ones(periods) / periods
    return np.convolve(data_set, weights, mode='valid')


class MainWindow(QtGui.QMainWindow):
    recive_update_singal = pyqtSignal("PyQt_PyObject")
    recive_start_singal = pyqtSignal("PyQt_PyObject")
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setFixedSize(1600, 700)
        global curve, curve1, curve2
        curve = np.uint8()
        curve1 = np.uint8()
        curve2 = np.uint8()
        self.setWindowTitle('CCD_High_Speed_50Hz')
        self.central_widget = QtGui.QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.login_widget = GuiWidget(self)

        self.login_widget.label_image.setPixmap(QtGui.QPixmap("smartcs.png"))

        self.th = Worker(parent=self)

        #
        ################################################################################
        #
        #    Show GuiWidget graph
        #
        curve = self.login_widget.plot1.plot(pen='y')

        curve1 = self.login_widget.plot2.plot(pen='y')

        curve2 = self.login_widget.plot3.plot(pen='r')

        self.login_widget.Connect.clicked.connect(self.pushButtonClicked_Acc_to_Con)
        self.login_widget.Update.clicked.connect(self.updateBtn) # call update button
        self.login_widget.StopBtn.clicked.connect(self.STOP)  # call update button
        self.recive_start_singal.connect(self.th.recive_start_singal)
        self.recive_update_singal.connect(self.th.recive_update_singal)
        self.central_widget.addWidget(self.login_widget)

    def plotter(self):
        self.data = [0]
        self.curve = self.login_widget.plot1.getPlotItem().plot()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updater)
        self.timer1.start(.01)
    #
    ################################################################################
    #
    #       Connect Button thread Function
    #
    @pyqtSlot()
    def pushButtonClicked_Acc_to_Con(self):
        parBtn = Parameters()
        parBtn.LowLImVal = self.login_widget.lineEdit_Lower_limit_value.value()
        parBtn.UpLImVal = self.login_widget.lineEdit_Upper_limit_value.value()
        parBtn.COM = self.login_widget.lineEdit_Com_device.text()
        self.recive_start_singal.emit(parBtn)
        time.sleep(1)
        self.th.start()
        self.th.working = True


    #
    ################################################################################
    #
    #       Update Button Function
    #
    @pyqtSlot()
    def updateBtn(self): #call update button function
        parUpt = Parameters()
        parUpt.LowLImVal = self.login_widget.lineEdit_Lower_limit_value.value()
        parUpt.UpLImVal = self.login_widget.lineEdit_Upper_limit_value.value()
        self.recive_update_singal.emit(parUpt)


    @pyqtSlot()
    def STOP(self):  # call STOP button function
        self.th.working = False

################################################################################
#
#       Connect Button Worker thread Function calculation
#

class Worker(QThread):
    def __init__(self, sec = 0, parent=None):
        super().__init__()
        self.main = parent
        self.working = True
        self.sec = sec

    def __del__(self):
        print("..! End thread !..")
        self.wait()

    @pyqtSlot("PyQt_PyObject")
    def recive_start_singal(self, inst):
        self.par_LowLImVal = inst.LowLImVal or 0
        self.par_UpLImVal = inst.UpLImVal or 21
        self.COM = inst.COM
        print("Start")
        print(self.par_LowLImVal)
        print(self.par_UpLImVal)


    @pyqtSlot("PyQt_PyObject")
    def recive_update_singal(self, update):
        self.par_LowLImVal = update.LowLImVal or 0
        self.par_UpLImVal = update.UpLImVal or 21
        print("Update...")
        print(self.par_LowLImVal)
        print(self.par_UpLImVal)

    def run(self):
        global naparrays, rawData, pltData, t_num, P_num
        self.serial_port = False
        try:
            self.serial_port = serial.Serial(self.COM, configs.baudrate, timeout=None)
            print(configs.port, 'connected')
        except serial.SerialException:
            print('SerialException')
        if not self.serial_port:
            raise serial.SerialException('not found, but tried hard.')
            print("reconnct")
        self.serial_port.write(str.encode("#CSDTP:1%"))
        # self.serial_port.write(str.encode("#CCDInt:%d%d%d%%")) #default integration time
        # self.serial_port.write(str.encode("#CCDInt:005%005")) #integration time set is 5
        t_num = 7296
        P_num = int(t_num / 2)
        np.zeros(t_num, np.uint8)
        pltData16 = np.zeros(P_num, np.uint8)
        pltData = np.zeros(P_num)
        Pixel_plot = np.zeros(500)
        while self.working:
            rxData8 = self.serial_port.read(t_num)  # 8332
            for rxi in range(P_num):  # 3648
                pltData16[rxi] = (rxData8[2 * rxi + 1] << 8) + rxData8[2 * rxi]
            rawData = pltData16
            max_pixel_num = np.where(pltData16 == pltData16.max())
            for j in range(0, len(max_pixel_num[0])):
                pltData16[max_pixel_num[0][j]] = 0
            pltData = butter_lowpass_filter(pltData16, 0.1, 10, order=5)
            for i in range(0, len(pltData)):
                if pltData[i] < self.par_LowLImVal:
                    pltData[i] = 0
                if pltData[i] > self.par_UpLImVal:
                    pltData[i] = self.par_UpLImVal

            max_pixel_num = np.where(pltData == pltData.max())
            Pixel_plot[-1] = max_pixel_num[0][0]
            naparrays = Pixel_plot / 100.0
            Pixel_plot = np.roll(Pixel_plot, -1, axis=0)
            curve.setData(rawData)
            curve1.setData(pltData)
            curve2.setData(naparrays)
        self.serial_port.close()

#
################################################################################
#
#      Background image set url
#
stylesheet = """
    MainWindow {
        background-image: url("C:/Users/ceo/Desktop/CCD_High_Speed_50Hz/pcb.jpg");
        background-repeat: no-repeat; 
        background-position: center;
    }
"""

if __name__ == '__main__':
    app = QtGui.QApplication([])
    app.setStyleSheet(stylesheet)  #
    window = MainWindow()
    window.show()
    app.exec_()

