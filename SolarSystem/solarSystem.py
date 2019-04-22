from vpython import *
import argparse
import pandas as pd
import copy

G = 1.36e-34 # Newton's Gravitational Constant in au^3/kg*s
km_in_au = 1.496e+8 # number of kilometers in one au
size_scale = 1000
dt = 0.5 
objects = []
default_objects = []
sliders = [] # used to store sliders in the ui to make it easier to change when reset button is clicked
object_names = ["mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto", "sun"]
running = True
reset = False

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

def createObjects(init_pos, init_vel, masses):
    """
    Function to create the vpython spheres for the planets and place them in their initial positions
    The size of the planet will scale with the mass except jupiter and saturn are scaled down. Saves planets 
    in global variable objects so the masses can be changed with sliders in ui while calculating position of each planet.
    :param init_pos: 3d array with x, y, and z coordinates for each planet
    :param masses: mass of each planet in kg
    :return: nothing 
    """
    global objects
    radius = [2439.7, 6051.8, 6378.1, 3396.2, 71492, 60268, 25559, 24764, 1195]

    sun = sphere(pos=vector(0, 0, 0), radius=(size_scale/75)*695510/km_in_au, color=color.yellow, texture=textures.flower, mass=1.99e+30, 
                 velocity=vector(0, 0, 0), name="sun", make_trail=True, retain=200, trail_type="points", trail_radius=0.02) # scaled the sun down
    objects.append(sun)

    for i in range(len(masses)):
        objects.append(sphere(pos=vector(init_pos[i][0], init_pos[i][1], init_pos[i][2]), radius=size_scale*radius[i]/km_in_au, 
                        mass=masses[i], velocity=vector(init_vel[i][0], init_vel[i][1], init_vel[i][2]), name=object_names[i],
                        make_trail=True, retain=200, trail_type="points", trail_radius=0.02))
    objects[1].color = vector(0.5, 0.5, 0.5) # mercury
    objects[1].texture = textures.rough 
    objects[2].color = vector(1, 0.8, 0.4) # venus
    objects[2].texture = textures.rock
    objects[3].texture=textures.earth # earth
    objects[4].color = vector(0.8, 0.1, 0.1) # mars
    objects[4].texture = textures.stones
    objects[5].texture = textures.wood_old # jupiter
    objects[5].color = vector(0.7, 0.8, 0.7)
    objects[5].radius = objects[4].radius / 4 # scale down the size of jupiter 
    objects[6].color = vector(1, 0.9, 0.7) # saturn
    objects[6].radius = objects[5].radius / 4 # scale down the size of saturn 
    objects[6].texture = textures.wood
    objects[7].color = vector(0.7, 0.8, 0.8) # uranus
    objects[8].color = vector(0.7, 0.8, 1) # neptune
    objects[8].texture = textures.metal
    objects[9].color = vector(0.7, 0.6, 0.5) # pluto

def simulateOrbitEulers():
    """
    Function to calculate next position of all the objects and draw it
    :params: none
    :returns: nothing
    """
    global objects, running, reset, default_objects
    t = 0
    while t < 3650000000: # days in 10 million years
        if running is True:
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
            if reset is True:
                resetObjects()
                reset = False

def simulateOrbitFrog():
    """
    Function that simulates the orbit of the planets using the leap frog method. Uses the global variables objects, running,
    reset, and default_objects to make it easier to change the mass with the slider, calculate positions, pause, and start.
    :params: none 
    :returns: nothing
    """
    global objects, running, reset, default_objects
    firstStep = 0
    t = 0
    while t < 3650000000: # days in 10 million years
        if running is True:
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
            t += dt
            if reset is True:
                resetObjects()
                reset = False


def resetObjects():
    """
    Function that changes the planets and sun in the objects list to their default position, velocity, and mass
    :param: none
    :return: nothing
    """
    global objects, default_objects, sliders
    for def_obj, obj, slider in zip(default_objects, objects, sliders):
        obj.pos = def_obj.pos
        obj.velocity = def_obj.velocity
        obj.mass = def_obj.mass
        slider.value = def_obj.mass
    scene.camera.pos = vector(0, 0, 10)

def sliderMoved(slider):
    """
    Function that gets called when a slider changes. This updates the mass of the object the slider refers to to the value of the slider.
    :param slider: slider object that gets called when a slider changes
    :return: nothing
    """
    global objects
    print(slider.value)
    for obj in objects:
        if obj.name is slider.name:
            obj.mass = slider.value
            break

def buttonClicked(button):
    """
    Function for handling button clicks. The button is passed in and the function changes whether the program should 
    pause, start, or reset based on the button name.
    :param button: button object 
    :returns: nothing
    """
    global running, reset
    if button.name is "start":
        running = True
    if button.name is "stop":
        running = False
    if button.name is "reset":
        reset = True

def createUI():
    """
    Function that creates start, stop, and reset buttons and the sliders for each of the planets mass to allow the user to adjust.
    param: nothing
    retunrs: nothing
    """
    global objects, sliders
    scene.append_to_caption('\nDrag the sliders to adjust the mass\n\n')
    for obj in objects:
        sliders.append(slider( bind=sliderMoved, name=obj.name, length=scene.width - 50, max=7557896004349417000000000000000, value=obj.mass))
        scene.append_to_caption(obj.name.capitalize(),'\n\n')
    button( bind=buttonClicked, text="Start", name="start", pos=scene.title_anchor)
    button( bind=buttonClicked, text="Stop", name="stop", pos=scene.title_anchor)
    button( bind=buttonClicked, text="Reset", name="reset", pos=scene.title_anchor)
    scene.append_to_caption('\nRight button drag or Ctrl-drag to rotate "camera" to view scene.\n'
                            'To zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.\n'
                            'On a two-button mouse, middle is left + right.\n'
                            'Shift-drag to pan left/right and up/down.\n'
                            'Touch screen: pinch/extend to zoom, swipe or two-finger rotate.\n\n')
    
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
    Function to get everything going
    """
    global objects, default_objects
    filename = parseArguments()
    init_pos, init_vel, masses = readFile(filename) # gets the information out of the file
    createObjects(init_pos, init_vel, masses) # adds all the data to the vpython objects when creating them
    default_objects = copy.deepcopy(objects)
    createUI()
    simulateOrbitFrog()
    simulateOrbitEulers()

if __name__ == "__main__":
    main()
    