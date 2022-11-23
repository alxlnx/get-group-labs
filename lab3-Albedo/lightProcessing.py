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

    inten = liFu.readIntensity(f'{name}.png', f"{name}_G_COOKED.png", f"{lamp_type}", f"{color_type}")
    intensities.append(inten)

### Калибровка ###
# Пусть длина волны λ задаётся формулой λ(n) = k * n + b, где n - номер столбца пикселей.
# Тогда коэффиценты k и b можно определить по трём точкам методом наименьших квадратов.
# Если же точек всего две, то следует решить систему линейных уравнений на k и b.
###

## Номера столбцов пикселей на графике для Hg, где наблюдается наибольшая "яркость". 
# На глаз:
red_max_pixel   = 130
green_max_pixel = 180
blue_max_pixel  = 245
# Расчёт по данным:
luma_mercury = intensities[0]
# Визуально определим, в какой области находится пики.
# Я не знаю, как заставить argmax() искать только в определённой области.
red_search   = luma_mercury[100:150]
green_search = luma_mercury[150:200]
blue_search   = luma_mercury[200:300]

red_max_pixel = np.argmax(red_search)     + 100
green_max_pixel = np.argmax(green_search) + 150
blue_max_pixel = np.argmax(blue_search)   + 200

# Длины волн с Википедии
red_λ   = 578.2    # нм
green_λ = 546.0735 # нм
blue_λ  = 435.8328 # нм

# Получение зависимости по трём точкам.
ys = [red_λ, green_λ, blue_λ]
xs = [red_max_pixel, green_max_pixel, blue_max_pixel]
(k, b) = np.polyfit(xs, ys, 1)

# Запись в файл.
with open("calibration.txt", 'w') as outfile:
    payload = f'λ(n) = {k:.3f}*n + {b:.3f}\n' +\
              'Точность: три знака после запятой.\n'
    outfile.write(payload)

### Построение графиков зависимости "яркости" от λ ###
# Переводим номера пикселей в длины волн.
λs = []
for px in range( len(luma_mercury) ):
    λ = k * px + b
    λs.append(λ)

# Настройка графика.
fig, ax = plt.subplots( figsize=(10, 5), dpi=200 )
ax.minorticks_on()
ax.set_facecolor('#EDEDED')
ax.grid(which='major', linestyle='-', linewidth=0.5)
ax.grid(which='minor', linestyle='--', linewidth=0.3)


font = {'fontname': 'DejaVu Serif'}
ax.set_xlabel('Длина волны, нм', **font)
ax.set_ylabel('Яркость', **font)
ax.set_title('Рис 1. Отражённая интенсивность излучения лампы накаливания', **font)

luma_blue   = intensities[1]  # Синий лист, лампа накаливания.
luma_green  = intensities[2]  # Зелёный лист, лампа накаливания.
luma_red    = intensities[3]  # Красный лист, лампа накаливания.
luma_white  = intensities[4]  # Белый лист, лампа накаливания.
luma_yellow = intensities[5]  # Жёлтый лист, лампа накаливания.

LINE_WIDTH = 2
ax.plot(λs, luma_blue,   color='blue',   label='Синий лист',   linewidth=LINE_WIDTH)
ax.plot(λs, luma_green,  color='green',  label='Зелёный лист', linewidth=LINE_WIDTH)
ax.plot(λs, luma_red,    color='red',    label='Красный лист', linewidth=LINE_WIDTH)
ax.plot(λs, luma_white,  color='white',  label='Белый лист',   linewidth=LINE_WIDTH)
ax.plot(λs, luma_yellow, color='yellow', label='Жёлтый лист',  linewidth=LINE_WIDTH)
ax.legend()

plt.savefig('!INTENSITIES_COOKED.png')

### Построение графиков зависимости альбедо от λ ###
albedoes = {'blue':   [],
            'green':  [],
            'red':    [],
            'white':  [],
            'yellow': []}
### 
#           I_отражённого_света
# Albedo = ---------------------
#           I_падающего_света
# I_падающего_света = const для всех цветов, кроме того, Albedo белого листа === 1
# Выходит, что
#                 I_отражённого_от_color_света
# Albedo_color = ------------------------------ * Albedo_white
#                 I_отражённого_от_белого_света
###

# Вычисление альбедо:
# Альбедо белого листа примем за 1, хотя это и не совсем так.
for i in range(len(luma_white)):
    albedoes['white'].append(1)
# Синий
for i in range(len(luma_blue)):
    if luma_white[i] == 0 or luma_blue[i] < 0.05:
        albedo = 0
    else: albedo = luma_blue[i] / luma_white[i]
    albedoes['blue'].append(albedo)
# Зелёный
for i in range(len(luma_green)):
    if luma_white[i] == 0 or luma_green[i] < 0.05:
        albedo = 0
    else: albedo = luma_green[i] / luma_white[i]
    albedoes['green'].append(albedo)
# Красный
for i in range(len(luma_red)):
    if luma_white[i] == 0 or luma_red[i] < 0.05:
        albedo = 0
    else: albedo = luma_red[i] / luma_white[i]
    albedoes['red'].append(albedo)
# Жёлтый
for i in range(len(luma_yellow)):
    if luma_white[i] == 0 or luma_yellow[i] < 0.05:
        albedo = 0
    else: albedo = luma_yellow[i] / luma_white[i]

    ### НА НЕКОТОРЫХ ПИКСЕЛЯХ РЕЗУЛЬТАТ ЗАШКАЛИВАЕТ
    if albedo > 1.5:
      albedo = 1
    ###
    
    albedoes['yellow'].append(albedo)

## Настройка графика
fig, ax = plt.subplots( figsize=(10, 5), dpi=200 )
ax.minorticks_on()
ax.set_facecolor('#EDEDED')
ax.grid(which='major', linestyle='-', linewidth=0.5)
ax.grid(which='minor', linestyle='--', linewidth=0.3)

font = {'fontname': 'DejaVu Serif'}
ax.set_xlabel('Длина волны, нм', **font)
ax.set_ylabel('Альбедо', **font)
ax.set_title('Рис 2. Зависимость альбедо поверхностей от длины волны падающего света', **font)

LINE_WIDTH = 2
ax.plot(λs, albedoes['blue'],   color='blue',   label='Синий лист',   linewidth=LINE_WIDTH)
ax.plot(λs, albedoes['green'],  color='green',  label='Зелёный лист', linewidth=LINE_WIDTH)
ax.plot(λs, albedoes['red'],    color='red',    label='Красный лист', linewidth=LINE_WIDTH)
ax.plot(λs, albedoes['white'],  color='white',  label='Белый лист',   linewidth=LINE_WIDTH)
ax.plot(λs, albedoes['yellow'], color='yellow', label='Жёлтый лист',  linewidth=LINE_WIDTH)
ax.legend(loc='upper left')

plt.savefig('!ALBEDOES_COOKED.png')
fig.show()