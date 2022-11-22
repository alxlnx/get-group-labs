#!/usr/bin/python3
import numpy as np
import lightFunctions as liFu
import matplotlib.pyplot as plt

photoNames =  [ "lab3-Albedo/mercury_white_(1)",
                "lab3-Albedo/filament_blue_11",
                "lab3-Albedo/filament_green_11",
                "lab3-Albedo/filament_red_11",
                "lab3-Albedo/filament_white_11",
                "lab3-Albedo/filament_yellow_11" ]

### Считывание интенсивностей и сохранение графиков ###
intensities = []
for name in photoNames:
    begin_idx = name.find('/')
    lamp_end_idx = name.find('_', begin_idx)
    color_end_idx = name.find('_', lamp_end_idx + 1)
    lamp_type = name[begin_idx + 1:lamp_end_idx]
    color_type = name[lamp_end_idx + 1:color_end_idx]

    inten = liFu.readIntensity(f'{name}.png', f"{name}_G.png", f"{lamp_type}", f"{color_type}")
    intensities.append(inten)

### Калибровка ###
# Пусть длина волны λ задаётся формулой λ(n) = k * n + b, где n - номер столбца пикселей.
# Тогда коэффиценты k и b можно определить по трём точкам методом наименьших квадратов.
# Если же точек всего две, то следует решить систему линейных уравнений на k и b.
###
luma_mercury = intensities[0]

red_max_pixel   = 130
green_max_pixel = 180
blue_max_pixel  = 245
red_λ   = 578.2    # нм
green_λ = 546.0735 # нм
blue_λ  = 435.8328 # нм

ys = [red_λ, green_λ, blue_λ]
xs = [red_max_pixel, green_max_pixel, blue_max_pixel]
(k, b) = np.polyfit(xs, ys, 1)

with open("calibration.txt", 'w') as outfile:
    payload = f'λ(n) = {k:.3f}*n + {b:.3f}\n' +\
              'Точность: три знака после запятой.\n'
    outfile.write(payload)

### Построение графиков зависимости "яркости" от λ ###
λs = []
for px in range(len(luma_mercury)):
    λ = k * px + b
    λs.append(λ)


fig, ax = plt.subplots( figsize=(10, 5), dpi=200 )
ax.set_facecolor('grey')
ax.set_title('Отражённая интенсивность излучения лампы накаливания')
ax.set_xlabel('Длина волны, [нм]')
ax.set_ylabel('Яркость')

luma_blue   = intensities[1]
luma_green  = intensities[2]
luma_red    = intensities[3]
luma_white  = intensities[4]
luma_yellow = intensities[5]


ax.plot(λs, luma_blue,   color='blue',   label='Синий лист')
ax.plot(λs, luma_green,  color='green',  label='Зелёный лист')
ax.plot(λs, luma_red,    color='red',    label='Красный лист')
ax.plot(λs, luma_white,  color='white',  label='Белый лист')
ax.plot(λs, luma_yellow, color='yellow', label='Жёлтый лист')
ax.plot(λs, luma_mercury, color='black')
ax.grid('--', which='major')
ax.minorticks_on()
ax.legend()

plt.savefig('test_inten.png')

fig.show()