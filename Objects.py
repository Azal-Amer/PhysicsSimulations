from math import remainder
import math
import random
import vpython as vp
from math import cos,sin,pi
from numpy import arange,array,empty
vp.scene.title = "Generating n number of planets in a system"
vp.scene.height = 600
vp.scene.width = 800
count = 50
vp.s = empty(count,vp.sphere)
Planets = {}
# for i in range(1,12):

#    planet = vp.sphere(pos=vp.vector(-1,0,0), radius=0.05, color=vp.color.green,
#                mass = 1, momentum=vp.vector(10,0,0), make_trail=True)
#    Planets.append(planet)
for n in range(count):
   x = random.randint(-5,5)
   y = (random.randint(-5,5))
   z = (random.randint(-5,5))
   print(n)
   vp.s[n] = vp.sphere(radius=.1,pos=vp.vector(x,y,z))
   print(vp.s[n].pos)
print(vp.s)