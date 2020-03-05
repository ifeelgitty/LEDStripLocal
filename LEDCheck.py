# Stuff relating LED Strip
import time
import RPi.GPIO as GPIO
# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI
# Configure the count of pixels(32 per meter):
PIXEL_COUNT = 192
# The radius which  
LED_DEGREES = 180
# Alternatively specify a hardware SPI connection on /dev/spidev0.0:
SPI_PORT   = 0
SPI_DEVICE = 0
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)

pixels.clear()
for i in range(PIXEL_COUNT):
    pixels.set_pixel_rgb(i, 255, 0, 0)
    pixels.show()
    time.sleep(0.02)

for i in range(PIXEL_COUNT):
    pixels.set_pixel_rgb(i, 12, 255, 222)
    pixels.show()
    time.sleep(0.02)
    
for i in range(PIXEL_COUNT):
    pixels.set_pixel_rgb(i, 0, 0, 255)
    pixels.show()
    time.sleep(0.02)