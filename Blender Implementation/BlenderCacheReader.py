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
    coordinates = coordinates = (worlds["frames"][0][n])
    
    bpy.ops.mesh.primitive_cube_add(location=(coordinates[0],coordinates[1],coordinates[2]),size = .5)
    print(n)
bpy.ops.object.select_all(action="SELECT")

#for i in range(int(FrameCount/skip)):
n = 0
  #  print(n)
    
for object in bpy.context.selected_objects:
    bpy.ops.object.select_all(action="SELECT")
    y_cord = []
    x_cord = []
    z_cord = []
    for j in range(FrameCount):

        y_cord.append(worlds['frames'][j][n][1])
    frames = range(1, FrameCount-1)
    # some action
    a = bpy.data.actions.new(str(n))
    fc = a.fcurves.new("location", index=1, action_group ="LocY")

    
    # populate points

    fc.keyframe_points.foreach_set("co", 
            [x for co in zip(frames, y_cord) for x in co])

# update 
    fc.update()
# assign to context ob
    ad = object.animation_data_create()
    ad.action = a
    fc.convert_to_samples(1, FrameCount-1) 
    n += 1
    
n=0
for object in bpy.context.selected_objects:
    bpy.ops.object.select_all(action="SELECT")

    x_cord = []

    for j in range(FrameCount):

        x_cord.append(worlds['frames'][j][n][0])

    frames = range(1, FrameCount-1)
    # some action
    a = bpy.data.actions.new(str(n))
    fc = a.fcurves.new("location", index=0, action_group ="LocX")
    fc.keyframe_points.add(count=len(frames))

    
    # populate points


    fc.keyframe_points.foreach_set("co", 
            [x for co in zip(frames, x_cord) for x in co])
    
# update 
    fc.update()
# assign to context ob
    ad = object.animation_data_create()
    ad.action = a
    fc.convert_to_samples(1, FrameCount-1) 
    n += 1
n=0
for object in bpy.context.selected_objects:
    bpy.ops.object.select_all(action="SELECT")

    z_cord = []
    for j in range(FrameCount):

        z_cord.append(worlds['frames'][j][n][2])
    
    frames = range(1, FrameCount-1)
    # some action
    a = bpy.data.actions.new(str(n))

    fc = a.fcurves.new("location", index=2, action_group ="LocZ")
    fc.keyframe_points.add(count=len(frames))

    
    # populate points  
    fc.keyframe_points.foreach_set("co", 
            [x for co in zip(frames, z_cord) for x in co])
# update 
    fc.update()
# assign to context ob
    ad = object.animation_data_create()
    ad.action = a
    fc.convert_to_samples(1, FrameCount-1) 
    n += 1




