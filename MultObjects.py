# TODO
# Allow particles to spawn within a given radius and have enough energy to fly out of it
# Cache the physics calculations outside of vpython
# - Beforehand, do a basic check for the amount of time this takes compared to the initial vpython run. 
#   If the calculations run faster than vpython than we know that running the posisions from the file won't 
#   increase the speed, as vpython's 3d is taking up most of the loads
import time
from math import remainder
import math
import vpython as vp
import random
from math import cos,sin,pi
from numpy import arange,array,empty
vp.scene.title = "Modeling the motion of planets with the gravitational force"  
vp.scene.height = 600
vp.scene.width = 800
count = 10000
tolerance = 100
# The leeway on how off the force applied can be compared to the adaquete one of that position
radius = 10
G = 1


star = vp.sphere(pos=vp.vector(0,0,0), radius=0.2, color=vp.color.yellow,
               mass = 2.0*1000, momentum=vp.vector(0,0,0), make_trail=True)
# checker = vp.sphere(pos= vp.vector(0,0,0),radius = radius-1, color = vp.color.)
vp.s = empty(count,vp.sphere)
def randomCords(radius):
    cord_X = random.uniform(-radius,radius)


    side_Z = bool(random.getrandbits(1))
    side_Y = bool(random.getrandbits(1))
    
    
    cord_Y = random.uniform(0,math.sqrt(radius**2-(cord_X**2)))
    #Would have used the randint function with an upper bound of y = sqrt(r^2-x^2), but then that removed chances at negative points
    cord_Z = random.uniform(0,math.sqrt(abs(radius**2-cord_X**2-cord_Y**2)))
    # cord_Z = math.sqrt(abs(radius**2-cord_X**2-cord_Y**2))

    if side_Z:
        cord_Z= cord_Z*-1
    if side_Y:
        cord_Y = cord_Y*-1
    return cord_X,cord_Y,cord_Z
def momentumCalculator(p1,p2,G,radius):
    # p1 is particle
    # p2 is star/ large mass
    # G is gravitaitonal constant
    # radius is the radius of the sphere 
    # distance is the spawned distance
    # dHat is the displacement vector
    distance = vp.mag(p1.pos)
    maxEnergy = -(p1.mass*G*p2.mass)/radius
    # GPE = mass * acceleration * height
    currentGPE = -(p1.mass*G*p2.mass)/distance
    # print("---------------------------")
    # velocity = math.sqrt(2*(maxEnergy-currentGPE)/p1.mass)
    velocity =  math.sqrt(-2*G*p2.mass*((1/radius**2)-1/distance**2))
    # print("velocity: " + str(velocity) + ",   kinetic energy: " + str(maxEnergy-currentGPE) + ", maxEnergy : " + str(maxEnergy) + ", currentGPE : " + str(currentGPE))

    dHat = p1.pos / distance
    momentum = p1.mass * velocity * -dHat
    return momentum

for n in range(count):
   coordinates = randomCords(radius)    
   x = coordinates[0]
   y = coordinates[1]
   z = coordinates[2]
   
   vp.s[n] = vp.sphere(radius=.1,pos=vp.vector(x,y,z),mass = 1, momentum = vp.vector(0,0,0), make_trail = False, motion = True)
#    print(str(n)  + "- " + "distance : " + str(vp.mag(vp.s[n].pos)) + ", radius: " + str(radius) )

   momentum = momentumCalculator(vp.s[n],star,G,radius)

   vp.s[n].momentum = momentum
   

#    To modify the initial momentum vector, change the above value under vp.vector() to whatever force vector you can calculate


def gravitationalForce(p1,p2,distance):
   rVector = p1.pos - p2.pos 
   rMagnitude = vp.mag(rVector)
   rHat = rVector / rMagnitude
   # above is the direction
  
   F =  - rHat * G * p1.mass * p2.mass /rMagnitude**2
   acceleration =( G*p2.mass)/(distance**2)
   maxForce = p1.mass * math.sqrt(2*acceleration*rMagnitude)
   currentVelocity = (abs(vp.mag(F/p1.mass)))
   if   ((currentVelocity > maxForce+tolerance)  or (currentVelocity < maxForce-tolerance)):
    #   print("trigger")
      F = -  rHat * math.sqrt(2*acceleration*rMagnitude) * p1.mass
      #DIFFERENT G'S MORON, ONE IS THE GRAVITATIONAL ACCELERATION, OTHER IS FOR PLANET
    #   print(F)
   return F
t = 0
dt = 0.0001
vp.graph(xtitle = "radius", ytitle = "momentum")
mmnt_curve =vp.gdots(color= vp.color.blue) 
run = True
success= 0
while(run):
   vp.rate(500)
   start_time = time.time()
    #Calculte the force using gravitationalForce function
#  vp.s[n] is a list contaning the planet objects
   for n in range(count):
       distance = vp.mag(star.pos-vp.s[n].pos)

       vp.s[n].force = gravitationalForce(vp.s[n],star,distance)
       vp.s[n].momentum = vp.s[n].momentum + vp.s[n].force*dt
       mmnt_curve.plot(time.time(), vp.mag(vp.s[n].pos))
       #    Momentum = impulse ( f*t)
       vp.s[n].pos = vp.s[n].pos + vp.s[n].momentum/vp.s[n].mass*dt
       if distance >= 9.5: 
           vp.s[n].color = vp.color.red

#    print("FPS: ", 1.0 / (time.time() - start_time)) # FPS = 1 / time to process loop

   t += dt
   k = vp.keysdown()
   
   if 'down' in k : 
       run = False
       print("# of Balls At radius: " + str(success))
       print( "SUCESSS RATE: " + str((success/count)*100))
   

# Issues: for some reason, its no longer elastic like it should be...
# DOWN ARROW IS SHUTDOWN

