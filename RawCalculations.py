# TODO

import math,random,json,os
import numpy as np
from numpy import empty
from playsound import playsound
from datetime import datetime
startTime = datetime.now()
from multiprocessing import Pool
class Particle:
     def __init__(self,pos,mass,momentum):
          self.pos = pos
          self.mass = mass
          self.momentum= momentum

path_to_script = os.path.dirname(os.path.abspath(__file__))
count = 1000
tolerance = 1
# The leeway on how off the force applied can be compared to the adaquete one of that position
radius = 10
G = 1
FrameCount = 30000
interpolation = 10
processes = 10
# ORDER OF DATASTRUCTURE= FRAMES -> PARTICLES -> COORDINATES
# ORDER OF PROCESSING PARTICLES (1-30,000) -> NEXT PARTICLE (1-30,000)
# Accidentally gave it a 3x speed boost lol
star = Particle(np.array([0,0,0]),2*1000,np.array([0,0,0]))
particles = []# particles[0] = empty(int(count/processes),Particle)
# particles[1] = empty(int(count/processes),Particle)
for i in range(processes):
    particles.append([])
    particles[i] = empty(int(count/processes),Particle)
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
    j = 0
j = 0
i= 0
for n in range(count):
    if ((n) % int(count/processes) == 0) and n!= 0: 
        i +=1; 
        j=0
    coordinates = randomCords(radius)             
    x = coordinates[0]
    y = coordinates[1]
    z = coordinates[2]
    particles[i][j] = Particle(np.array([x,y,z]), 1, np.array([0,0,0]))
    particles[i][j].momentum = momentumCalculator(particles[i][j],star,G,radius)
    j+=1
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

dt = 0.0001
success= 0
fractionFrame = 0
def f(particles):
    world = []
    t = 0
    i=0
    world.append([])
    for n in range(int(count/processes)):
        # count/2
        for i in range(FrameCount):
            particles[n].force = gravitationalForceinverse(particles[n],star)
            particles[n].momentum+= particles[n].force*dt
            particles[n].pos += particles[n].momentum/particles[n].mass*dt
            if i%interpolation == 0:

                world.append([])
                # no index exists at i/10 yet, so we add an array to the end of world['frames'] to access 
                world[int(i/interpolation)].append([particles[n].pos[0],particles[n].pos[1],particles[n].pos[2]])
            # i is the frame number
        # n is the particle number
        print(n)
    return world
if __name__ == '__main__':
    with Pool(processes) as p:
        
        calculatedPositions = []
        # # mulp processing outputs an array, with each of the outputs from a process being placed in its correcponding index
        # for i in range(int(count/processes)):
        #     calculatedPositions.append(particles[i])
        #     print(i)
        frames = p.map(f,particles)
        # depending on the number of 
    print('-------------')
    world = []

    for i in range(processes):
        for j in range(int(FrameCount/interpolation)):
            world.append([])
            world[j] += frames[i][j]
            # this should be the first frame slice from the output of the first process
            
    print(world[2999])
    final = {}
    final['Count']= count
    final['FrameCount'] = int(FrameCount/interpolation) 
    final['frames'] = world
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
