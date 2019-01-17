from vpython import *
# pos: for the center position of the object. Takes input in vector form (x, y, z)
# radius: the sphere radius
# color: color of the object
ball = sphere(pos = vector(-3, 0, 0), radius = 0.5, color = color.red)
# box: object
# size: takes input in vector form (x, y, z)
boxColor = color.blue
wallR = box(pos = vector(5, 0, 0), color = color.blue, size = vector(0.2, 10, 10))
wallL = box(pos = vector(-5, 0, 0), color = color.blue, size = vector(0.2, 10, 10))
wallT = box(pos = vector(0, 5, 0), color = color.blue, size = vector(10, 0.2, 10))
wallBottom = box(pos = vector(0, -5, 0), color = color.blue, size = vector(10, 0.2, 10))
wallBack = box(pos = vector(0, 0, -5), color = color.blue, size = vector(10, 10, 0.2))
wallFront = box(pos = vector(0, 0, 5), color = color.blue, opacity = 0.3, size = vector(10, 10, 0.2))

ball.velocity = vector(2, 1, 1.5)
# Define time interval
t = 0 # time tracker
deltat = 0.05 # increments

ball.pos = ball.pos + ball.velocity * deltat # update ball position

bufferSpace = ball.radius + wallR.size.x

while t < 100:
    rate(50)
    if ball.pos.x > (wallR.pos.x - bufferSpace) or ball.pos.x < (wallL.pos.x + bufferSpace):
        ball.velocity.x = -ball.velocity.x
    if ball.pos.y > (wallT.pos.y - bufferSpace) or ball.pos.y < (wallBottom.pos.y + bufferSpace):
        ball.velocity.y = -ball.velocity.y
    if ball.pos.z > (wallFront.pos.z - bufferSpace) or ball.pos.z < (wallBack.pos.z + bufferSpace):
        ball.velocity.z = -ball.velocity.z
    ball.pos = ball.pos + ball.velocity * deltat
    t = t + deltat # update time
    # Trying out github push