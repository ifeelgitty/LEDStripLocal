# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 21:22:19 2019

@author: soenk
"""


"""
Computing the central LED that has to light up representing the respective car.
veh = Vehicle from the Vehicle-class
step = the angle-"distances" between each pixel
f_pixels = Why is that in there? :D
returns the central pixel as int
"""
def led_position_front(veh, step, LED_DEGREES):
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
    """
    Change Light unsurprisingly changes a light, well, a pixel.
    add_val: value to be added to pixel
    f_pixels: the array of front pixels, to be changed
    led_pos: The CENTRAL pixel of the car-representation
    led_ord: The order of the value, so +- around the central pixel.
    Returns the changed front pixel array
    """
    def change_light(add_val, f_pixels, c_pixels, led_pos, led_ord, dist):
        def change_c_pix(c_pix, pos):
            if c_pix[pos] == 0 or c_pix[pos] > dist:
                c_pix[pos] = dist
            return c_pix
            
        if add_val <= 0:
            return f_pixels, c_pixels
        elif add_val >= 1:
            if led_ord == 0:
                f_pixels[led_pos] = 1
                c_pixels = change_c_pix(c_pixels, led_pos)
                return f_pixels, c_pixels
            else:
                try:
                    f_pixels[led_pos + led_ord] += 1
                    c_pixels = change_c_pix(c_pixels, led_pos + led_ord)
                except IndexError:
                    pass
                try:
                    f_pixels[led_pos - led_ord] += 1
                    c_pixels = change_c_pix(c_pixels, led_pos - led_ord)
                except IndexError:
                    pass
                return f_pixels, c_pixels
        else:
            if led_ord == 0:
                f_pixels[led_pos] += add_val
                c_pixels = change_c_pix(c_pixels, led_pos)
                return f_pixels, c_pixels
            else:
                try:
                    f_pixels[led_pos + led_ord] += add_val
                    c_pixels = change_c_pix(c_pixels, led_pos + led_ord)
                except IndexError:
                    pass
                try:
                    f_pixels[led_pos - led_ord] += add_val
                    c_pixels = change_c_pix(c_pixels, led_pos - led_ord)
                except IndexError:
                    pass
                return f_pixels, c_pixels
            
        
    
    # Noof pixels representing back of car on every side
    b_pixels = 10
    # Noof front pixels can be calculated from all of the parameters
    f_pixels = PIXEL_COUNT - b_pixels * 2
    # Pixel vector for the front pixels
    pix_vec = [0] * f_pixels
    color_vec_f = [0] * f_pixels
    pix_vec_back = [0] * (2 * b_pixels)
    color_vec_b = [0] * (2 * b_pixels)
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
                    pix_vec, color_vec_f = change_light(bright_list[j], pix_vec, color_vec_f, led_c, j)
            else:
                led_c = led_position_back(i, step_back, LED_DEGREES)
                bright_list = []
                for j in led_pref:
                    bright_list.append((j[0] - i.e_d) / (j[0] - j[1]))
                for j in range(len(bright_list)):
                    pix_vec_back, color_vec_b = change_light(bright_list[j], pix_vec_back, color_vec_b, led_c, j)
    
    print(pix_vec_back)
    pix_vec_b_r = pix_vec_back[:b_pixels]
    pix_vec_b_r.reverse()
    pix_vec_b_l = pix_vec_back[b_pixels:]
    pix_vec_b_l.reverse()
    
    color_vec_b_r = color_vec_b[:b_pixels]
    color_vec_b_r.reverse()
    color_vec_b_l = color_vec_b[b_pixels:]
    color_vec_b_l.reverse()
    
    vec_vec = [pix_vec_b_r, pix_vec, pix_vec_b_l]
    col_vec = [color_vec_b_r, color_vec_f, color_vec_b_l]
    print(vec_vec)
    return vec_vec, col_vec