import numpy as np

filename_0   = '0mmHg - blood-data 2022-11-03 13:51:30.txt'
filename_40  = '40mmHg - blood-data 2022-11-03 13:47:37.txt'
filename_80  = '80mmHg - blood-data 2022-11-03 13:48:36.txt'
filename_120 = '120mmHg - blood-data 2022-11-03 13:49:44.txt'
filename_160 = '160mmHg - blood-data 2022-11-03 13:50:26.txt'

with open(filename_160, 'r') as file0:
    lines = file0.readlines()

vals0 = []
vals0_str = lines[4::1]
for line in vals0_str:
    line.rstrip('\n')
    val0 = int(line)
    vals0.append(val0)

# print(vals0)
val0_mean = np.mean(vals0)
print(val0_mean)