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

import math
"""
The vehicle class is basically used as a struct to contain data regarding the vehicles
x = x-position
y = y-position
v = velocity
h = heading
e_d = distance to ego car
e_a = angle relative to ego car
"""
class Vehicle:
    def __init__(self, x=0, y=0, v=0, h=0, e_d=0, e_a=0):
        self.x = x
        self.y = y
        self.v = v
        # Compensating for a bug in the sim, sometimes showing negative degrees
        if h < 0:
            self.h = 360 - h
        else:
            self.h = h
        self.e_d = e_d
        self.e_a = e_a
    # Function to show all assigned variables of the Vehicle, for debugging
    def status(self):
        print("x: " + str(self.x))
        print("y: " + str(self.y))
        print("v: " + str(self.v))
        print("h: " + str(self.h))
        print("e_d: " + str(self.e_d))
        print("e_a: " + str(self.e_a))
    
#Formatting String into the single Vehicle variables    
def format_string(s):
    # Removing Whitespaces
    s = s.replace(' ', '')
    # separate into list
    l = s.split('/')
    # Create list to hold items
    vehicles = []
    # Creating an Object of the Class Vehicle per vehicle.
    # Note, the ego-vehicle is always the first on the list, accessible as
    # vehicles[0]
    for i in range(5):
        vehicles.append(Vehicle(
            float(l[1 + 8*i]),
            float(l[3 + 8*i]),
            float(l[5 + 8*i]),
            float(l[7 + 8*i])
        ))
    return(vehicles)

"""
Transposing the vehicles in relation to ego-vehicle
First, the origin of the matrix is set to the location of the ego-vehicle,
so the ego-vehicle has the coordinates 0,0 and all other vehicles are set
respectively.
Then, the matrix is rotated in such a way, that the ego-vehicle going straight
equals 0°, a car exactly on the left would be at 270° and a car exactly on the
right 90°. This makes further computations with differing angles being covered
by the LED strip or other devices easier.
Input and Output of function a list containing members of Vehicle-class.
"""
def transposing_vehicles(vehicles):
    
    # Transposing origin to ego vehicle
    for i in range(1,5):
        vehicles[i].x = vehicles[0].x - vehicles[i].x
        vehicles[i].y = vehicles[0].y - vehicles[i].y
    vehicles[0].x = 0
    vehicles[0].y = 0
    
    # Rotate matrix, so that ego vehicle's direction is 0
    rot = -(vehicles[0].h) - 90
    # math-library works with radians, therefore convert to radians
    rot_rad = math.radians(rot)
    for i in range(1,5):
        x = vehicles[i].x
        y = vehicles[i].y
        vehicles[i].x = x*math.cos(rot_rad) - y*math.sin(rot_rad)
        vehicles[i].y = x*math.sin(rot_rad) + y*math.cos(rot_rad)
        vehicles[i].h = vehicles[i].h + rot
    vehicles[0].h = 0
    return vehicles
        
# Computing the distances relative to the ego car
def dist_to_ego(vehicles):
    # Just calculate hypotenuse of coordinates(automatically the x/y distances)
    for i in range(1,5):
        vehicles[i].e_d = math.sqrt(vehicles[i].x**2 + vehicles[i].y**2)
    return vehicles

# Computing the relative angle to the ego car
def angle_to_ego(vehicles):
    for i in range(1,5):
        vehicles[i].e_a = math.degrees(math.atan2(math.radians(vehicles[i].x), math.radians(vehicles[i].y)))
        # Convert negative values back tp positive ones
        if vehicles[i].e_a < 0:
            vehicles[i].e_a = 360 + vehicles[i].e_a
    return vehicles

"""
Computing the central LED that has to light up representing the respective car.
veh = Vehicle from the Vehicle-class
step = the angle-"distances" between each pixel
f_pixels = Why is that in there? :D
returns the central pixel as int
"""
def led_position_front(veh, step, f_pixels):
    # Position if car on the right side
    if veh.e_a <= LED_DEGREES/2:
        return int((LED_DEGREES/2 - veh.e_a) / step)
    # Position if car on left side
    elif veh.e_a >= 360 - LED_DEGREES/2:
        return int((-(veh.e_a - 360) + LED_DEGREES/2) / step)
        #return round((veh.e_a - LED_DEGREES)/ step)
        #return round(((360 - veh.e_a) + LED_DEGREES/2) / step)
    else:
        return None
    
def led_position_back(veh, step_back, b_pixels):
    return int((veh.e_a - LED_DEGREES/2) / step_back)

"""
Annoyingly written function for a simple LED pattern which is shown for the
front of the LEDs, meaning where the location of the pixel is supposed to 
accurately represent the one of the car.
Two aspects are regarded in this pattern: The angle, represented by the
location of the pixel(s) lighting up, as well as the distance to the ego car.
THe latter one is represented by the number of pixels lighting up as well as
how strongly they are lighting up.
"""
def simple_led_pattern(vehicles):
    """
    Change Light unsurprisingly changes a light, well, a pixel.
    add_val: value to be added to pixel
    f_pixels: the array of front pixels, to be changed
    led_pos: The CENTRAL pixel of the car-representation
    led_ord: The order of the value, so +- around the central pixel.
    Returns the changed front pixel array
    """
    def change_light(add_val, f_pixels, led_pos, led_ord):
        if add_val <= 0:
            return f_pixels
        elif add_val >= 1:
            if led_ord == 0:
                f_pixels[led_pos] = 1
                return f_pixels
            else:
                try:
                    f_pixels[led_pos + led_ord] += 1
                except IndexError:
                    pass
                try:
                    f_pixels[led_pos - led_ord] += 1
                except IndexError:
                    pass
                return f_pixels
        else:
            if led_ord == 0:
                f_pixels[led_pos] += add_val
                return f_pixels
            else:
                try:
                    f_pixels[led_pos + led_ord] += add_val
                except IndexError:
                    pass
                try:
                    f_pixels[led_pos - led_ord] += add_val
                except IndexError:
                    pass
                return f_pixels
    
    # Noof pixels representing back of car on every side
    b_pixels = 10
    # Noof front pixels can be calculated from all of the parameters
    f_pixels = PIXEL_COUNT - b_pixels * 2
    # Pixel vector for the front pixels
    pix_vec = [0] * f_pixels
    pix_vec_back = [0] * (2 * b_pixels)
    # The distance, from which on a car is represented on the screen
    threshold = 200
    # 
    step = LED_DEGREES / f_pixels
    step_back = (360 - LED_DEGREES) / (2 * b_pixels)
    led_pref = [
                [200, 60],
                [150, 45],
                [100, 30],
                [60, 20],
                [30, 10],
                [18, 0]
                ]
    
    
    vehicles.pop(0)
    for i in vehicles:
        if i.e_d <= threshold:
            led_c = led_position_front(i, step, f_pixels)
            if led_c != None:
                bright_list = []
                for j in led_pref:
                    bright_list.append((j[0] - i.e_d) / (j[0] - j[1]))
                print(bright_list)
                for j in range(len(bright_list)):
                    """
                    bright_list j = 
                    pix vec = Total vectors of pixels used for LED strip
                    ledc = the central LED position
                    j = diversion from ledc
                    """
                    pix_vec = change_light(bright_list[j], pix_vec, led_c, j)
            else:
                led_c = led_position_back(i, step_back, b_pixels)
                bright_list = []
                for j in led_pref:
                    bright_list.append((j[0] - i.e_d) / (j[0] - j[1]))
                for j in range(len(bright_list)):
                    pix_vec_back = change_light(bright_list[j], pix_vec_back, led_c, j)
    
    print(pix_vec_back)
    pix_vec_b_r = pix_vec_back[:b_pixels]
    pix_vec_b_r.reverse()
    pix_vec_b_l = pix_vec_back[b_pixels:]
    pix_vec_b_l.reverse()
    
    vec_vec = [pix_vec_b_r, pix_vec, pix_vec_b_l]
    print(vec_vec)
    return vec_vec
                    

def show_LEDs(pixels, led_vector):
    pix = 0
    for i in range(len(led_vector[0])):
        pixels.set_pixel_rgb(pix, int(led_vector[0][i] * 255), 0, int(led_vector[0][i] * 255))
        pix += 1
    for i in range(len(led_vector[1])):
        pixels.set_pixel_rgb(pix, int(led_vector[1][i] * 255), 0, 0)
        pix += 1
    for i in range(len(led_vector[2])):
        pixels.set_pixel_rgb(pix, int(led_vector[2][i] * 255), 0, int(led_vector[2][i] * 255))
        pix += 1
    # pixels.clear()
    pixels.show()

if __name__ == "__main__":
    # Clear all the pixels to turn them off.
    pixels.clear()
    pixels.show()  # Make sure to call show() after changing any pixels!





while True:
    data, addr = sock.recvfrom(300) # buffer size is 1024 bytes
    vehicles = format_string(str(data))
    vehicles[1].x
    vehicles = transposing_vehicles(vehicles)
    vehicles = dist_to_ego(vehicles)
    vehicles = angle_to_ego(vehicles)
    for i in vehicles:
        i.status() 
    led_vector = simple_led_pattern(vehicles)
    print(led_vector)
    show_LEDs(pixels, led_vector)
    
    

    #print("received message:", data)
    