# TODO
# Allow particles to spawn within a given radius and have enough energy to fly out of it
# Cache the physics calculations outside of vpython
# - Beforehand, do a basic check for the amount of time this takes compared to the initial vpython run. 
#    If the calculations run faster than vpython than we know that running the posisions from the file won't 
#    increase the speed, as vpython's 3d is taking up most of the loads
import math,random,json,os
import numpy as np
from numpy import empty
from playsound import playsound
from datetime import datetime
startTime = datetime.now()

class Particle:
     def __init__(self,pos,mass,momentum):
          self.pos = pos
          self.mass = mass
          self.momentum= momentum

path_to_script = os.path.dirname(os.path.abspath(__file__))
count = 100
r_Count = range(count)
tolerance = 1
# The leeway on how off the force applied can be compared to the adaquete one of that position
radius = 10
G = 1
FrameCount = 30000
# ORDER OF DATASTRUCTURE= FRAMES -> PARTICLES -> COORDINATES
world = {"Count":count} 
world['FrameCount']= FrameCount

world['frames'] = []

star = Particle(np.array([0,0,0]),2*1000,np.array([0,0,0]))

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
    distance = p1.pos-p2.pos
    # GPE = mass * acceleration * height
    # print("---------------------------")
    # az-timmy
    A = -5.603
    B = -21.17
    C = 86.94
    distanceMag = math.sqrt(p1.pos[0]**2+p1.pos[1]**2+p1.pos[2]**2)
    # Above variables are just from a fit curve of the changing momentum of the real particle
    pos = abs(distanceMag)
    velocity =  math.sqrt(-2*G*p2.mass*((1/radius)-(1/distanceMag)))
    dHat = distance / distanceMag
    if abs(distanceMag) <tolerance:
        velocity = A*(pos**2) + B*pos + C
    if abs(distanceMag) < .75:
        dHat = -dHat
    
    # below is michelle
    # velocity = math.sqrt(abs(2*G*p2.mass*((1/distance)-(1/radius))))

    momentum = p1.mass * velocity * dHat
    return momentum

for n in r_Count:
    coordinates = randomCords(radius)     
    x = coordinates[0]
    y = coordinates[1]
    z = coordinates[2]
    
    particles[n] = Particle(np.array([x,y,z]), 1, np.array([0,0,0]))
    particles[n].momentum = momentumCalculator(particles[n],star,G,radius)

#     To modify the initial momentum vector, change the above value under vp.vector() to whatever force vector you can calculate

def gravitationalForceinverse(p1,p2):
    rVector = p1.pos - p2.pos 
    rMagnitude = rVector[0]**2 +rVector[1]**2 + rVector[2]**2
    # Above is the squared of what
    rHat = rVector * (rMagnitude)**-.5
    # above is the direction
    

    if abs(rMagnitude**.5) < tolerance:
        F = - rHat * G * p1.mass * p2.mass /(tolerance)**2
    else:
        F =  - rHat * G * p1.mass * p2.mass * rMagnitude**-1
        #DIFFERENT G'S MORON, ONE IS THE GRAVITATIONAL ACCELERATION, OTHER IS FOR PLANET
    #    print(F)
    return F
def gravitationalForce(p1,p2):
    rVector = p1.pos - p2.pos 
    rMagnitudesqrd = rVector[0]**2 +rVector[1]**2 + rVector[2]**2
    rHat = rVector * (rMagnitudesqrd)**-.5
    # above is the direction
    F =  - rHat * G * p1.mass * p2.mass * rMagnitudesqrd**-1

    if abs(rMagnitudesqrd**.5) < tolerance:
        F = - rHat * G * p1.mass * p2.mass /(tolerance)**2
        #DIFFERENT G'S MORON, ONE IS THE GRAVITATIONAL ACCELERATION, OTHER IS FOR PLANET
    #    print(F)
    return F
t = 0
dt = 0.0001
run = True
success= 0
i=0
fractionFrame = 0
while(run):
    world['frames'].append([])
    #  particles[n] is a list contaning the planet objects
    n= 0
    count_Run = True
    while(count_Run):
        j = []
        # distance = (star.pos-particles[n].pos)
        particles[n].force = gravitationalForceinverse(particles[n],star)
        particles[n].momentum += particles[n].force*dt
        
        #     Momentum = impulse ( f*t)
        particles[n].pos += particles[n].momentum/particles[n].mass*dt
        if i%10==0:
            j.append(float(format(particles[n].pos[0],'.3f')))
            j.append(float(format(particles[n].pos[1],'.3f')))
            j.append(float(format(particles[n].pos[2],'.3f')))
        #    j is  a list with size 1xTotalParticles, each index has the corresponding numbered particle's x-y-z positions in another list 
            world['frames'][int(i/10)].append(j)
         #    i is the frame number. i is a list with each index being another version of j.
        n +=1

        if n == count: count_Run = False
    
    t += dt
    i += 1
    print(i)
    if i==FrameCount:
        run = False
     
world['frames'].pop(0)
my_filename = os.path.join(path_to_script, "SpeedTesting.json")
data = json.dumps(world, indent = 4)
with open(my_filename, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
print("Time taken to finish: " + str( datetime.now() - startTime))
# Issues: for some reason, its no longer elastic like it should be...

