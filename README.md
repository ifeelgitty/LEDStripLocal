# LEDStripLocal

A carefully improvised overview explaining the python-code for a Raspberry Pi controlling any LED Strip in any Driving Simulator - as long as it's a driving sim at the Uni Groningen - and the LED Strip is the specifically setup one there.

The project was never finished due to the then oncoming Covid-Lockdown, so neither is the code streamlined or debugged, nor is it fine-tuned. It is also well-possible that it isn't runnable, as I do not know the state it was in when the lockdown suddenly struck.

## Requirements

- It must run on a Raspberry Pi, I doubt that the exact version matters
- The LED Strip(s) has/have to be WS2801-alike, directly connected to the GPIO
- A UDP connection to the Simulator itself. This was the trickiest part to figure out and required dedicated configuration there, which I do not remember precisely, so whoever takes care of the simulator these days will certainly be able to help you, there was a dedicated script for this somewhere in the project code.
- Packages need to be installed, I do not know exactly the whole list, but it seems like:
    - RPi.GPIO
    - Adafruit_GPIO
    - Adafruit_WS2801
    Just google it, I guess... There are generally quite a few tutorials on the WS2801 online that I borrowed from.

## File Overview

- **SimProc.py**: Vehicle-class-structure to allow saving the respective x and y-coordinates of the car's position, v for the speed, as well as the angle that the vehicle is heading towards. Further, both the distance and the angle relative to the ego car(so, the car of the driver) are computed in an annoying way. The file itself is more or less well-documented. 
- **LEDBasics.py**: Harbors the two basic functions to set the LEDs themselves. **show_LEDs** converts the brightness to specific color values for the LED Strip, while **show_Dim_LEDs**(did I seriously use capital letters in function names? What the heck?) is used to create a light pattern which switches colors the closer one gets to the car. For more details, check the paper and respective file.
- **Main_LED_back.py**: The general script you need to run to control the LED strip. There are also other variations of this script, but I assume they are not only for different patterns (back=back lights shown, noback=no back lights shown etc.), but also not all up to the most current date. However, take them as reference point as you need to. Ultimately, none of these are in a finished state, but the main_led-one is the most current. The script runs an eternal loop, constantly taking in the data from the driving sim over the UDP connection, converting it to the vehicles-data with the relative data of all vehicles, converting it to the led vector, which determines which LEDs light up and then showing them on the LED strip.
- **SimpleLEDPattern_back.py**: Wow, I really followed no naming conventions here... Anyway, It converts the relative angles to positions on the LED strip on which the cars would appear and further convert the distances to how many LEDs surrounding the "central" LED are supposed to light up (and how much they are supposed to light up). The math here is quite chaotic and unintuitive. That is, for once, because I had to compensate for a lot of quirks of the simulator, and the LED strip, but also for the fact that the positioning of the vehicles on screen isn't clearly dividable into angles. The angles depend a lot on the driver's position relative to the screen and LED strip and had to be adjusted as best as possible by doing annoying math. I'm sure there are better solutions to this, though.
