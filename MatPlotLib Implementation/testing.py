import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import json
import matplotlib as mpl 
fig = plt.figure()
ax = p3.Axes3D(fig)
# cache = open ("C:\\Users\\amer_\\OneDrive - Greenhill School\\Documents\\GitHub\\PhysicsSimulations\\MatPlotLib Implementation\\rounded.json")
cache = open ("C:\\Users\\amer_\\OneDrive - Greenhill School\\Documents\\GitHub\\PhysicsSimulations\\blender.json")

mpl.rcParams['animation.ffmpeg_path'] = r'C:\\FFmpeg\\bin\\ffmpeg.exe'
world = {}

world = json.loads(json.load(cache))
world


# data = Gen_RandPrtcls(n_particles=10, n_iterations=3)
data = world['frames']



data = np.array(data)  # (n_iterations, n_particles, 3)
# Plot the first position for all particles
h = ax.plot(*data[0].T, marker='.', linestyle='None')[0]
# Equivalent to
# h = ax.plot(data[0, :, 0], data[0, :, 1], data[0, :, 2], 
#             marker='.', linestyle='None')[0]

# Setting the axes properties
ax.set_xlim3d([-10.0, 10.0])
ax.set_xlabel('X')

ax.set_ylim3d([-10.0, 10.0])
ax.set_ylabel('Y')

ax.set_zlim3d([-10.0, 10.0])
ax.set_zlabel('Z')
ax.set_title('3D Test')

def update_particles(num):
    # Plot the iterations up to num for all particles
    h.set_xdata(data[:num, :, 0].ravel())
    h.set_ydata(data[:num, :, 1].ravel())
    h.set_3d_properties(data[:num, :, 2].ravel())
    return h
f = r"c://Users/amer_/Desktop/animation.gif" 
prtcl_ani = animation.FuncAnimation(fig, update_particles, frames=30000, 
                                    interval=.5)
# writergif = animation.PillowWriter(fps=30) 
# prtcl_ani.save(f, writer=writergif)

plt.show()