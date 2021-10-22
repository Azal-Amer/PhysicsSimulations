# TODO

import math,random,json,os
import numpy as np
from numpy import empty
from datetime import datetime
startTime = datetime.now()
from multiprocessing import Pool
import importlib.util

spec = importlib.util.spec_from_file_location("RandomMB", "Gas Dynamics\\randomMB.py")
gas = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gas)

# loading up gas function
path_to_script = os.path.dirname(os.path.abspath(__file__))
count = 2000
tolerance = 1
# The radius at which the div0 compensator kicks in  
radius = 10
G = 1
# The gravitational constant
FrameCount = 30000
interpolation = 10
# Every nth frame is saved. N is interpolation
processes = 10
m_1=5000
m_2 = 1

# ORDER OF DATASTRUCTURE= FRAMES -> PARTICLES -> COORDINATES
# ORDER OF PROCESSING PARTICLES (1-30,000) -> NEXT PARTICLE (1-30,000)
# Accidentally gave it a 3x speed boost lol
velocityMB = gas.randomMB(10,count,m_2)[0]
print(velocityMB)
class Particle:
     def __init__(self,pos,mass,momentum,velocityMB):
          self.pos = pos
          self.mass = mass
          self.momentum= momentum
          self.velocityMB = velocityMB
star = Particle(np.array([0,0,0]),m_1,np.array([0,0,0]),0)
particles = []
for i in range(processes):
    particles.append([])
    particles[i] = empty(int(count/processes),Particle)
    # populate the list particles with empty numpy lists that are filled by each process
def randomCords(radius):
     cord_X = random.uniform(-radius,radius)
     cord_Y = random.uniform(-math.sqrt(radius**2-(cord_X**2)),math.sqrt(radius**2-(cord_X**2)))
     #Would have used the randint function with an upper bound of y = sqrt(r^2-x^2), but then that removed chances at negative points
     cord_Z = random.uniform(-math.sqrt(abs(radius**2-cord_X**2-cord_Y**2)),math.sqrt(abs(radius**2-cord_X**2-cord_Y**2)))
     # cord_Z = math.sqrt(abs(radius**2-cord_X**2-cord_Y**2))
     return cord_X,cord_Y,cord_Z
    #  To Implement this for the magnitude splitter, just have the z coordinate solve for something.
def vectorSplit(radius):
     cord_X = random.uniform(-radius,radius)
     cord_Y = random.uniform(-math.sqrt(radius**2-(cord_X**2)),math.sqrt(radius**2-(cord_X**2)))
     #Would have used the randint function with an upper bound of y = sqrt(r^2-x^2), but then that removed chances at negative points
     cord_Z = math.sqrt(abs(radius**2-cord_X**2-cord_Y**2))*random.choice([-1,1])
     # cord_Z = math.sqrt(abs(radius**2-cord_X**2-cord_Y**2))
     return cord_X,cord_Y,cord_Z
    #  NEED TO BIAS THE DIRECTION OF THE PARTICLES TO THE RADIUS
# New random point grabber rewritten from https://karthikkaranth.me/blog/generating-random-points-in-a-sphere/
# Seemed to be a similar concept to ray tracing
# This implementation works in a polar system, to read more about it, look here https://mathworld.wolfram.com/SpherePointPicking.html
def randNormtoVect(r,mag):
    v = [0,0,0]
    # v is the returned vector
    r_mag = math.sqrt(r[0]**2+r[1]**2+r[2]**2)
    r_hat = np.divide(r,r_mag)


    print('---')
    success = False
    i = 0
    v[0] = random.uniform(-1,1)
    v[1] = random.uniform(-math.sqrt(1-(v[0]**2)),(math.sqrt(1-(v[0]**2))))
    v[2]= (-v[0]*r_hat[0]-v[1]*r_hat[1])/r_hat[2]
    # while(success == False):
        
    #     if (((r_hat[2]**2)+4*(c))/2)>0 :
    #         print(c)
    #         success == True
    #         break
    print("the dot product is " + str(r_hat[0]*v[0]+r_hat[1]*v[1]+r_hat[2]*v[2]))

    # v[2] = ((r_hat[2]+math.sqrt((r_hat[2]**2)+4*(c)))/2)
    print(mag)
    v = np.multiply(v,mag) 
    print(v)
    return v


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

    
    # below is michelle
    # velocity = math.sqrt(abs(2*G*p2.mass*((1/distance)-(1/radius))))
    sign = random.randint(0,1)
    if(sign == 1): sign = -1
    if(sign == 0):sign = 1
    
    momentum = sign*p1.mass * velocity * dHat
    return momentum
j = 0
i= 0
for n in range(count):
    randomVelocityMBIndex = np.random.random_integers(0,count-1)
    if ((n) % int(count/processes) == 0) and n!= 0: 
        # 0 is technically a factor of processes here so I'm just skipping it
        i +=1; 
        j=0
    coordinates = randomCords(radius)             
    x = coordinates[0]
    y = coordinates[1]
    z = coordinates[2]
    particles[i][j] = Particle(np.array([x,y,z]), m_2, np.array([0,0,0]),randNormtoVect([x,y,z],velocityMB[randomVelocityMBIndex]))
    gravMomentum = momentumCalculator(particles[i][j],star,G,radius)
    particles[i][j].momentum = (gravMomentum+ particles[i][j].velocityMB)
    # Maybe take the differences in the magnitude of the two momentums, then split it up
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
        
        calculatedPositions = []
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
    my_filename = os.path.join(path_to_script, "Gas.json")
    data = json.dumps(final, indent = 4)
    with open(my_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("Time taken to finish: " + str( datetime.now() - startTime))


# Issues: for some reason, its no longer elastic like it should be...

# Make a function to iterate the calculation, that takes the parameters of an array of particle objects. From there just simulate each particle to 30,000 frames
# Instead of iterating through each particle in a frame, iterate through each particle and their total frames
#  Multiple process jsons created, now we need to join them
# 
