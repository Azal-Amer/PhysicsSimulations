# TODO
# Allow particles to spawn within a given radius and have enough energy to fly out of it
# Cache the physics calculations outside of vpython
# - Beforehand, do a basic check for the amount of time this takes compared to the initial vpython run. 
#   If the calculations run faster than vpython than we know that running the posisions from the file won't 
#   increase the speed, as vpython's 3d is taking up most of the loads
import time,math,random,json,os
from math import remainder
import vpython as vp
from math import cos,sin,pi
import numpy as np
from numpy import arange,array,empty

class Particle:
    def __init__(self,pos,radius,mass,momentum):
        self.pos = pos
        self.radius = radius
        self.mass = mass
        self.momentum= momentum

path_to_script = os.path.dirname(os.path.abspath(__file__))
count = 100
r_Count = range(count)
tolerance = 100
# The leeway on how off the force applied can be compared to the adaquete one of that position
radius = 10
G = 1
FrameCount = 30000
# ORDER OF DATASTRUCTURE= FRAMES -> PARTICLES -> COORDINATES
world = {"Count":count} 
world['FrameCount']= FrameCount

world['frames'] = []

star = Particle(vp.vector(0,0,0),.2,2*1000,vp.vector(0,0,0))

particles = empty(count,Particle)
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
    velocity =  math.sqrt(abs(-2*G*p2.mass*((1/radius**2)-1/distance**2)))
    # print("velocity: " + str(velocity) + ",   kinetic energy: " + str(maxEnergy-currentGPE) + ", maxEnergy : " + str(maxEnergy) + ", currentGPE : " + str(currentGPE))

    dHat = p1.pos / distance
    momentum = p1.mass * velocity * -dHat
    return momentum

for n in r_Count:
   coordinates = randomCords(radius)    
   x = coordinates[0]
   y = coordinates[1]
   z = coordinates[2]
   
   particles[n] = Particle(vp.vector(x,y,z),.1, 1, vp.vector(0,0,0))
   momentum = momentumCalculator(particles[n],star,G,radius)
   particles[n].momentum = momentum
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
run = True
success= 0
i=0
while(run):
   world['frames'].append([])
   start_time = time.time()
   #  particles[n] is a list contaning the planet objects
   n= 0
   count_Run = True
   while(count_Run):
       j = []
       distance = vp.mag(star.pos-particles[n].pos)
       particles[n].force = gravitationalForce(particles[n],star,distance)
       particles[n].momentum = particles[n].momentum + particles[n].force*dt
       #    Momentum = impulse ( f*t)
       particles[n].pos = particles[n].pos + particles[n].momentum/particles[n].mass*dt
       j.append(float(format(particles[n].pos.x,'.3f')))
       j.append(float(format(particles[n].pos.y,'.3f')))
       j.append(float(format(particles[n].pos.z,'.3f')))
    #    j is  a list with size 1xTotalParticles, each index has the corresponding numbered particle's x-y-z positions in another list 
       world['frames'][i].append(j)
    #    i is the frame number. i is a list with each index being another version of j.

       n +=1
       if n == count: count_Run = False
    
   t += dt
   i += 1
   print(i)
   if i==FrameCount:
       run = False
    
# Position in vPython is a vector, need to convert to an array
world['frames'].pop(0)
my_filename = os.path.join(path_to_script, "blender.json")
data = json.dumps(world, indent = 4)
with open(my_filename, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
# Issues: for some reason, its no longer elastic like it should be...

