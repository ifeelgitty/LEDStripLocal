# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 21:18:46 2019

@author: soenk
"""



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