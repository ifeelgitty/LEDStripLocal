# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 21:22:19 2019

@author: soenk
"""

import logging

"""
Computing the central LED that has to light up representing the respective car.
veh = Vehicle from the Vehicle-class
step = the angle-"distances" between each pixel
returns the central pixel as int
"""

    
def led_position_back(veh, step_back, LED_DEGREES):
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


def main(vehicles, PIXEL_COUNT, LED_DEGREES):

    
    def led_position_front(veh, step, LED_DEGREES, b_pixels, step_rr, step_r, step_l, step_ll):
        if angle_to_bar_r <= veh.e_a <= LED_DEGREES/2:
            relative_ea = veh.e_a
            relative_led_degr = (LED_DEGREES/2)
            return int(((relative_led_degr) - relative_ea) / step_rr)
        elif 0 <= veh.e_a < angle_to_bar_r:
            return 69 - b_pixels + int((angle_to_bar_r - veh.e_a) / step_r) 
        elif (360 - angle_to_bar_l) <= veh.e_a <= 360:
            return 103 - b_pixels + int(-(veh.e_a - 360) / step_l)
        elif (360 - LED_DEGREES/2) <= veh.e_a:
            return 121 - b_pixels + int((-(veh.e_a - 360)-angle_to_bar_l) / step_ll)
        else:
            return None
        
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
                try:
                    f_pixels[led_pos] = 1
                except IndexError:
                    pass
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
                try:
                    f_pixels[led_pos] += add_val
                except IndexError:
                    pass
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
    b_pixels = 30
    # Noof front pixels can be calculated from all of the parameters
    f_pixels = PIXEL_COUNT - b_pixels * 2
    # Pixel vector for the front pixels
    pix_vec = [0] * f_pixels
    pix_vec_back = [0] * (2 * b_pixels)
    # The distance, from which on a car is represented on the screen
    threshold = 200
    # These represent the angles until the respective "end" of the middle screen of the simulator towards the right and left, which I've called "bar"
    angle_to_bar_r = 55
    angle_to_bar_l = 35
    # Steps refer to the angle steps from one LED to the next, which depending on the specific position changes, as the LED strips distance changes, so it's not a circle around the driver. figuring all of these values out is ANNOYING and takes a while, I basically had to do it by trial and error and am not claiming that it is perfectly right.
    step = LED_DEGREES / f_pixels
    step_rr = (LED_DEGREES/2 - angle_to_bar_r) / (69 - b_pixels)
    step_r = angle_to_bar_r / 34
    step_l = angle_to_bar_l / 18
    step_ll = (LED_DEGREES/2 - angle_to_bar_l) / (71 - b_pixels)
    step_back = (360 - LED_DEGREES) / (2 * b_pixels)
    
    # This refers to the distances at which the respective LEDs relative to the most central LED representing a car bright up and at which distance they are at their full brightness. Check the paper for a conceptual explanation! Basically: The central LED starts at 200 meters distance and is at full brightness at 60 meters distance, the ones to the right and left start at 150 and are full at 45, etc.
    led_pref = [
                [200, 60],
                [150, 45],
                [100, 30],
                [60, 20],
                [30, 10],
                [18, 0]
                ]
    
    led_pref_back = [
                [200, 70],
                [180, 60],
                [160, 55],
                [140, 45],
                [120, 40],
                [100, 35],
                [90, 30],
                [80, 25],
                [70, 22],
                [60, 20],
                [45, 15],
                [30, 10],
                [18, 0]
                ]
    
    
    vehicles.pop(0) # Delete ego car from list of surrounding vehicles :)
    
    # Looping over all vehicles
    for i in vehicles:
        if i.e_d <= threshold and i.e_d > 0:
            led_c = led_position_front(i, step, LED_DEGREES, b_pixels, step_rr, step_r, step_l, step_ll)
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
                led_c = led_position_back(i, step_back, LED_DEGREES)
                bright_list = []
                for j in led_pref_back:
                    bright_list.append((j[0] - i.e_d) / (j[0] - j[1]))
                for j in range(len(bright_list)):
                    pix_vec_back = change_light(bright_list[j], pix_vec_back, led_c, j)

    # Reshuffling the order to get three lists of pixels, representing the left-back, right-back and central(front), as this is necessary for the right order in the "showing" on the LED strip.
    pix_vec_b_r = pix_vec_back[:b_pixels]
    pix_vec_b_r.reverse()
    pix_vec_b_l = pix_vec_back[b_pixels:]
    pix_vec_b_l.reverse()
    
    vec_vec = [pix_vec_b_r, pix_vec, pix_vec_b_l]
    print(vec_vec)
    
    return vec_vec
