'''
Created on 20.05.2013
@author: tland001
Tastenkonfig:
A = Objekt nach Links drehen (um Y-Achse)
D = Objekt nach Rechts drehen (um Y-Achse)
S = Objekt nach unten drehen (um X-Achse)
W = Objekt nach Oben drehen (um X-Achse)
Q = Objekt nach Links drehen (um Z-Achse)
E = Objekt nach Rechts drehen (um Z-Achse)
P = Perspektive Wechseln (Orthogonal / Perspektivisch)
+ = Hintergrundfarbe wechseln
- = Objektfarbe wechseln
'''
#import oglFixme
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL.arrays import vbo
from numpy import *
from math import *
import sys
import os
from loadobj import load_obj


EXIT = -1
FIRST = 0

WIDTH, HEIGHT = 500, 500
bgColor = 0
objColor = 0
color = (1.0, 1.0, 0.0)

doZoom = False
doRot = False
doTrans = False

perspect = False
ortho = True

aspect = float(WIDTH / HEIGHT)
fov = 45
near = 0.1
far = 30.0

axis = [1, 0, 0]
angle = 0
angleX, angleY, angleZ = 0, 0, 0
actOri = matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

oldY = 0.0
oldX = 0.0
newX = 0.0
newY = 0.0

boundingBox = []
my_vbo = None
scale = []

distance = 0

"""
def readfle(string):
    fle = [x.split() for x in file(string)]
    v, f = [], []
    for i in fle:
        if i != [] and i[0] == "v":
            v.append([float(i[1]), float(i[2]), float(i[3])])
        if i != [] and i[0] == "f":
            f.append([int(i[1].split('//')[0]), int(i[2].split('//')[0]),
                      int(i[3].split('//')[0])])
    data = []
    for face in f:
        for vertex in face:
            vn = int(vertex[0]) - 1
            nn = int(vertex[2]) - 1
            data.append()
    vTri = [v[y - 1] for x in f for y in x]
    return vTri
"""


# my_vbo, scale, center, data = load_obj("obj/loveyou4ever.obj")
my_vbo, scale, center, data = load_obj("obj/heart.obj")


def init(WIDTH, HEIGHT):
    """ Initialize an OpenGL window """
    glClearColor(0.0, 0.0, 0.0, 0.0)  # background color
    if perspect:
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(fov, aspect, near, far)
        gluLookAt(0, 0, 4 + scale, 0, 0, 0, 0, 1, 0)
        glMatrixMode(GL_MODELVIEW)
    elif ortho:
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-1.5, 1.5, -1.5, 1.5, -10.0, 10.0)
        glMatrixMode(GL_MODELVIEW)

def init_light():
    ambient = [1.0, 1.0, 1.0, 0.2]
    diffuse = [1.0, 1.0, 1.0, 0.5]
    specular = [1.0, 1.0, 1.0, 0.5]
    position = [1.0, 1.0, 0.0, 1.0]

    lmodel_ambient = [0.2, 0.2, 0.2, 1.0]
    local_view = [1.0]

    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)
    glLightfv(GL_LIGHT0, GL_POSITION, position)
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, lmodel_ambient)
    glLightModelfv(GL_LIGHT_MODEL_LOCAL_VIEWER, local_view)

    glFrontFace(GL_CW)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_AUTO_NORMAL)
    glEnable(GL_NORMALIZE)
    glEnable(GL_DEPTH_TEST) 

def draw_vbo():
    my_vbo.bind()

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)

    #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glVertexPointer(3, GL_FLOAT, 24, my_vbo)
    glNormalPointer(GL_FLOAT, 24, my_vbo + 12)

    # glTranslate(newX, newY, 0.0)
    # glRotate(angle, 1, 0, 0)
    # glRotate(angle, 0, 1, 0)
    # glRotate(angle, 0, 0, 1)
    # glMultMatrixf(actOri * rotate(angle, axis))
    glScale(scale, scale, scale)
    # glTranslate(-center[0], -center[1], -center[2])

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glDrawArrays(GL_TRIANGLES, 0, len(data))

    my_vbo.unbind()

    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_NORMAL_ARRAY)
    glutSwapBuffers()  # swap buffer


def renderVBO(x, y, ambr, ambg, ambb, difr, difg, 
                      difb, specr, specg, specb, shine):
    mat = [0, 0, 0, 0]

    glPushMatrix()
    glTranslatef(x, y, 0.0)
    mat[0] = ambr; mat[1] = ambg; mat[2] = ambb; mat[3] = 1.0
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat)
    mat[0] = difr; mat[1] = difg; mat[2] = difb
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat)
    mat[0] = specr; mat[1] = specg; mat[2] = specb

    print mat

    glMaterialfv(GL_FRONT, GL_SPECULAR, mat)
    glMaterialf(GL_FRONT, GL_SHININESS, shine * 128.0)
    # Linux GLUT seems to optimize away the actual generation of the 
    # teapot on modern GLUT when using display-lists, so we have to 
    # use direct calls here...
    #   glCallList(teapotList)
    # glutSolidTeapot(1.0)
    draw_vbo()
    glPopMatrix()

def display():
    #print center
    """ Render all objects"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # clear screen
    glColor(color[0], color[1], color[2])  # render stuff

    glLoadIdentity()

    init_light()

    renderVBO(10.0, 5.0, 0.0, 0.0, 0.0, 0.55, 0.55, 0.55,
      0.70, 0.70, 0.70, .25)

def rotate(angle, axis):
    c, mc = cos(float(angle)), 1 - cos(float(angle))
    s = sin(angle)
    l = sqrt(dot(array(axis), array(axis)))
    x, y, z = array(axis) / l
    r = matrix(
               [[x * x * mc + c, x * y * mc - z * s, x * z * mc + y * s, 0],\
                [x * y * mc + z * s, y * y * mc + c, y * z * mc - x * s, 0],\
                [x * z * mc - y * s, y * z * mc + x * s, z * z * mc + c, 0],
                [0, 0, 0, 1]])
    return r.transpose()


def keyPressed(key, x, y):
    """ handle keypress events """
    if key == chr(27):  # chr(27) = ESCAPE
        sys.exit()

def main():
    # Hack for Mac OS X
    cwd = os.getcwd()
    glutInit(sys.argv)
    os.chdir(cwd)

    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutCreateWindow("simple openGL/GLUT template")

    glutDisplayFunc(display)  # register display function
    glutKeyboardFunc(keyPressed)  # register keyboard function

    glutAddMenuEntry("First Entry", FIRST)  # Add a menu entry
    glutAddMenuEntry("EXIT", EXIT)  # Add another menu entry
    # glutAttachMenu(GLUT_RIGHT_BUTTON)  # Attach mouse button to menue

    # init(WIDTH, HEIGHT)  # initialize OpenGL state

    glutMainLoop()  # start even processing


if __name__ == "__main__":
    main()