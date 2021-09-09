# TODO

import math,random,json,os
import numpy as np
from numpy import empty
from datetime import datetime
startTime = datetime.now()
from multiprocessing import Pool

path_to_script = os.path.dirname(os.path.abspath(__file__))
count = 10000
tolerance = 1
# The radius at which the div0 compensator kicks in  
radius = 10
G = 1
# The gravitational constant
FrameCount = 30000
interpolation = 10
# Every nth frame is saved. N is interpolation
processes = 10
# ORDER OF DATASTRUCTURE= FRAMES -> PARTICLES -> COORDINATES
# ORDER OF PROCESSING PARTICLES (1-30,000) -> NEXT PARTICLE (1-30,000)
# Accidentally gave it a 3x speed boost lol
class Particle:
     def __init__(self,pos,mass,momentum):
          self.pos = pos
          self.mass = mass
          self.momentum= momentum
star = Particle(np.array([0,0,0]),2*1000,np.array([0,0,0]))
particles = []
for i in range(processes):
    particles.append([])
    particles[i] = empty(int(count/processes),Particle)
    # populate the list particles with empty numpy lists that are filled by each process
def randomCordsOLD(radius):
     cord_X = random.uniform(-radius,radius)

     cord_Y = random.uniform(-math.sqrt(radius**2-(cord_X**2)),math.sqrt(radius**2-(cord_X**2)))
     #Would have used the randint function with an upper bound of y = sqrt(r^2-x^2), but then that removed chances at negative points
     cord_Z = random.uniform(-math.sqrt(abs(radius**2-cord_X**2-cord_Y**2)),math.sqrt(abs(radius**2-cord_X**2-cord_Y**2)))
     # cord_Z = math.sqrt(abs(radius**2-cord_X**2-cord_Y**2))

     return cord_X,cord_Y,cord_Z
def randomCords(radius):
    u = random.uniform(0,1)
    v = random.uniform(0,1)
    theta = u * 2.0 * math.pi
    phi = math.acos(2.0 * v - 1.0)
    r = (random.uniform(0,1))**(1/3)
    sinTheta = math.sin(theta)
    cosTheta = math.cos(theta)
    sinPhi = math.sin(phi)
    cosPhi = math.cos(phi)
    x = r * sinPhi * cosTheta
    y = r * sinPhi * sinTheta
    z = r * cosPhi
    return x*radius,y*radius,z*radius
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
    sign = random.randint(0,1)
    if(sign == 1): sign = -1
    if(sign == 0):sign = 1
    
    momentum = sign*p1.mass * velocity * dHat

    return momentum
    j = 0
j = 0
i= 0
for n in range(count):
    if ((n) % int(count/processes) == 0) and n!= 0: 
        # 0 is technically a factor of processes here so I'm just skipping it
        i +=1; 
        j=0
    coordinates = randomCords(radius)             
    x = coordinates[0]
    y = coordinates[1]
    z = coordinates[2]
    particles[i][j] = Particle(np.array([x,y,z]), 1, np.array([0,0,0]))
    particles[i][j].momentum = momentumCalculator(particles[i][j],star,G,radius)
    j+=1
    # i is the counter for every number that is a factor of the int(processes). It splits up the total particle count across the particle sublists
    # j is the index the loop is currently at inside the sublists
# This loop populates the particles array and sublists with all the Particle objects and their required properties
def gravitationalForce(p1,p2):
    rVector = p1.pos - p2.pos 
    rMagnitude = rVector[0]**2 +rVector[1]**2 + rVector[2]**2
    # Above is the squared of what
    rHat = rVector * (rMagnitude)**-.5
    # above is the direction
    

    if abs(rMagnitude**.5) < tolerance:
        F = - rHat * G * p1.mass * p2.mass /(tolerance)**2
    else:
        F =  - rHat * G * p1.mass * p2.mass * rMagnitude**-1
    #    print(F)
    return F
dt = 0.0001
def f(particles):
    world = []
    i=0
    world.append([])
    for n in range(int(count/processes)):
        # count/2
        for i in range(FrameCount):
            particles[n].force = gravitationalForce(particles[n],star)
            particles[n].momentum+= particles[n].force*dt
            particles[n].pos += particles[n].momentum/particles[n].mass*dt
            if i%interpolation == 0:
                world.append([])
                # no index exists at i/10 yet, so we add an array to the end of world['frames'] to access 
                world[int(i/interpolation)].append([float(format(particles[n].pos[0],'.3f')),float(format(particles[n].pos[1],'.3f')),float(format(particles[n].pos[2],'.3f'))])
                # every frame that has a factor of interpolation is written to.
            # i is the frame number
        # n is the particle number
        print(n)
    return world
if __name__ == '__main__':
    with Pool(processes) as p:
        
        # multiprocessing outputs an array, with each of the outputs from a process being placed in its correcponding index

        frames = p.map(f,particles)
        # depending on the number of 
    world = []
    for i in range(processes):
        for j in range(int(FrameCount/interpolation)):
            world.append([])
            world[j] += frames[i][j]
            # this should be the first frame slice from the output of the first process
    final = {}
    final['Count']= count
    final['FrameCount'] = int(FrameCount/interpolation) 
    final['frames'] = world
    # Some final JSON structure work for backwards compadibility
    my_filename = os.path.join(path_to_script, "SpeedTesting.json")
    data = json.dumps(final, indent = 4)
    with open(my_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("Time taken to finish: " + str( datetime.now() - startTime))
# Issues: for some reason, its no longer elastic like it should be...

# Make a function to iterate the calculation, that takes the parameters of an array of particle objects. From there just simulate each particle to 30,000 frames
# Instead of iterating through each particle in a frame, iterate through each particle and their total frames
#  Multiple process jsons created, now we need to join them
# 
