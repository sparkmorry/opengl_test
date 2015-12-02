from visual import *
from convert_stl import stl_to_faces
# Be sure to look at the bottom of the figure!
scene.width = scene.height = 800
scene.autocenter = True
myobj = stl_to_faces("STLbot.stl")
myobj.smooth()
myobj.color = color.orange
myobj.material = materials.wood
