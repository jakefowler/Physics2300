from vpython import *
import argparse
import pandas as pd

G = 1.36e-34 # Newton's Gravitational Constant in au^3/kg*s
au = 1.496e+8 # au in kilometers
size_scale = 1000
dt = 1 
objects = []
object_names = ["mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto", "sun"]

def readFile(filename):
    """
    Function to take a filename of a csv file and read it in. Skips the header of the csv file.
    :param filename: file containing the planets name, x, y, z corrdinates in au, velocity in x, y, z in au/day, and mass. 
    :returns init_pos: 3d array holding the initial x, y, and z coordinates for the planets
             init_vel: 3d array holding the initial x, y, and z velocities for the planets
             masses: array holding the masses for each of the planets
    """
    data = pd.read_csv(filename, skiprows=1)
    init_pos = data.iloc[:, 1:4].values
    init_vel = data.iloc[:, 4:7].values
    masses = data.iloc[:, -1].astype('float64').values
    print(data)
    print(masses)
    print(init_pos)
    print(init_vel)
    print(type(init_pos[0][0]))
    print(type(masses[0]))

    return init_pos, init_vel, masses

def createPlanets(init_pos, init_vel, masses):
    """
    Function to create the vpython spheres for the planets and place them in their initial positions
    The size of the planet will scale with the mass except jupiter and saturn are scaled down.
    :param init_pos: 3d array with x, y, and z coordinates for each planet
    :param masses: mass of each planet in kg
    :return: list of vpython spheres representing the planets
    """
    planets = []
    radius = [2439.7, 6051.8, 6378.1, 3396.2, 71492, 60268, 25559, 24764, 1195]
    
    for i in range(len(masses)):
        planets.append(sphere(pos=vector(init_pos[i][0], init_pos[i][1], init_pos[i][2]), radius=size_scale*radius[i]/au, 
                        mass=masses[i], velocity=vector(init_vel[i][0], init_vel[i][1], init_vel[i][2]), name=object_names[i]))
    planets[0].color = vector(0.5, 0.5, 0.5) # mercury
    planets[0].texture = textures.rough 
    planets[1].color = vector(1, 0.8, 0.4) # venus
    planets[1].texture = textures.rock
    planets[2].texture=textures.earth # earth
    planets[3].color = vector(0.8, 0.1, 0.1) # mars
    planets[3].texture = textures.stones
    planets[4].texture = textures.wood_old # jupiter
    planets[4].color = vector(0.7, 0.8, 0.7)
    planets[4].radius = planets[4].radius / 4 # scale down the size of jupiter 
    planets[5].color = vector(1, 0.9, 0.7) # saturn
    planets[5].radius = planets[5].radius / 4 # scale down the size of saturn 
    planets[5].texture = textures.wood
    planets[6].color = vector(0.7, 0.8, 0.8) # uranus
    planets[7].color = vector(0.7, 0.8, 1) # neptune
    planets[7].texture = textures.metal
    planets[8].color = vector(0.7, 0.6, 0.5) # pluto

    return planets

def simulateOrbitEulers(objects):
    """
    Function to calculate next position of all the objects and draw it
    :param objects: list that hods all of the vpython spheres
    :returns: nothing
    """
    t = 0
    while t < 3650000000: # days in 10 million years
        rate(100)
        for i in objects:
            i.acceleration = vector(0,0,0)
            for j in objects:
                if i != j:
                    dist = j.pos - i.pos
                    i.acceleration = i.acceleration + G * j.mass * dist / mag(dist)**3
            i.velocity = i.velocity + i.acceleration*dt
            i.pos = i.pos + i.velocity * dt
        t += dt

def simulateOrbitFrog(objects):
    """
    Function that simulates the orbit of the planets using the leap frog method
    :param objects: list that holds all of the vpython spheres 
    :returns: nothing
    """
    firstStep = 0
    t = 0
    while t < 3650000000: # days in 10 million years
        rate(100)
        for i in objects:
            i.acceleration = vector(0,0,0)
            for j in objects:
                if i != j:
                    distance = (j.pos - i.pos)
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

def sliderMoved(slider):
    """
    Function that gets called when a slider changes. This updates the mass of the object the slider refers to to the value of the slider.
    :param slider: slider object that gets called when a slider changes
    :return: nothing
    """
    print(slider.value)
    for obj in objects:
        if obj.name is slider.name:
            obj.mass = slider.value

def createSliders():
    """
    Function that creates the sliders for each of the planets mass to allow the user to adjust.
    param: nothing
    retunrs: nothing
    """
    global objects
    scene.append_to_caption('\nDrag the sliders to adjust the mass\n\n')
    for obj in objects:
        slider( bind=sliderMoved, name=obj.name, length=scene.width - 40, max=2e+31, value=obj.mass)
        scene.append_to_caption(obj.name.capitalize(),'\n\n')
    
def parseArguments():
    """
    Function that parses the arguments and returns the filename entered. If no filename was entered it gives the default one.
    :param: none
    :returns filename: string of filename
    """
    parser = argparse.ArgumentParser(description="Solar System Simulation")
    parser.add_argument("--file", "-f", action="store", dest="filename", type=str, required=False, 
        help="Filename for csv file containing the planets name, x, y, z corrdinates in au, velocity in x, y, z in au/day, and mass. \
        File should be in the same directory or include the filepath. The header is skipped when read in.")
    args = parser.parse_args()
    filename = args.filename
    if not filename:
        filename = "solar_system_points.csv"

    return filename

def main():
    """
    Function to create the argument parser and get everything going
    """
    global objects
    filename = parseArguments()
    init_pos, init_vel, masses = readFile(filename) # gets the information out of the file

    objects = createPlanets(init_pos, init_vel, masses) # adds all the data to the vpython objects when creating them
    sun = sphere(pos=vector(0, 0, 0), radius=(size_scale/75)*695510/au, color=color.yellow, texture=textures.flower, mass=1.99e+30, velocity=vector(0, 0, 0), name="sun") # scaled the sun down
    objects.append(sun)
    createSliders()
    simulateOrbitFrog(objects)
    simulateOrbitEulers(objects)

if __name__ == "__main__":
    main()
    