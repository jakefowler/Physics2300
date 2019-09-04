from vpython import *
import argparse
import pandas as pd
import copy

class SolarSystem:
    def __init__(self, init_pos, init_vel, masses):
        self.createObjects(init_pos, init_vel, masses)
        self.default_objects = copy.deepcopy(self.objects)
        self.createUI()

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
    time = 0

    def createObjects(self, init_pos, init_vel, masses):
        """
        Function to create the vpython spheres for the planets and place them in their initial positions
        The size of the planet will scale with the mass except jupiter and saturn are scaled down.
        :param init_pos: 3d array with x, y, and z coordinates for each planet
        :param masses: mass of each planet in kg
        :return: nothing 
        """
        radius = [2439.7, 6051.8, 6378.1, 3396.2, 71492, 60268, 25559, 24764, 1195]
        colors = [vector(0.5, 0.5, 0.5), vector(1, 0.8, 0.4), color.blue, vector(0.8, 0.1, 0.1), 
                vector(0.7, 0.8, 0.7), vector(1, 0.9, 0.7), vector(0.7, 0.8, 0.8), vector(0.7, 0.8, 1), vector(0.7, 0.6, 0.5)]

        sun = sphere(pos=vector(0, 0, 0), radius=(self.size_scale/75)*695510/self.km_in_au, color=color.yellow, texture=textures.flower, mass=1.99e+30, 
                    velocity=vector(0, 0, 0), name="sun", make_trail=True, retain=200, trail_type="points", trail_radius=0.02) # scaled the sun down
        self.objects.append(sun)

        for i in range(len(masses)):
            self.objects.append(sphere(pos=vector(init_pos[i][0], init_pos[i][1], init_pos[i][2]), radius=self.size_scale*radius[i]/self.km_in_au, 
                            mass=masses[i], velocity=vector(init_vel[i][0], init_vel[i][1], init_vel[i][2]), name=self.object_names[i],
                            color=colors[i], make_trail=True, retain=200, trail_type="points", trail_radius=0.007))
        self.objects[1].texture = textures.rough 
        self.objects[2].texture = textures.rock
        self.objects[3].color=color.white
        self.objects[3].texture=textures.earth # earth
        self.objects[4].texture = textures.stones
        self.objects[5].texture = textures.wood_old # jupiter
        self.objects[5].radius = self.objects[4].radius / 4 # scale down the size of jupiter 
        self.objects[6].radius = self.objects[5].radius / 4 # scale down the size of saturn 
        self.objects[6].texture = textures.wood
        self.objects[8].texture = textures.metal

    def simulateOrbitEulers(self):
        """
        Function to calculate next position of all the objects and draws it.
        :params: none
        :returns: nothing
        """
        while self.time < 3650000000: # days in 10 million years
            if self.running is True:
                rate(100)
                for i in self.objects:
                    i.acceleration = vector(0,0,0)
                    for j in self.objects:
                        if i != j:
                            dist = j.pos - i.pos
                            i.acceleration = i.acceleration + self.G * j.mass * dist / mag(dist)**3
                    i.velocity = i.velocity + i.acceleration*self.dt
                    i.pos = i.pos + i.velocity * self.dt
                self.time += self.dt
                if reset is True:
                    self.resetObjects()
                    reset = False

    def simulateOrbitFrog(self):
        """
        Function that simulates the orbit of the planets using the leap frog method.
        :params: none 
        :returns: nothing
        """
        firstStep = 0
        while self.time < 3650000000: # days in 10 million years
            if self.running is True:
                rate(100)
                for i in self.objects:
                    i.acceleration = vector(0,0,0)
                    for j in self.objects:
                        if i != j:
                            distance = (j.pos - i.pos)
                            i.acceleration = i.acceleration + self.G * j.mass * distance / mag(distance)**3 
                if firstStep == 0:
                    for i in self.objects:
                        i.velocity = i.velocity + i.acceleration*self.dt/2.0
                        i.pos = i.pos + i.velocity*self.dt
                        firstStep = 1
                else:
                    for i in self.objects:
                        i.velocity = i.velocity + i.acceleration*self.dt
                        i.pos = i.pos + i.velocity*self.dt
                self.time += self.dt
                if self.reset is True:
                    self.resetObjects()
                    self.reset = False

    def resetObjects(self):
        """
        Function that changes the planets and sun in the objects list to their default position, velocity, and mass
        :param: none
        :return: nothing
        """
        for def_obj, obj, slider in zip(self.default_objects, self.objects, self.sliders):
            obj.pos = def_obj.pos
            obj.velocity = def_obj.velocity
            obj.mass = def_obj.mass
            slider.value = def_obj.mass
        scene.camera.pos = vector(0, 0, 2)

    def sliderMoved(self, slider):
        """
        Function that gets called when a slider changes. This updates the mass of the object the slider refers to to the value of the slider.
        :param slider: slider object that gets called when a slider changes
        :return: nothing
        """
        print(slider.value)
        for obj in self.objects:
            if obj.name is slider.name:
                obj.mass = slider.value
                break

    def buttonClicked(self, button):
        """
        Function for handling button clicks. The button is passed in and the function changes whether the program should 
        pause, start, or reset based on the button name.
        :param button: button object 
        :returns: nothing
        """
        if button.name is "start":
            self.running = True
        if button.name is "stop":
            self.running = False
        if button.name is "reset":
            self.reset = True

    def createUI(self):
        """
        Function that creates start, stop, and reset buttons and the sliders for each of the planets mass to allow the user to adjust.
        param: nothing
        retunrs: nothing
        """
        scene.append_to_caption('\nDrag the sliders to adjust the mass\n\n')
        for obj in self.objects:
            self.sliders.append(slider(bind=self.sliderMoved, name=obj.name, length=scene.width - 50, max=7557896004349417000000000000000, value=obj.mass))
            scene.append_to_caption(obj.name.capitalize(),'\n\n')
        button(bind=self.buttonClicked, text="Start", name="start", pos=scene.title_anchor)
        button(bind=self.buttonClicked, text="Stop", name="stop", pos=scene.title_anchor)
        button(bind=self.buttonClicked, text="Reset", name="reset", pos=scene.title_anchor)
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

def main():
    """
    Function to get everything going
    """
    filename = parseArguments()
    init_pos, init_vel, masses = readFile(filename) # gets the information out of the file
    solarSystem = SolarSystem(init_pos, init_vel, masses)
    solarSystem.simulateOrbitFrog()

if __name__ == "__main__":
    main()
    