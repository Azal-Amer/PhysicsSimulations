import time,math,random,json,os
from numpy import arange,array,empty
from matplotlib.animation import FuncAnimation
import mpl_toolkits.mplot3d.axes3d as p3
# cache = open("C:\\Users\\amer_\\OneDrive - Greenhill School\\Documents\\GitHub\\PhysicsSimulations\\Caches\\dummy.json")
cache = open ("C:\\Users\\amer_\\OneDrive - Greenhill School\\Documents\\GitHub\\PhysicsSimulations\\MatPlotLib Implementation\\rounded.json")
world = {}

world = json.loads(json.load(cache))
content = world['frames']['0']
import numpy as np
import matplotlib.pyplot as plt
framecount = world['FrameCount']
count = world['Count']
#with open("measurements.txt") as f:
    #content = f.read().splitlines()
#print content

#for value in content:
#    x, y, z = value.split(',')
x=[]
y=[]
z=[]
points = []
fig = plt.figure()

ax = p3.Axes3D(fig)
h = ax.plot(*data[0].T, marker='.', linestyle='None')[0]
for i in range(count):
    x.append(float(world['frames']['0'][str(i)][0]))
    y.append(float(world['frames']['0'][str(i)][1]))
    z.append(float(world['frames']['0'][str(i)][2]))
    print(x)
    newpoint, = ax.plot(x[i], y[i],z[i])
    print(newpoint)
    points.append(newpoint)
    

def animation_frames(i):
    for j in range(framecount):
        xi = float(world['frames'][str(j)][str(i)][0])
        yi = float(world['frames'][str(j)][str(i)][1])
        zi = float(world['frames'][str(j)][str(i)][2])
        print(str(xi) + ',' + str(yi) + ',' + str(zi))
        points[j].set_3d_properties(xi,yi)       

animation = FuncAnimation(fig, animation_frames, frames=framecount, interval=30)
    
#print(x, y, z)
plt.show()

