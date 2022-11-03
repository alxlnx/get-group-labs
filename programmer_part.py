'''
Этот скрипт обрабатывает данные, полученные с АЦП, и строит по ним график.
'''

import matplotlib.pyplot as plt
import numpy as np

k = 1 / 7.5
b = 205.4
def get_pressure_mmHg(number):
    result = number * k + b
    return result

# --------- READ DATA ----------
# --- BEFORE ---
before_filename = 'BEFORE ACTIVITY - blood-data 2022-11-03 14:26:53.txt'
after_filename  = 'AFTER ACTIVITY - blood-data 2022-11-03 14:30:33.txt'

lines = []  # Raw strings from file
with open(before_filename, 'r') as beforef:
    lines = beforef.readlines()

before_duration_line  = lines[2]    # Duration: ...
before_duration = float(before_duration_line[12:17])

before_data_lines = lines[4::]  # numbers, numbers...
before_data = []
for data_line in before_data_lines:
    data_line.rstrip('\n')
    data = int(data_line)

    data = get_pressure_mmHg(data)

    before_data.append(data)
before_data = np.array(before_data)

before_times = np.arange(0, before_duration, before_duration/len(before_data))

# --- AFTER ---
with open(after_filename, 'r') as afterf:
    lines = afterf.readlines()

after_duration_line  = lines[2]    # Duration: ...
after_duration = float(after_duration_line[12:17])

after_data_lines = lines[4::]  # numbers, numbers...
after_data = []
for data_line in after_data_lines:
    data_line.rstrip('\n')
    data = int(data_line)

    data = get_pressure_mmHg(data)

    after_data.append(data)
after_data = np.array(after_data)

after_times = np.arange(0, after_duration, after_duration/len(after_data))

# --------- PROCCESS DATA ----------

# --------- DRAW THE GRAPH ----------
figure, axes = plt.subplots()
axes.plot(before_times[::100], before_data[::100], ms=0.25, label='До')
axes.plot(after_times[::100], after_data[::100], ms=0.25, label='После')
axes.legend()
plt.show()