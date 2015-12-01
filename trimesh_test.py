import numpy as np
import trimesh

# this list will be much longer if assimp is available
print(trimesh.available_formats())

# load_mesh can accept a filename or file object, 
# however file objects require 'file_type' specified (eg. file_type='stl')
# on load does basic cleanup of mesh, including merging vertices 
# and removing duplicate/degenerate faces
mesh = trimesh.load_mesh('./models/unit_cube.STL')

# split mesh based on connected components
# by default this will only return watertight meshes, but the check can be disabled
meshes = mesh.split() 

# first component  
m = meshes[0]

# assign all faces a color
m.set_face_colors()

# find groups of coplanar adjacent faces
facets, facets_area = m.facets(return_area=True)

# the largest group of faces by area    
largest_facet = facets[np.argmax(facets_area)]

# set all faces of the largest facet to a random color
m.faces[largest_facet] = trimesh.color.random_color()

# preview mesh in an opengl window
m.show()