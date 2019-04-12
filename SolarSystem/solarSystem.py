from vpython import *
import numpy as np
from matplotlib import pyplot as plt
import argparse
import csv
import pandas as pd

G = 6.6738e-11          # Newton's Gravitational Contant 
au = 1.496e+8 # au in kilometers
sizeScale = 1000
dt = 6.3e-12


def readFile(filename):
    """
    Function to take a filename of a csv file and read it in. Skips the header of the csv file.
    :param filename: file containing the planets name, x, y, z corrdinates in au, velocity in x, y, z in au/day, and mass. 
    :returns: nothing
    """
    data = pd.read_csv(filename, skiprows=1)
    initPos = data.iloc[:, 1:4].values
    initVel = data.iloc[:, 4:7].values
    masses = data.iloc[:, -1].astype('float64').values
    print(data)
    print(masses)
    print(initPos)
    print(initVel)
    print(type(initPos[0][0]))
    print(type(masses[0]))

    return initPos, initVel, masses

def createPlanets(initPos, initVel, masses):
    """
    Function to create the vpython spheres for the planets and place them in their initial positions
    The size of the planet will scale with the mass.
    :param initPos: 3d array with x, y, and z coordinates for each planet
    :param masses: masss of each planet in kg
    :return: list of vpython spheres representing the planets
    """
    planets = []
    radius = [2439.7, 6051.8, 6378.1, 3396.2, 71492, 60268, 25559, 24764, 1195]
    
    for i in range(len(masses)):
        planets.append(sphere(pos=vector(initPos[i][0], initPos[i][1], initPos[i][2]), radius=sizeScale*radius[i]/au, 
                        mass=masses[i], velocity=vector(initVel[i][0], initVel[i][1], initVel[i][2]), texture=textures.earth))
        #planets[2].texture=textures.earth
    return planets

def simulateOrbitEulers(objects, initVel, masses):
    """
    Function to calculate next position of all the objects and draw it
    """
    while True:
        for i in objects:
            rate(100)
            i.acceleration = vector(0,0,0)
            for j in objects:
                if i != j:
                    dist = j.pos - i.pos
                    i.acceleration = i.acceleration + G * j.mass * dist / mag(dist)**3
        for i in objects:
            i.velocity = i.velocity + i.acceleration*dt
            i.pos = i.pos + i.velocity * dt

def simulateOrbitFrog(objects):
    firstStep = 0
    while True:
        rate(1000)
        for i in objects:
            i.acceleration = vector(0,0,0)
            for j in objects:
                if i != j:
                    distance = j.pos - i.pos
                    i.acceleration = i.acceleration + G * j.mass * distance / mag(distance)**3
        if firstStep == 0:
            for i in objects:
                i.velocity = i.velocity + i.acceleration*dt/2.0
                i.pos = i.pos + i.velocity*dt
                firstStep = 1
        else:
            for i in objects:
                i.velocity = i.velocity + i.acceleration*dt
                i.pos = i.pos + i.velocity*dt

def main():
    parser = argparse.ArgumentParser(description="Solar System Simulation")

    parser.add_argument("--file", "-f", action="store", dest="filename", type=str, required=False, 
        help="Filename for csv file containing the planets name, x, y, z corrdinates in au, velocity in x, y, z in au/day, and mass. \
        File should be in the same directory or include the filepath.")
    args = parser.parse_args()
    filename = args.filename
    if not filename:
        filename = "solar_system_points.csv"

    initPos, initVel, masses = readFile(filename)

    objects = createPlanets(initPos, initVel, masses)
    sun = sphere(pos=vector(0, 0, 0), radius=(sizeScale/100)*695510/au, color=color.yellow, mass=1.99e+30, velocity=vector(0, 0, 0)) # scaled the sun down
    objects.append(sun)
    initVel = list(initVel).append([0, 0, 0]) # add the sun to the velocity list
    masses = list(masses).append(1.99e+30) # add the mass of the sun to the array

    simulateOrbitFrog(objects)



if __name__ == "__main__":
    main()
    