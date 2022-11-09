'''
Этот скрипт обрабатывает данные, полученные с АЦП, и строит по ним график.
'''

import matplotlib.pyplot as plt
import numpy as np

k = 1 / 7.5
b = 205.4
def get_pressure_mmHg(number):
    ''' Перевести значение давления (напряжения), полученное с АЦП, в ммРтСт '''
    result = k*(number - b)
    return result

# ----------------------------------------
# --------- READ & PROCESS DATA ----------
# --- BEFORE ---
before_filename = 'BEFORE ACTIVITY - blood-data 2022-11-03 14_26_53.txt'
after_filename  = 'AFTER ACTIVITY - blood-data 2022-11-03 14_30_33.txt'

# Чтение сырых данных из файла
lines = []                                              # Raw strings from file
with open(before_filename, 'r') as beforef:
    lines = beforef.readlines()

# Получение из сырых данных времени эксперимента
before_duration_line  = lines[2]                        # Duration: ...
before_duration = float(before_duration_line[12:17])

# Получение из сырых данных значений давления (напряжения) с АЦП
before_data_lines = lines[4::]                          # numbers, numbers...
before_data = []                                        # Готовый список чисел (значений с АЦП)
for data_line in before_data_lines:
    data_line.rstrip('\n')
    data = int(data_line)

    data = get_pressure_mmHg(data)

    before_data.append(data)
before_data = np.array(before_data)

before_times = np.arange(0, before_duration,           # Соответствующие моменты времени 
                        before_duration/len(before_data)) 
# --- AFTER ---
# Полностью аналогично BEFORE
# -------------
with open(after_filename, 'r') as afterf:
    lines = afterf.readlines()

after_duration_line  = lines[2]                         # Duration: ...
after_duration = float(after_duration_line[12:17])

after_data_lines = lines[4::]                           # numbers, numbers...
after_data = []
for data_line in after_data_lines:
    data_line.rstrip('\n')
    data = int(data_line)

    data = get_pressure_mmHg(data)

    after_data.append(data)
after_data = np.array(after_data)

after_times = np.arange(0, after_duration, after_duration/len(after_data))

# -----------------------------------
# --------- DRAW THE GRAPH ----------

SPACING = 50                   # Отображаем каждую "SPACING"-ую строчку
figure, axes = plt.subplots()
plt.minorticks_on()
plt.grid(which='major', linestyle='--', linewidth=0.5) # '-', '--', '-.', ':', '',

#Общие настройки
#axes.set_ylabel('Давление [мм рт.ст.]')
axes.set_ylabel('Изменение давления в артерии [мм рт.ст.]') #Меняем надпись в зависимости от графика (пульс -> изменение)
axes.set_xlabel('Время, с')

#Настройки для "до нагрузки"
"""
axes.set_xlim([0, 45])
axes.set_ylim([0, 200])
axes.set_title('Артериальное давление до физической нагрузки', wrap=True)
axes.plot(before_times[::SPACING], before_data[::SPACING], ms=0.25, label='Давление - 140/69 [мм рт.ст.]')
axes.scatter(before_times[270500], 140, c='r', marker = '*', s = 50)
axes.scatter(before_times[516000], 68.8, c='r', marker = '*', s = 50)
axes.text(0.40, 0.75, 'Systole', horizontalalignment='center', verticalalignment='center', transform=axes.transAxes)
axes.text(0.80, 0.37, 'Diastole', horizontalalignment='center', verticalalignment='center', transform=axes.transAxes)
"""

#Настройки для пульса "до нагрузки"
"""
#Усреднение измерения "с окном"
tmp_before_data = []
mean_before_data = [] #Массив со средними значениями
before_times_fmean = []

start = 270500
step = 12275
end = start

for i in range(20):
    end += step

    tmp_before_data = np.array(before_data[start:end])
    mean_before_data.append(np.mean(tmp_before_data))

    tmp_before_data = np.array(before_times[start:end])
    before_times_fmean.append(np.mean(tmp_before_data))
    
    start += step


print(mean_before_data)
print(before_times_fmean)
"""

"""
Проверка усреднения
axes.set_xlim([0, 45])
axes.set_ylim([0, 200])
axes.set_title('Артериальное давление до физической нагрузки', wrap=True)
axes.plot(before_times_fmean, mean_before_data, ms=0.25, label='Давление - 140/69 [мм рт.ст.]')
"""
"""
#Вычитание из исходного массива усредненный массив
new_before_data = []
substructer = 0
start = 270500
step = 12275
for i in range(20):
    substructer = mean_before_data[i]
    start = 270500 + i * step
    for j in range(12275):
        new_before_data.append(before_data[start + j] - substructer)

#Построение графика "Пульс до нагрузки"
axes.set_xlim([18.0, 33.0])
axes.set_ylim([-5, 5])
axes.set_title('Пульс \nдо физической нагрузки', wrap=True)
axes.plot(before_times[270500:516000:SPACING], new_before_data[::SPACING], ms=0.25, label='Пульс - 104 [уд. мин]')
"""

#Настройки для "после нагрузки"
"""
axes.set_xlim([0, 50])
axes.set_ylim([0, 250])
axes.set_title('Артериальное давление после физической нагрузки', wrap=True)
axes.plot(after_times[::SPACING], after_data[::SPACING], ms=0.25, label='Давление - 199/98 [мм рт.ст.]', c='orange')
axes.scatter(after_times[133800], 199, c='r', marker = '*', s = 50)
axes.scatter(after_times[398500], 98, c='r', marker = '*', s = 50)
axes.text(0.22, 0.81, 'Systole', horizontalalignment='center', verticalalignment='center', transform=axes.transAxes)
axes.text(0.55, 0.40, 'Diastole', horizontalalignment='center', verticalalignment='center', transform=axes.transAxes)
"""


#Настройки для пульса "после нагрузки"

#Усреднение измерения "с окном"
tmp_after_data = []
mean_after_data = [] #Массив со средними значениями
after_times_fmean = []

start = 134000
step = 13300
end = start

for i in range(20):
    end += step

    tmp_after_data = np.array(after_data[start:end])
    mean_after_data.append(np.mean(tmp_after_data))

    tmp_after_data = np.array(after_times[start:end])
    after_times_fmean.append(np.mean(tmp_after_data))
    
    start += step


print(mean_after_data)
print(after_times_fmean)

#Вычитание из исходного массива усредненный массив
new_after_data = []
substructer = 0
start = 134000
step = 13300
for i in range(20):
    substructer = mean_after_data[i]
    start = 134000 + i * step
    for j in range(13300):
        new_after_data.append(after_data[start + j] - substructer)

#Построение графика "Пульс до нагрузки"
axes.set_xlim([9, 25])
axes.set_ylim([-10, 10])
axes.set_title('Пульс \nпосле физической нагрузки', wrap=True)
axes.plot(after_times[134000:400000:SPACING], new_after_data[::SPACING], ms=0.25, c="orange", label='Пульс - 131 [уд. мин]')




axes.legend()
plt.show()
