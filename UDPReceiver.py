# Stuff relating UDP connection
import socket
# Set IP of the Raspberry Pi
UDP_IP = "145.90.179.96"
# Set Port used bz Simulator to send data
UDP_PORT = 30002
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

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

import SimProc
import LEDBasics
import SimpleLEDPattern

if __name__ == "__main__":
    # Clear all the pixels to turn them off.
    pixels.clear()
    pixels.show()  # Make sure to call show() after changing any pixels!


while True:
    data, addr = sock.recvfrom(300) # buffer size is 1024 bytes
    vehicles = SimProc.preproc(data)
    for i in vehicles:
        i.status() 
    led_vector = SimpleLEDPattern.main(vehicles, PIXEL_COUNT, LED_DEGREES)
    print(led_vector)
    LEDBasics.show_LEDs(pixels, led_vector, ["red", "yellow"])
    #LEDBasics.show_LEDs(pixels, led_vector, ["yellow", "red"])

    
    

    #print("received message:", data)
    