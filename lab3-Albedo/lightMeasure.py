from time import sleep
from picamera import PiCamera

camera = PiCamera()
camera.brightness = 53

camera.start_preview() # Camera warm-up time
sleep(2)
camera.capture('mercury_white_(2).png') # Take a picture

#camera.stop_preview()

# camera.resolution = (1280, 720)
# camera.contrast = 10