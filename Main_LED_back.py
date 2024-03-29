# Stuff relating UDP connection
import socket
# Set IP of the Raspberry Pi
UDP_IP = "192.168.1.101"
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
# The radius which the LED strip approximately covers
#LED_DEGREES = 230
LED_DEGREES = 190

# Alternatively specify a hardware SPI connection on /dev/spidev0.0:
SPI_PORT   = 0
SPI_DEVICE = 0
# pixels accesses the strip itself programmatically
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)
# Take over refers to a different scenario, where the car first drives itself.
take_over = False

import SimProc
import LEDBasics
import SimpleLEDPattern_noback
import SimpleLEDPattern_back
import SimpleLEDPattern_noback_dim

if __name__ == "__main__":
    # Clear all the pixels to turn them off.
    pixels.clear()
    pixels.show()  # Make sure to call show() after changing any pixels!

# Loop running all functions relating the LED strip processing
while True:
    # Gets data from driving sim over UDP
    data, addr = sock.recvfrom(300) # buffer size is 1024 bytes
    # Processing data of all vehicles
    vehicles, take_over = SimProc.preproc(data)
    for i in vehicles:
        i.status()
        
    # Converts the state of vehicles into respective LED patterns
    led_vector = SimpleLEDPattern_back.main(vehicles, PIXEL_COUNT, LED_DEGREES)
    print(led_vector)
    
    curr_time = int(round(time.time() * 10))
    
    # Showing the LEDs in their respective colors!
    if take_over == True and ( curr_time % 10 < 2 or 4 <= curr_time % 10 < 6 or curr_time % 10 >= 8 )  :
        print("Its off")
        pixels.clear()
        pixels.show()
    else:
        LEDBasics.show_LEDs(pixels, led_vector, ["red", "yellow"])
        #LEDBasics.show_LEDs(pixels, led_vector, ["yellow", "red"])
        #LEDBasics.show_Dim_LEDs(pixels, led_vector, ["yellow_to_red", "yellow_to_red"], color_vector)

    

    #print("received message:", data)
    
