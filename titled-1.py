import numpy as np

leds=np.tile(0,(3,150))
rgb=[1,2,3]
#leds=np.put_along_axis(leds,np.array([[0],[0],[0]]),10, axis=1)
r=leds[0]
g=leds[1]
b=leds[2]

np.put_along_axis(r,np.array([0,1,2]),rgb[0], axis=0)
np.put_along_axis(g,np.array([0]),rgb[1], axis=0)
np.put_along_axis(b,np.array([0]),rgb[2], axis=0)

leds=np.stack((r,g,b))
print (leds)