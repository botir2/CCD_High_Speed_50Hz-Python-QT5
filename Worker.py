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
from Worker import *
import configs
################################################################################
#
#       Connect Button Worker thread Function calculation
#
class Worker(QThread):
    def __init__(self, sec=0, parent=None):
        super().__init__()
        self.main = parent
        self.working = True
        self.sec = sec

    def __del__(self):
        print(".... end thread.....")
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
        t_num = 7296
        P_num = int(t_num / 2)
        Lower_limit_value = 0
        upper_limit_value = 21
        rxData8 = np.zeros(t_num, np.uint8)
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
