from vpython import *
import random

# box: object
# size: takes input in vector form (x, y, z)
boxColor = color.blue
wallR = box(pos = vector(5, 0, 0), color = boxColor, size = vector(0.2, 10, 10))
wallL = box(pos = vector(-5, 0, 0), color = boxColor, size = vector(0.2, 10, 10))
wallT = box(pos = vector(0, 5, 0), color = boxColor, size = vector(10, 0.2, 10))
wallBottom = box(pos = vector(0, -5, 0), color = boxColor, size = vector(10, 0.2, 10))
wallBack = box(pos = vector(0, 0, -5), color = boxColor, size = vector(10, 10, 0.2))
wallFront = box(pos = vector(0, 0, 5), color = boxColor, opacity = 0.3, size = vector(10, 10, 0.2))

# pos: for the center position of the object. Takes input in vector form (x, y, z)
# radius: the sphere radius
# color: color of the object
ball = sphere(pos = vector(-3, 0, 0), radius = 0.5, color = color.red)
ball.velocity = vector(2, 1, 1.5)
objects = [ball]

for i in range(100):
    objects.append(ball.clone(pos=vector(random.uniform(-4, 4), random.uniform(-4, 4), random.uniform(-4, 4)),
                                color=vector(random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)))) 
    objects[i+1].velocity = vector(random.uniform(-4, 4), random.uniform(-4, 4), random.uniform(-4, 4))

# Define time interval
t = 0 # time tracker
deltat = 0.05 # increments

ball.pos = ball.pos + ball.velocity * deltat # update ball position

bufferSpace = ball.radius + wallR.size.x

while t < 100:
    rate(50)
    for i in objects:
        if i.pos.x > (wallR.pos.x - bufferSpace) or i.pos.x < (wallL.pos.x + bufferSpace):
            i.velocity.x = -i.velocity.x
        if i.pos.y > (wallT.pos.y - bufferSpace) or i.pos.y < (wallBottom.pos.y + bufferSpace):
            i.velocity.y = -i.velocity.y
        if i.pos.z > (wallFront.pos.z - bufferSpace) or i.pos.z < (wallBack.pos.z + bufferSpace):
            i.velocity.z = -i.velocity.z
        i.pos = i.pos + i.velocity * deltat
    t = t + deltat # update time