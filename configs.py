import numpy as np


#serial definitions
lowLimVal = 0
port = 'COM3'
baudrate = 115200
#parametres
t_Num = 7296
t_Num_max  = 7500
lowLimVal = 0
upperLimVal = 21

#Data as the program handles
SHperiod = np.uint32(20)
ICGperiod = np.uint32(500000)
AVGn = np.uint8([0,1])

#Data arrays for received bytes
rxData8 = np.zeros(7388, np.uint8)
rxData16 = np.zeros(3694, np.uint16)
pltData16 = np.zeros(3648, np.uint8)
rxData128 = np.zeros(7388, np.uint32)

globals()
rxDataVC = np.zeros(4096, np.uint16)

#Arrays for data to transmit
txsh = np.uint8([0,0,0,0]) 
txicg = np.uint8([0,0,0,0])
