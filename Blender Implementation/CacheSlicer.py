# Instead of generating a new cache every time I want to change the interpol, I'm using this to slice it up
import time,math,random,json,os
from math import remainder
import vpython as vp
from math import cos,sin,pi
from numpy import arange,array,empty
# Defining the particle class
interp = 10
#Opening the cache
cache = open("C:\\Users\\amer_\\OneDrive - Greenhill School\\Documents\\GitHub\\PhysicsSimulations\\Gas.json")
print(cache)
world = {}
newWorld = {}
world = json.loads(json.load(cache))

newWorld['Count'] = world['Count']
newWorld['frames'] = []
FrameCount = world['FrameCount']
print(FrameCount)
newWorld['FrameCount'] = int(((FrameCount-(FrameCount%10))/10))
print(newWorld['FrameCount'])
#    To modify the initial momentum vector, change the above value under vp.vector() to whatever force vector you can calculate
for i in range(newWorld['FrameCount']):
    newWorld['frames'].append(world['frames'][i*10])
    print(i)
path_to_script = os.path.dirname(os.path.abspath(__file__))

my_filename = os.path.join(path_to_script, "Sliced.json")
data = json.dumps(newWorld, indent = 4)
with open(my_filename, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)



    
