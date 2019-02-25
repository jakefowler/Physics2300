from vpython import *

# Every variable of size for the table and the legs are based on the table length
# and width. The whole table moves when the tableX , Y, and Z variables are changed.

tableX = 2.5
tableY = -2
tableZ = -1

tableLength = 10
tableWidth = 5
tableTopHeight = tableWidth / tableLength
legLength = tableWidth
legRadius = tableWidth / tableLength

tableTop = box(pos = vector(tableX, tableY, tableZ), color = color.red, size = vector(tableWidth, tableTopHeight, tableLength))
legFrontLeft = cylinder(pos = vector(tableX - (tableWidth / 2) + legRadius, tableY, tableZ + (tableLength / 2) - legRadius), up = vector(1, 0, 0), size = vector(legLength, legRadius, legRadius))
legFrontRight = cylinder(pos = vector(tableX + (tableWidth / 2) - legRadius, tableY, tableZ + (tableLength / 2) - legRadius), up = vector(1, 0, 0), size = vector(legLength, legRadius, legRadius))
legBackLeft = cylinder(pos = vector(tableX - (tableWidth / 2) + legRadius, tableY, tableZ - (tableLength / 2) + legRadius), up = vector(1, 0, 0), size = vector(legLength, legRadius, legRadius))
legBackRight = cylinder(pos = vector(tableX + (tableWidth / 2) - legRadius, tableY, tableZ - (tableLength / 2) + legRadius), up = vector(1, 0, 0), size = vector(legLength, legRadius, legRadius))