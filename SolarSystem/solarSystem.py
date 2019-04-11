from vpython import *
import numpy as np
from matplotlib import pyplot as plt
import argparse
import csv
import pandas as pd

def readFile(filename):
    """
    Function to take a filename of a csv file and read it in. Skips the header of the csv file.
    :param filename: file containing the planets name, x, y, z corrdinates in au, velocity in x, y, z in au/day, and mass. 
    :returns: nothing
    """
    data = pd.read_csv(filename, skiprows=1)
    masses = data.iloc[:, -1].values
    initPos = data.iloc[:, 1:4].values
    initVel = data.iloc[:, 4:7].values
    print(data)
    print(masses)
    print(type(masses))
    print(initPos)
    print(initVel)

def main():
    parser = argparse.ArgumentParser(description="Solar System Simulation")

    parser.add_argument("--file", "-f", action="store", dest="filename", type=float, required=False, 
        help="Filename for csv file containing the planets name, x, y, z corrdinates in au, velocity in x, y, z in au/day, and mass. \
        File should be in the same directory or include the filepath.")

    #filename = args.filename
 #  if filename != null:
 #      readFile(filename)
 #  else:
    readFile("solar_system_points.csv")

if __name__ == "__main__":
    main()
    