# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 21:18:46 2019

@author: soenk
"""

def show_LEDs(pixels, led_vector, colors):
    def px_red(factor):
        return int(factor * 255), 0, 0
    def px_yellow(factor):
        return int(factor * 255), 0, int(factor * 255)

    
    color_option = {}
    color_option["red"] = px_red
    color_option["yellow"] = px_yellow
    
    pix = 0
    for i in range(len(led_vector[0])):
        pixels.set_pixel_rgb(pix, color_option[colors[1]](led_vector[0][i]))
        pix += 1
    for i in range(len(led_vector[1])):
        pixels.set_pixel_rgb(pix, color_option[colors[0]](led_vector[1][i]))
        pix += 1
    for i in range(len(led_vector[2])):
        pixels.set_pixel_rgb(pix, color_option[colors[1]](led_vector[2][i]))
        pix += 1
    # pixels.clear()
    pixels.show()
    
def show_Dim_LEDs(pixels, led_vector, colors, color_vec):
    
    def px_yellow_to_red(factor, dist_color):
        if dist_color > distances[0]:
            factor_color = 0
        elif dist_color < distances[1]:
            factor_color = 1
        else:
            factor_color = (distances[0] - dist_color) / (distances[0] - distances[1])
        return int(factor * 255), 0, int(factor_color * factor * 255)
    
    color_option = {}
    color_option["yellow_to_red"] = px_yellow_to_red
        
    distances = [60, 5]
    
    pix = 0
    for i in range(len(led_vector[0])):
        pixels.set_pixel_rgb(pix, color_option[colors[1]](led_vector[0][i]))
        pix += 1
    for i in range(len(led_vector[1])):
        pixels.set_pixel_rgb(pix, color_option[colors[0]](led_vector[1][i]))
        pix += 1
    for i in range(len(led_vector[2])):
        pixels.set_pixel_rgb(pix, color_option[colors[1]](led_vector[2][i]))
        pix += 1
    # pixels.clear()
    pixels.show()
    