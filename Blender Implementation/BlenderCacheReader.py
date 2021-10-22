import random
import math
import bpy
import time,math,random,json,os
from math import remainder

from math import cos,sin,pi
from numpy import arange,array,empty
#how many cubes you want to add

cache = open("C:\\Users\\Robotics\\OneDrive - Greenhill School\\Documents\\GitHub\\PhysicsSimulations\\Blender Implementation\\Sliced.json")
worlds = {}

worlds = json.loads(json.load(cache))

count = 100


FrameCount = worlds['FrameCount']



D = bpy.data



bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete() 

for n in range(0,count):    
    coordinates = coordinates = (worlds["frames"][0][(n)])
    
    bpy.ops.mesh.primitive_cube_add(location=(coordinates[0],coordinates[1],coordinates[2]),size = .5)
    print(n)
bpy.ops.object.select_all(action="SELECT")

#for i in range(int(FrameCount/skip)):
n = 0
  #  print(n)
    
for object in bpy.context.selected_objects:
    coordinates = []
    for j in range(FrameCount):
        coordinates.append(worlds['frames'][j][n])
    

#        world =  bpy.context
#       world.scene.frame_set(i)
    # coordinates = (worlds["frames"][(int(i)*skip)][(n)])
#     object.location.x  = coordinates[0]
#    object.location.y  = coordinates[1]
    #   object.location.z  = coordinates[2]
    
    
    #  randColor = random.randint(0,2)
    # object.keyframe_insert(data_path="location", frame=(key))
#      if randColor == 0: object.active_material = red 
#       if randColor == 1: object.active_material = blue
#        if randColor == 2: object.active_material = green
    frames = range(1, FrameCount-1)

    # some action
    a = bpy.data.actions.new(str(n))
    fc = a.fcurves.new("location", n, "LocY")

    fc.keyframe_points.add(count=len(frames))
    # populate points

    fc.keyframe_points.foreach_set("co", 
            [x for co in zip(frames, coordinates) for x in co])
# update 
    fc.update()
# assign to context ob
    ad = bpy.context.object.animation_data_create()
    ad.action = a
    fc.convert_to_samples(1, 250) 
    n += 1
    print(n)




