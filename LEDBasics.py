# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 21:18:46 2019

@author: soenk
"""

"""
show_Leds: Shows the leds in different brightnesses representing different brightnesses. The color stays the same.

show_dim_leds: Shows the leds, with different brightnesses AND a shade of two colors changing when a car comes closer. As example, when a car comes closer, not only will a wider range of LEDs light up and be brighter, they will also have a deeper red, instead of yellow, to potentially increase the warning effect.
"""

def show_LEDs(pixels, led_vector, colors):
    # px_color functions to convert the factor (0 for off, 1 for full brightness) into RGB values representing the relative colors. I don't remember whether the order was actually RGB or RBG, but I think the second.
    def px_red(factor):
        if factor >= 1:
            factor = 1
        # Highest brightness value is 255
        return int(factor * 255), 0, 0
    def px_yellow(factor):
        if factor >= 1:
            factor = 1
        return int(factor * 255), 0, int(factor * 255)

    # Dic with the color options
    color_option = {}
    color_option["red"] = px_red
    color_option["yellow"] = px_yellow
    
    # The three loops are relevant regarding the different parts of the strip and their respective different colors
    pix = 0
    for i in range(len(led_vector[0])):
        pixel_rgb = color_option[colors[1]](led_vector[0][i])
        pixels.set_pixel_rgb(pix, pixel_rgb[0], pixel_rgb[1], pixel_rgb[2])
        pix += 1
    for i in range(len(led_vector[1])):
        pixel_rgb = color_option[colors[0]](led_vector[1][i])
        pixels.set_pixel_rgb(pix, pixel_rgb[0], pixel_rgb[1], pixel_rgb[2])
        pix += 1
    for i in range(len(led_vector[2])):
        pixel_rgb = color_option[colors[1]](led_vector[2][i])
        pixels.set_pixel_rgb(pix, pixel_rgb[0], pixel_rgb[1], pixel_rgb[2])
        pix += 1
    # pixels.clear()
    pixels.show()
    
def show_Dim_LEDs(pixels, led_vector, colors, color_vec):
    #
    def px_yellow_to_red(factor, dist_color):
        if factor >= 1:
            factor = 1
        if dist_color > distances[0]:
            factor_color = 0
        elif dist_color < distances[1]:
            factor_color = 1
        else:
            factor_color = (distances[0] - dist_color) / (distances[0] - distances[1])
        return int(factor * 255), 0, int((1 - factor_color) * factor * 255)
    
    color_option = {}
    color_option["yellow_to_red"] = px_yellow_to_red
        
    # distances represent the start and end point of the intenser color, so at 120m distance "redding" would occur, this would then be at full red at 10m distance.
    distances = [120, 10]
    
    pix = 0
    for i in range(len(led_vector[0])):
        pixel_rgb = color_option[colors[1]](led_vector[0][i], color_vec[0][i])
        pixels.set_pixel_rgb(pix, pixel_rgb[0], pixel_rgb[1], pixel_rgb[2])
        pix += 1
    for i in range(len(led_vector[1])):
        pixel_rgb = color_option[colors[0]](led_vector[1][i], color_vec[1][i])
        pixels.set_pixel_rgb(pix, pixel_rgb[0], pixel_rgb[1], pixel_rgb[2])
        pix += 1
    for i in range(len(led_vector[2])):
        pixel_rgb = color_option[colors[1]](led_vector[2][i], color_vec[2][i])
        pixels.set_pixel_rgb(pix, pixel_rgb[0], pixel_rgb[1], pixel_rgb[2])
        pix += 1
    # pixels.clear()
    pixels.show()
    
