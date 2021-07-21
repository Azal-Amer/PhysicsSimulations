import bpy
import random
import math
import bpy
import time,math,random,json,os
from math import remainder

from math import cos,sin,pi
from numpy import arange,array,empty
#how many cubes you want to add

cache = open("C:\\Users\\amer_\\OneDrive - Greenhill School\\Documents\\GitHub\\PhysicsSimulations\\dummy.json")
worlds = {}

worlds = json.loads(json.load(cache))

count = worlds['Count']


FrameCount = worlds['FrameCount']

skip = 100

D = bpy.data
red= D.materials["Red"]
blue = D.materials["Blue"]
green = D.materials["Green"]


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete() 

for n in range(0,count):    
    coordinates = coordinates = (worlds["frames"]['0'][str(n)])
    
    bpy.ops.mesh.primitive_cube_add(location=(coordinates[0],coordinates[1],coordinates[2]),size = .5)
bpy.ops.object.select_all(action="SELECT")

for i in range(int(FrameCount/skip)):
    n = 0
    
    for object in bpy.context.selected_objects:

        world =  bpy.context
        world.scene.frame_set(i)
        coordinates = (worlds["frames"][str(int(i)*skip)][str(n)])
        object.location.x  = coordinates[0]
        object.location.y  = coordinates[1]
        object.location.z  = coordinates[2]
        randColor = random.randint(0,2)
        object.keyframe_insert(data_path="location")
        if randColor == 0: object.active_material = red 
        if randColor == 1: object.active_material = blue
        if randColor == 2: object.active_material = green 
        n += 1
        print(n)
#        if randSelect >7:
#            coordinates = randomCords(radius)
#            object.location.x  = coordinates[0]
#            object.location.y  = coordinates[1]
#            object.location.z  = coordinates[2]
#        else:
#            object.location.x  = -object.location.x 
#            object.location.y  = -object.location.y
#            object.location.z  = -object.location.z 
#        object.keyframe_insert(data_path="location")




