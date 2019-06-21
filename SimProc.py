# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 21:09:32 2019

@author: soenk
"""

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


def preproc(dat):
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
    
    vehicles = format_string(str(dat))
    vehicles = transposing_vehicles(vehicles)
    vehicles = dist_to_ego(vehicles)
    vehicles = angle_to_ego(vehicles)
    return vehicles