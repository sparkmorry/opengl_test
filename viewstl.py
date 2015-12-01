from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot

# Create a new plot
figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)

# Load the STL files and add the vectors to the plot
your_mesh = mesh.Mesh.from_file('loveyou4ever.STL')

axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
axes.set_axis_off()

# print your_mesh.data
# print your_mesh.facets


# Auto scale to the mesh size
scale = your_mesh.points.flatten(-1)
axes.auto_scale_xyz(scale, scale, scale)

# Show the plot to the screen
# pyplot.show()
from OpenGL.arrays import vbo

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

# setup
vertices_gl = vbo.VBO(your_mesh.points)
print vertices_gl

def draw():
	glClear(GL_DEPTH_BUFFER_BIT)
    # paint black to blue smooth shaded polygon for background 
	glVertexPointer(2, GL_FLOAT, 0, vertices_gl)
	return
	
def key(k, x, y):
    global view_rotz

    if k == 'z':
        view_rotz += 5.0
    elif k == 'Z':
        view_rotz -= 5.0
    elif ord(k) == 27: # Escape
        sys.exit(0)
    else:
        return
    glutPostRedisplay()


if __name__ == '__main__':
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)

    glutInitWindowPosition(0, 0)
    glutInitWindowSize(300, 300)
    glutCreateWindow("pyGears")
    # init()
    
    glutDisplayFunc(draw)
    # glutReshapeFunc(reshape)
    glutKeyboardFunc(key)
    # glutSpecialFunc(special)
    # glutVisibilityFunc(visible)

    if "-info" in sys.argv:
        print "GL_RENDERER   = ", glGetString(GL_RENDERER)
        print "GL_VERSION    = ", glGetString(GL_VERSION)
        print "GL_VENDOR     = ", glGetString(GL_VENDOR)
        print "GL_EXTENSIONS = ", glGetString(GL_EXTENSIONS)

    glutMainLoop()

# in drawing code
# vertices.bind()
# colours.bind()
# glColorPointer(2, gl.GL_FLOAT, 0, vertices_gl) 
