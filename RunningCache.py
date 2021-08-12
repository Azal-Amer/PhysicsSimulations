import time,math,random,json,os
from math import remainder
import vpython as vp
from math import cos,sin,pi
from numpy import arange,array,empty
# Defining the particle class


#Opening the cache
cache = open("SpeedTesting.json")
world = {}

world = json.loads(json.load(cache))
star = vp.sphere(pos=vp.vector(0,0,0), radius=0.2, color=vp.color.yellow,
               mass = 2.0*1000, momentum=vp.vector(0,0,0), make_trail=True)
count = world['Count']
vp.s = empty(count,vp.sphere)
FrameCount = world['FrameCount']
for n in range(count):
   coordinates = (world["frames"][0][n])
   x = float(coordinates[0])
   y = float(coordinates[1])
   z = float(coordinates[2])
   seed = random.randint(0,2)
   if seed == 0: randColor = vp.color.white
   if seed == 1: randColor = vp.color.cyan
   if seed == 2: randColor = vp.color.yellow

   vp.s[n] = vp.sphere(pos = vp.vector(x,y,z), radius = 0.1, color = randColor)
print(FrameCount)
#    To modify the initial momentum vector, change the above value under vp.vector() to whatever force vector you can calculate
for i in range(FrameCount):
    vp.rate(50)
    for n in range(count):
        # the x position of the particle is equal to the "frame"  'i' at the particle 'n's coordinates, at 0 in the coordinate array
        # vp.s[n].pos.x = float(world["frames"][str(i)][str(n)][0])
        coordinates = world["frames"][i][n]
        # print("the cordinates of particle" + str(n) + ' at ' + str(i) + " are : " + str(coordinates))
        vp.s[n].pos.x = float(coordinates[0])
        vp.s[n].pos.y = float(coordinates[1])
        vp.s[n].pos.z = float(coordinates[2])

    
