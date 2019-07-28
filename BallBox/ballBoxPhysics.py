from vpython import *
import random

def createBox():
    """
    Function to create all the walls for the cube and put them in a dictionary to be returned.
    :param: none
    :returns cube: a dictionary contained the walls of the cube
    """
    cube = {}
    cubeColor = color.blue
    cube["wallR"] = box(pos = vector(5, 0, 0), color = cubeColor, size = vector(0.2, 10, 10))
    cube["wallL"] = box(pos = vector(-5, 0, 0), color = cubeColor, size = vector(0.2, 10, 10))
    cube["wallT"] = box(pos = vector(0, 5, 0), color = cubeColor, size = vector(10, 0.2, 10))
    cube["wallBottom"] = box(pos = vector(0, -5, 0), color = cubeColor, size = vector(10, 0.2, 10))
    cube["wallBack"] = box(pos = vector(0, 0, -5), color = cubeColor, size = vector(10, 10, 0.2))
    cube["wallFront"] = box(pos = vector(0, 0, 5), color = cubeColor, opacity = 0.3, size = vector(10, 10, 0.2))
    return cube

def createBalls(num_balls):
    """
    Function to create the balls with random positions in the box and random velocities
    :param num_balls: integer for the number of balls to be placed
    :returns balls: a list holding all the sphere objects
    """
    balls = []
    ball = sphere(pos = vector(-3, 0, 0), radius = 0.5, color = color.red)
    ball.velocity = vector(2, 1, 1.5)
    balls.append(ball)
    for i in range(num_balls - 1):
        balls.append(ball.clone(pos=vector(random.uniform(-4, 4), random.uniform(-4, 4), random.uniform(-4, 4)),
                                    color=vector(random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)))) 
        balls[i+1].velocity = vector(random.uniform(-4, 4), random.uniform(-4, 4), random.uniform(-4, 4))
    return balls

def calcPositions(balls, box):
    """
    Function for the animation of the balls in the box. The velocity on one axis is reversed based on the wall the ball hits.
    :param balls: list holding the vPython spheres
    :param box: dictionary holding the walls that make up the box
    :returns nothing
    """
    t = 0 # time tracker
    deltat = 0.05 # increments
    bufferSpace = balls[0].radius + box["wallR"].size.x

    while t < 100:
        rate(50)
        for i in balls:
            if i.pos.x > (box["wallR"].pos.x - bufferSpace) or i.pos.x < (box["wallL"].pos.x + bufferSpace):
                i.velocity.x = -i.velocity.x
            if i.pos.y > (box["wallT"].pos.y - bufferSpace) or i.pos.y < (box["wallBottom"].pos.y + bufferSpace):
                i.velocity.y = -i.velocity.y
            if i.pos.z > (box["wallFront"].pos.z - bufferSpace) or i.pos.z < (box["wallBack"].pos.z + bufferSpace):
                i.velocity.z = -i.velocity.z
            i.pos = i.pos + i.velocity * deltat
        t = t + deltat # update time

def main():
    box = createBox()
    balls = createBalls(100)
    calcPositions(balls, box)

if __name__ == "__main__":
    main()