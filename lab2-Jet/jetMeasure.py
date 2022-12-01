import jetFunctions as j
import time
import numpy as np
import spidev

spi = spidev.SpiDev()
j.initSpiAdc()

### КАЛИБРОВКА
isAway = -1

N = 500 # Кол-во точек для одной калибр. точки
if isAway == 0:
    P_away_data = []
    for i in range(N):
        P_away_data.append(j.getAdc())
    P_away_mn = np.mean(P_away_data)

    j.save(P_away_data, -1)
    print(P_away_mn)
elif isAway == 1:
    P_inside_data = []
    for i in range(N):
        P_inside_data.append(j.getAdc())
    P_inside_mn = np.mean(P_inside_data)

    j.save(P_inside_data, -1)
    print(P_inside_mn) 
    # P_away = j.getAdc()     # Давление вне струи (приблизительно нормальное атмосферное)
    # P_inside = j.getAdc()   # Давление в струе (измерено манометром)
else:
    j.initStepMotorGpio()

    data_90 = []
    for i in range(100):
        data_90.append(j.getAdc())
        j.stepForward(8)
        # j.stepBackward(8)
    j.save(data_90, 800)

j.deinitSpiAdc()
j.deinitStepMotorGpio()