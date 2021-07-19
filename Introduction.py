from math import remainder
import math
import vpython as vp
import random
vp.scene.title = "Modeling the motion of planets with the gravitational force"
vp.scene.height = 600
vp.scene.width = 800
randomMomentum = random.randint(30,100)

star = vp.sphere(pos=vp.vector(0,0,0), radius=0.2, color=vp.color.yellow,
               mass = 2.0*10000, momentum=vp.vector(0,0,0), make_trail=True)
planet1 = vp.sphere(pos=vp.vector(-1,0,0), radius=0.05, color=vp.color.green,
               mass = 1, momentum=vp.vector(10,0,0), make_trail=True)
planet2 = vp.sphere(pos=vp.vector(0,-1,0), radius=0.05, color=vp.color.green,
               mass = 1, momentum=vp.vector(0,-10,0), make_trail=True)

G = 1
distance = vp.mag(star.pos-planet1.pos)
totalEnergy = planet1.mass * G * distance

distanceVector = (star.pos - planet1.pos) / distance 
def gravitationalForce(p1,p2):
   rVector = p1.pos - p2.pos 
   rMagnitude = vp.mag(rVector)
   rHat = rVector / rMagnitude
   # above is the direction
  
   F =  - rHat * G * p1.mass * p2.mass /rMagnitude**2
   print(F)
   acceleration =( G*p2.mass)/(distance**2)
   if (vp.mag(F/p1.mass)) > p1.mass * math.sqrt(2*acceleration*rMagnitude):
      print("trigger")
      F = -  rHat * math.sqrt(2*acceleration*rMagnitude) * p1.mass
      #DIFFERENT G'S MORON, ONE IS THE GRAVITATIONAL ACCELERATION, OTHER IS FOR PLANET
      print(F)
   return F
t = 0
dt = 0.001
# for i in range (1000):
while(True):
   vp.rate(500)
 
    #Calculte the force using gravitationalForce function
   # star.force = gravitationalForce(star,planet1)
   planet1.force = gravitationalForce(planet1,star)
   planet2.force = gravitationalForce(planet2,star)

    #Update momentum, position and time
   # star.momentum = star.momentum + star.force*dt
   planet1.momentum = planet1.momentum + planet1.force*dt
   planet2.momentum = planet2.momentum + planet2.force*dt
   # star.pos = star.pos + star.momentum/star.mass*dt
   planet1.pos = planet1.pos + planet1.momentum/planet1.mass*dt
   planet2.pos = planet2.pos + planet2.momentum/planet2.mass*dt
   t += dt