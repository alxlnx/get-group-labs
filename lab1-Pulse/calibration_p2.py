import numpy as np
import matplotlib.pyplot as plt

mm_0_mean = 128.14755260812015
mm_40_mean = 504.71675009058094
mm_80_mean = 886.4396748323825
mm_120_mean = 1253.2826511643627
mm_160_mean = 1657.0868222234344

y = [mm_0_mean, mm_40_mean, mm_80_mean, mm_120_mean, mm_120_mean]
x = [0, 40, 80, 120, 160]

k, b = np.polyfit(x, y, 1)
print(k, b)

# val = np.linspace(0, 1000, 1000)
# plt.plot(val, k * val + b)
# plt.show()