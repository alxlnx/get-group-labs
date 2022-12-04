import matplotlib.pyplot as plt
import numpy as np
import math

# # --------CALLIBRATION PRESSURE--------
# acp_value_inside = 1317.908 #Среднее значение с АЦП внутри потока
# acp_value_away = 977.562 #Среднее значение с АЦП вне потока
# rl_value_inside = 69.73 #Среднее значение на электронном манометре внутри потока (ПА)
# rl_value_away = 0 #Среднее значение на электронном манометре вне потока (ПА)


# rl_values = np.array([rl_value_away, rl_value_inside*3]) #Две точки аппроксимирующей прямой
# k = (acp_value_inside - acp_value_away) / rl_value_inside #Коэф. наклона прямой

# plt.plot(rl_values, k*rl_values + acp_value_away, "-", linewidth=2, c='orange', zorder=3)
# plt.scatter([rl_value_away, rl_value_inside], [acp_value_away, acp_value_inside], c='green', zorder=4)
# plt.title('Калибровочный график зависимости \nпоказаний АЦП от давления')

# plt.xlim(0, 200)
# plt.ylim(0, 2500)
# plt.xlabel('Давление [Па]')
# plt.ylabel('Показания АЦП')

# print(k)

# plt.minorticks_on()
# plt.grid(which='major', linewidth=0.8)
# plt.grid(which='minor', color='#DDDDDD', linestyle = '--', linewidth=0.5)
# plt.legend(['Измерения (средние значения)', r'$P$ = 0,205 $\cdot$ $N$ - 200,40 [Па]'])
# plt.show()
 
# # --------CALLIBRATION DISTANCE--------
# steps = 800 #Кол-во шагов трубки
# distance = 4.4 #Перемещение трубки [см]

# distances = np.array([0, 15]) #Две точки аппроксимирующей прямой
# p = steps/distance #Коэф. прямой
# plt.plot(p*distances, distances, "-", linewidth=2, c='coral', zorder=3)
# plt.scatter([0, steps], [0, distance], c='darkblue', zorder=4)
# plt.title('Калибровочный график \nзависисмости премещения трубки Пито от шага двигателя')

# plt.xlim(0, 1500)
# plt.ylim(0, 8)
# plt.xlabel('Перемещение трубки Пито [см]')
# plt.ylabel('Количество шагов')


# plt.minorticks_on()
# plt.grid(which='major', linewidth=0.8)
# plt.grid(which='minor', color='#DDDDDD', linestyle = '--', linewidth=0.5)
# plt.legend(['Измерения', r'$X$ = 0,0055 $\cdot$ $steps$ [см]'])
# plt.show()

# --------FUNCS FOR READ & PROCESS DATA--------
def get_pressure_pa(acp_data):
    '''Перевести значение давления, полученное с АЦП, в ПА'''
    real_pressure = abs(0.205 * acp_data - 200.4)
    return real_pressure

def get_full_pa_data(fileName):
    '''Перевести массив давлений, полученных с АЦП, в ПА'''
    distances_filename = fileName

    lines = []
    with open(distances_filename, 'r') as f_mm:
        lines = f_mm.readlines()

    distances_lines = lines[3::]
    distances = []
    for data_line in distances_lines:
        data_line.rstrip('\n')
        data = int(data_line)
        data = get_pressure_pa(data)
        distances.append(data)
    
    return(distances)

def get_speeds_data(pdata):
    '''Перевести массив давлений в [ПА], в скорости [м/с]'''
    speed_value = 0
    sdata = []
    for i in range(len(pdata)):
        speed_value = float(((2*pdata[i])/1.2)**0.5)
        sdata.append(speed_value)
    
    return(sdata)

def get_max(speeds):
    max_speed = max(speeds)
    max_index = 0
    for i in range(45, 55):
        if speeds[i] == max_speed:
            max_index = i
    return max_index

def jet_flow_calculation(distances, speeds):
    #Урезаем облатсь подсчёта, т.к. трубка Пито в первых и последних 30 точках находится вне диаметра сопла
    distances_ = distances[30:70]
    speeds = speeds[30:70]

    q = 0 #Единичный расход
    Q = 0 #Суммарный расход
    for i in range(39):
        q = 0.5*(abs(distances[i])*(speeds[i]-10) + abs(distances[i+1])*(speeds[i+1]-10))*abs(abs(distances[i+1]) - abs(distances[i]))
        #Учитываем, что график находится примерно на десять единиц выше нуля, т.е. помимо расхода струи присутствует ещё какая-то компонента...
        #...которую нужно исключить
        Q += q
    
    Q = Q * 2 * 3.14 * 1200 #Используем формулу 1.5 из теории для подсчёта расхода. Сразу же переводим м^3/c в г/с, домножая на плотность 1200 [г/с]
    return Q


# --------READ & PROCESS DATA--------
positions = np.linspace(-44, 44, 200) #Положение трубки относительно центра

pressures_data_0 = get_full_pa_data('0mm.txt') #Массив давлений 0 в [Па]
speeds_data_0 = get_speeds_data(pressures_data_0) 
speeds_data_0 = np.array(speeds_data_0) #Скорости 0 в [м/с]
max_0 = 50 - get_max(speeds_data_0) #Индекс максимума
Q_0 = jet_flow_calculation((0.001*positions[50-3:150-3]), speeds_data_0) #Расход 0

pressures_data_10 = get_full_pa_data('10mm.txt') #Массив давлений 10 в [Па]
speeds_data_10 = get_speeds_data(pressures_data_10) 
speeds_data_10 = np.array(speeds_data_10) #Скорости 10 в [м/с]
max_10 = 50 - get_max(speeds_data_10) #Индекс максимума
Q_10 = jet_flow_calculation((0.001*positions[50+max_10:150+max_10]), speeds_data_10) #Расход 10

pressures_data_20 = get_full_pa_data('20mm.txt') #Массив давлений 20 в [Па]
speeds_data_20 = get_speeds_data(pressures_data_20) 
speeds_data_20 = np.array(speeds_data_20) #Скорости 20 в [м/с]
max_20 = 50 - get_max(speeds_data_20) #Индекс максимума
Q_20 = jet_flow_calculation((0.001*positions[50+max_20:150+max_20]), speeds_data_20) #Расход 20

pressures_data_30 = get_full_pa_data('30mm.txt') #Массив давлений 30 в [Па]
speeds_data_30 = get_speeds_data(pressures_data_30) 
speeds_data_30 = np.array(speeds_data_30) #Скорости 30 в [м/с]
max_30 = 50 - get_max(speeds_data_30) #Индекс максимума
Q_30 = jet_flow_calculation((0.001*positions[50+max_30:150+max_30]), speeds_data_30) #Расход 30

pressures_data_40 = get_full_pa_data('40mm.txt') #Массив давлений 40 в [Па]
speeds_data_40 = get_speeds_data(pressures_data_40) 
speeds_data_40 = np.array(speeds_data_40) #Скорости 40 в [м/с]
max_40 = 50 - get_max(speeds_data_40) #Индекс максимума
Q_40 = jet_flow_calculation((0.001*positions[50+max_40:150+max_40]), speeds_data_40) #Расход 40

pressures_data_50 = get_full_pa_data('50mm.txt') #Массив давлений 50 в [Па]
speeds_data_50 = get_speeds_data(pressures_data_50) 
speeds_data_50 = np.array(speeds_data_50) #Скорости 50 в [м/с]
max_50 = 50 - get_max(speeds_data_50) #Индекс максимума
Q_50 = jet_flow_calculation((0.001*positions[50+max_50:150+max_50]), speeds_data_50) #Расход 50

pressures_data_60 = get_full_pa_data('60mm.txt') #Массив давлений 60 в [Па]
speeds_data_60 = get_speeds_data(pressures_data_60) 
speeds_data_60 = np.array(speeds_data_60) #Скорости 60 в [м/с]
max_60 = 50 - get_max(speeds_data_60) #Индекс максимума
Q_60 = jet_flow_calculation((0.001*positions[50+max_60:150+max_60]), speeds_data_60) #Расход 60

pressures_data_70 = get_full_pa_data('70mm.txt') #Массив давлений 70 в [Па]
speeds_data_70 = get_speeds_data(pressures_data_70) 
speeds_data_70 = np.array(speeds_data_70) #Скорости 70 в [м/с]
max_70 = 50 - get_max(speeds_data_70) #Индекс максимума
Q_70 = jet_flow_calculation((0.001*positions[50+max_70:150+max_70]), speeds_data_70) #Расход 70

pressures_data_80 = get_full_pa_data('80mm.txt') #Массив давлений 80 в [Па]
speeds_data_80 = get_speeds_data(pressures_data_80) 
speeds_data_80 = np.array(speeds_data_80) #Скорости 80 в [м/с]
max_80 = 50 - get_max(speeds_data_80) #Индекс максимума
Q_80 = jet_flow_calculation((0.001*positions[50+max_80:150+max_80]), speeds_data_80) #Расход 80

pressures_data_90 = get_full_pa_data('90mm.txt') #Массив давлений 90 в [Па]
speeds_data_90 = get_speeds_data(pressures_data_90) 
speeds_data_90 = np.array(speeds_data_90) #Скорости 90 в [м/с]
max_90 = 50 - get_max(speeds_data_90) #Индекс максимума
Q_90 = jet_flow_calculation((0.001*positions[50+max_90:150+max_90]), speeds_data_90) #Расход 90

# --------DRAW THE MAIN GRAPH--------
plt.plot(positions[50-3:150-3], speeds_data_0, "-", linewidth=1, zorder=3)
plt.plot(positions[50+max_10:150+max_10], speeds_data_10, "-", linewidth=1, zorder=4)
plt.plot(positions[50+max_20:150+max_20], speeds_data_20, "-", linewidth=1, zorder=5)
plt.plot(positions[50+max_30:150+max_30], speeds_data_30, "-", linewidth=1, zorder=6)
plt.plot(positions[50+max_40:150+max_40], speeds_data_40, "-", linewidth=1, zorder=7)
plt.plot(positions[50+max_50:150+max_50], speeds_data_50, "-", linewidth=1, zorder=8)
plt.plot(positions[50+max_60:150+max_60], speeds_data_60, "-", linewidth=1, zorder=9)
plt.plot(positions[50+max_70:150+max_70], speeds_data_70, "-", linewidth=1, zorder=10)
plt.plot(positions[50+max_80:150+max_80], speeds_data_80, "-", linewidth=1, zorder=11)
plt.plot(positions[50+max_90:150+max_90], speeds_data_90, "-", linewidth=1, zorder=12)

plt.title('Скорость потока воздуха \nв сечении затопленной струи')
plt.xlabel('Положение трубки Пито относительно центра струи [мм]')
plt.ylabel('Скорость воздуха [м/с]')
plt.xlim(-25, 25)
plt.ylim(0, 35)


plt.minorticks_on()
plt.grid(which='major', linewidth=0.8)
plt.grid(which='minor', color='#DDDDDD', linestyle = '--', linewidth=0.5)
plt.legend([r'$Q$ (00 мм) = 21.2 [г/с]', r'$Q$ (10 мм) = 18.9 [г/с]', r'$Q$ (20 мм) = 17.1 [г/с]', r'$Q$ (30 мм) = 18.4 [г/с]', r'$Q$ (40 мм) = 14.2 [г/с]', r'$Q$ (50 мм) = 12.2 [г/с]', r'$Q$ (60 мм) = 9.6 [г/с]', r'$Q$ (70 мм) = 14.1 [г/с]', r'$Q$ (80 мм) = 13.8 [г/с]', r'$Q$ (90 мм) = 13.0 [г/с]'])
plt.show()

# #--------DRAW THE Q-R GRAPH--------
# Qs = np.array([Q_0, Q_10, Q_20, Q_30, Q_40, Q_50, Q_60, Q_70, Q_80, Q_90]) #Расход струи
# Rs = np.array([0, 10, 20, 30, 40, 50, 60, 70, 80, 90]) #Расстоянеи до сопла

# print(Qs)

# plt.plot(Rs, Qs, "-", c='cornflowerblue', linewidth=2, zorder=3)
# plt.scatter(Rs, Qs, c='orangered', zorder=4)

# plt.title('Зависимость расхода от расстояния до сопла')
# plt.xlabel('Расстояние трубки Пито до сопла [мм]')
# plt.ylabel('Расход $Q$ [г/с]')
# plt.xlim(-10, 100)
# plt.ylim(0, 25)

# plt.minorticks_on()
# plt.grid(which='major', linewidth=0.8)
# plt.grid(which='minor', color='#DDDDDD', linestyle = '--', linewidth=0.5)
# plt.legend(['-', 'Значения'])
# plt.show()

