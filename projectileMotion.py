"""
Jacob Fowler
2/4/2019
"""

import numpy as np
import math as m
import matplotlib.pyplot as plt

def get_user_input():
    """
    Function to get the initial x and y velocity from the user.
    Input from the user needs to be a float.
    returns the x and y velocity that the user entered.
    """
    x_velocity = float(input("Please enter the initial horizontal velocity: "))
    y_initial_velocity = float(input("Please enter the initial vertical velocity: "))
    return x_velocity, y_initial_velocity

def calculate_x_coordinate(x_velocity, time):
    """
    Function to calculate the horizontal projectile motion.
    Param: x_velocity -> velocity in the x direction
           time -> how long the projectile has been traveling 
    Returns the calculation of the current velocity in the x direction.
    """
    return x_velocity * time 

def calculate_y_coordinate(y_initial_velocity, time, gravity = 9.8):
    """
    Function to calculate the vertical projectile motion.
    Param: y_initial_velocity -> the velocity at the start
           time -> how long the projectile has been traveling
           gravity -> what is the acceleration of gravity in this environment? Defaults to -9.8. 
    Returns the calculation of the current velocity in the y direction.
    """
    return ((y_initial_velocity * time) - (0.5 * gravity * (time * time)))

def generate_list_coordinates(x_velocity, y_initial_velocity, gravity = 9.8):
    """
    Function to pass the data to the calculate_projectile function and populate the x and y lists
    with the data.
    This increments the time and loops until the projectile has a y coordinate of 0.
    Param: x_velocity -> the velocity in the x direction
           y_initial_velocity -> the initial velocity in the y direction
           gravity -> what is the acceleration of gravity in this environment? Defaults to -9.8. 
    Returns a list for all the x coordinates and a list for all the y coordinates
    """
    # list to hold all the x coordinates
    x_coordinates = []
    # list to hold all the y coordinates
    y_coordinates = []
    # deltat is the jump in time that each loop will make to increment the coordinates.
    deltat = 0.1
    # variable for time
    t = 0.0
    while(True):
        y_temp = calculate_y_coordinate(y_initial_velocity, t)
        if y_temp > -0.001:
            y_coordinates.append(y_temp)
        else:
            break
        x_coordinates.append(calculate_x_coordinate(x_velocity, t))
        t = t + deltat
    return x_coordinates, y_coordinates

def plot_graph(x_coordinates, y_coordinates):
    """
    Function that a graph of the two lists received.
    Param: x_coordinates -> a list of the x coordinates
           y_coordinates -> a list of the y coordinates
    """
    plt.plot(x_coordinates, y_coordinates)
    plt.show()

def main():
    """
    Function that gets everything going.
    """
    x_velocity, y_initial_velocity = get_user_input()
    x_coordinates, y_coordinates = generate_list_coordinates(x_velocity, y_initial_velocity)
    plot_graph(x_coordinates, y_coordinates)

if __name__ == "__main__":
    main()

