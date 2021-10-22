# TODO
# Allow particles to spawn within a given radius and have enough energy to fly out of it
# Cache the physics calculations outside of vpython
# - Beforehand, do a basic check for the amount of time this takes compared to the initial vpython run. 
#    If the calculations run faster than vpython than we know that running the posisions from the file won't 
#    increase the speed, as vpython's 3d is taking up most of the loads
import time
from math import remainder
import math
import numpy as np
import vpython as vp
import random,os,csv
from math import cos,sin,pi
from numpy import arange,array,empty
import importlib.util

spec = importlib.util.spec_from_file_location("RandomMB", "Gas Dynamics\\randomMB.py")
gas = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gas)

vp.scene.title = "Modeling the motion of planets with the gravitational force"  
vp.scene.height = 600
vp.scene.width = 800
count = 10
tolerance = 1
# The leeway on how off the force applied can be compared to the adaquete one of that position
radius = 10
inner_Radius = 3
FrameCount = 30000
velocityMB = gas.randomMB(40,count)[0]

vp.graph(xtitle = "distance", ytitle = "momentum")
mmnt_curve =vp.gdots(color= vp.color.blue) 
G = 1
b = open('output.csv', 'w')
a = csv.writer(b)
points = []
chance = .01
star = vp.sphere(pos=vp.vector(0,0,0), radius=0.2, color=vp.color.yellow,
                    mass = 2.0*1000, momentum=vp.vector(0,0,0), make_trail=True)
# checker = vp.sphere(pos= vp.vector(0,0,0),radius = radius-1, color = vp.color.)
vp.s = empty(count,vp.sphere)
def randomCords(radius):
    cord_X = random.uniform(-radius,radius)
    cord_Y = random.uniform(-math.sqrt(radius**2-(cord_X**2)),math.sqrt(radius**2-(cord_X**2)))
    #Would have used the randint function with an upper bound of y = sqrt(r^2-x^2), but then that removed chances at negative points
    cord_Z = random.uniform(-math.sqrt(abs(radius**2-cord_X**2-cord_Y**2)),math.sqrt(abs(radius**2-cord_X**2-cord_Y**2)))
    # cord_Z = math.sqrt(abs(radius**2-cord_X**2-cord_Y**2))

    # if side_Z:
    #      cord_Z= cord_Z*-1
    # if side_Y:
    #      cord_Y = cord_Y*-1
    return cord_X,cord_Y,cord_Z
def vectorSplit(radius):
     cord_X = random.uniform(-radius,radius)
     cord_Y = random.uniform(-math.sqrt(radius**2-(cord_X**2)),math.sqrt(radius**2-(cord_X**2)))
     #Would have used the randint function with an upper bound of y = sqrt(r^2-x^2), but then that removed chances at negative points
     cord_Z = math.sqrt(abs(radius**2-cord_X**2-cord_Y**2))*random.choice([-1,1])
     # cord_Z = math.sqrt(abs(radius**2-cord_X**2-cord_Y**2))
     return cord_X,cord_Y,cord_Z
# Above implementation, while effective, had a non-uniform distribution of points, biased toward the outside

# New random point grabber rewritten from https://karthikkaranth.me/blog/generating-random-points-in-a-sphere/
# Seemed to be a similar concept to ray tracing
# This implementation works in a polar system, to read more about it, look here https://mathworld.wolfram.com/SpherePointPicking.html



def momentumCalculator(p1,p2,G,radius):
    # p1 is particle
    # p2 is star/ large mass
    # G is gravitaitonal constant
    # radius is the radius of the sphere 
    # distance is the spawned distance
    # dHat is the displacement vector
    distance = p1.pos-p2.pos
    # GPE = mass * acceleration * height
    # print("---------------------------")
    # az-timmy
    A = -5.603
    B = -21.17
    C = 86.94
    distanceMag = math.sqrt(p1.pos.x**2+p1.pos.y**2+p1.pos.z**2)
    # Above variables are just from a fit curve of the changing momentum of the real particle
    pos = abs(distanceMag)
    velocity =  math.sqrt(-2*G*p2.mass*((1/radius)- (1/distanceMag)))
    dHat = distance / distanceMag
    if abs(distanceMag) <tolerance:
        velocity = A*(pos**2) + B*pos + C
    sign = random.randint(0,1)
    if(sign == 1): sign = -1
    if(sign == 0):sign = 1
    
    momentum = sign*p1.mass * velocity * dHat

    return momentum

  
for n in range(count):
    randomVelocityMBIndex = np.random.random_integers(0,count-1)
    coordinates = randomCords(radius)     
    x = coordinates[0]
    y = coordinates[1]
    z = coordinates[2]
    start = random.randint(0,FrameCount/3)
    vp.s[n] = vp.sphere(radius=.1,pos=vp.vector(x,y,z),mass = 1, momentum = 0, make_trail = False, motion = True,startFrame = start, MB =vectorSplit(velocityMB[randomVelocityMBIndex]))

    vp.s[n].momentum = momentumCalculator(vp.s[n],star,G,radius)
    
# for n in range(count):

    
#     vp.s[n] = vp.sphere(radius=.1,pos=vp.vector(0,((n)/10)+.1,0),mass = 1, momentum = vp.vector(0,0,0), make_trail = False, motion = True)
#     # vp.s[n] = vp.sphere(radius=.1,pos=vp.vector(0,radius,0),mass = 1, momentum = vp.vector(0,0,0), make_trail = False, motion = True)



#     vp.s[n].momentum = momentumCalculator(vp.s[n],star,G,radius)
#     #     To modify the initial momentum vector, change the above value under vp.vector() to whatever force vector you can calculate


def gravitationalForce(p1,p2):
    rVector = p1.pos - p2.pos 
    #rMagnitude = vp.mag(rVector)
    rMagnitude = ((rVector.x**2) + (rVector.y**2) + (rVector.z**2))
    rHat = rVector / math.sqrt(rMagnitude)
    # print("self calc: " + str(rHat) + " vs vPython : " + str(rVector/ vp.mag(rVector)))
    # above is the direction
    if abs(vp.mag(p1.pos)) < tolerance:
        F_i = - rHat * G * p1.mass * p2.mass /(tolerance)**2
    else:
        F_i =  - rHat * G * p1.mass * p2.mass /rMagnitude
    F = [F_i.x,F_i.y,F_i.z]
      #DIFFERENT G'S MORON, ONE IS THE GRAVITATIONAL ACCELERATION, OTHER IS FOR PLANET
      
    return F
t = 0
dt = 0.0001
run = True
success= 0
i = 0
while(True):
    start_time = time.time()
    #Calculte the force using gravitationalForce function
    #  vp.s[n] is a list contaning the planet objects
    vp.rate(500)
    for n in range(count):

        if vp.s[n].motion == True:
            distance = vp.mag(star.pos-vp.s[n].pos)
            vp.s[n].force = gravitationalForce(vp.s[n],star)
            dHat = (star.pos-vp.s[n].pos) / (distance)
            vp.s[n].momentum = vp.s[n].momentum + vp.s[n].force*dt
            impulse = vp.s[n].momentum/vp.s[n].mass*dt
            vp.s[n].pos = vp.s[n].pos + vp.vector(impulse[0],impulse[1],impulse[2])
            # This change from using vPython less was done soley for testing and full removal of vpython from other code. 1x3 vectors implementation functional


            # if vp.mag(vp.s[n].momentum)<.1:
            #     vp.s[n].color= vp.color.red
            #     vp.s[n].motion = False
            #     print("Particle number " + str(n) + " had a final position of " + str(vp.mag(vp.s[n].pos)))
            #     mmnt_curve.plot(n,vp.mag(vp.s[n].pos))
            #     points.append([n,abs(vp.mag(vp.s[n].pos))])
    i +=1
    # print("FPS: ", 1.0 / (time.time() - start_time))
    t += dt
    k = vp.keysdown()
    
    if 'down' in k : 
        run = False
        print("# of Balls At radius: " + str(success))
        print( "SUCESSS RATE: " + str((success/count)*100))
a.writerows(points)
b.close()
# Issues: for some reason, its no longer elastic like it should be...
# DOWN ARROW IS SHUTDOWN


# Alt implementation: freeze some particles randomly while the sim gets started
    #When all the objects start, they have a one in 10,000 chance of starting to move, 

# Add a property to each particle dubbed "StartFrame", which is a random integer between 0 and 1/3 of the total frames to calculate
# Make two arrays, one with inactive particles, one with active ones