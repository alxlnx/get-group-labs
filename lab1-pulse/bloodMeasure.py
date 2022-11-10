import time
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import bloodFunctions as b

GPIO.setmode(GPIO.BCM)

# This setup (idk what exactly should go here)
# was done beforehand by one the teachers.
# GPIO.setup(9,  ) 
# GPIO.setup(10, )
# GPIO.setup(11, )

b.initSpiAdc()

PRESSURE_LOWER_BOUND = 350  # Pressure, after which the measurements are stopped.

is_calibrating = False      # Since we have a separate routine for calibration.
if is_calibrating == False:
    try:
        samples = []

        start = time.time()
        while True:
            current_data = b.getAdc()
            samples.append(current_data)

            if current_data < PRESSURE_LOWER_BOUND:
                break
        
        finish = time.time()

        b.save(samples, start, finish)

        plt.plot(samples)
        plt.show()
    except KeyboardInterrupt:
        finish = time.time()
        b.save(samples, start, finish)
        plt.plot(samples)
        plt.show()
    finally:
        b.deinitSpiAdc()
else:
    try:
        samples = []

        start = time.time()
        while True:
            now = time.time()
            current_data = b.getAdc()
            samples.append(current_data)

            if now - start >= 10:
                break
                 
        finish = time.time()

        b.save(samples, start, finish)
    except KeyboardInterrupt:
        finish = time.time()
        b.save(samples, start, finish)
        plt.plot(samples)
        plt.show()
    finally:
        b.deinitSpiAdc()