import numpy

from OpenGL.GL import *
from OpenGL.GLU import *

points=numpy.array([2.4,0,0,0,0,2,0,0,0,0,0,2,2.4,0,0,\
2.4,0,2,0,0,2,0,-1.66,0,0,0,0,0,-1.66,0,2.4,0,0,0,0,0,\
2.4,0,0,2.4,-1.66,2,2.4,0,2,2.4,-1.66,2,0,0,2,2.4,0,2,0,\
-1.66,0,0,0,2,0,-1.66,2,2.4,0,0,0,-1.66,0,2.4,-1.66,0,\
2.4,-1.66,2,2.4,0,0,2.4,-1.66,0,0,0,2,2.4,-1.66,2,0,\
-1.66,2,2.4,-1.66,2,0,-1.66,0,0,-1.66,2,0,-1.66,0,2.4,
-1.66,2,2.4,-1.66,0],'f').reshape(-1,3)

indices=numpy.arange(36,'i')

glEnableClientState(GL_VERTEX_ARRAY);
glVertexPointerf( points )
glDrawElementsui(GL_TRIANGLES, indices)