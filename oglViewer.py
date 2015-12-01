#coding=utf-8
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

EXIT = -1
FIRST = 0

moScale = 2.0

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


def loadOBJ(filename):
    objectVertices = []
    objectNormals = []
    objectFaces = []
    data = []

    for lines in file(filename):
        # check if not empty
        if lines.split():
            check = lines.split()[0]
            if check == 'v':
                objectVertices.append(map(float, lines.split()[1:]))
            if check == 'vn':
                objectNormals.append(map(float, lines.split()[1:]))
            if check == 'f':
                first = lines.split()[1:]
                for face in first:
                    objectFaces.append(map(float, face.split('//')))

    for face in objectFaces:
        # if no vt is available fill up with 0 at list position 1
        if len(face) == 2:
            face.insert(1, 0.0)
        # if no vt and no vn is available fill up with 0 at list position 1 and
        if len(face) == 1:
            face.insert(1, 0.0)
            face.insert(2, 0.0)

    return objectVertices, objectNormals, objectFaces


def readfle(string):
    '''
    load obj File, init Bounding Box, init Faces
    '''
    global my_vbo, scale, center, data, boundingBox

    # load obj File
    objectVertices, objectNormals, objectFaces = loadOBJ(string)
    data = []

    # Create BoundingBox
    boundingBox = [map(min, zip(*objectVertices)),
                   map(max, zip(*objectVertices))]
    # Calc center of bounding box
    center = [(x[0] + x[1]) / 2.0 for x in zip(*boundingBox)]
    # Calc scale factor
    print boundingBox
    scale = moScale / max([(x[1] - x[0]) for x in zip(*boundingBox)])

    # get the right data for the my_vbo
    for vertex in objectFaces:
        vn = int(vertex[0]) - 1
        nn = int(vertex[2]) - 1
        if objectNormals:
            data.append(objectVertices[vn] + objectNormals[nn])
        else:
            # calc standard normals, if no objectNormals available
            normals = [x - y for x, y in zip(objectVertices[vn], center)]
            l = math.sqrt(normals[0] ** 2 + normals[1] ** 2 + normals[2] ** 2)
            normals = [x / l for x in normals]
            data.append(objectVertices[vn] + normals)

    my_vbo = vbo.VBO(array(data, 'f'))

# readfle("loveyou4ever.obj")

teapotList = None

def init2(WIDTH, HEIGHT):
    """ Initialize an OpenGL window """
    # glClearColor(0.0, 0.0, 0.0, 0.0)  # background color
    ambient = [0.0, 0.0, 0.0, 1.0]
    diffuse = [1.0, 1.0, 1.0, 1.0]
    specular = [1.0, 1.0, 1.0, 1.0]
    position = [0.0, 3.0, 3.0, 0.0]

    lmodel_ambient = [0.2, 0.2, 0.2, 1.0]
    local_view = [0.0]

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

    global teapotList
    teapotList = glGenLists(1)
    glNewList (teapotList, GL_COMPILE)
    glutSolidTeapot(1.0)
    #   glutWireTeapot(1.0)
    #   glutSolidSphere( 1.0, 8, 8 )
    glEndList ()
    # if perspect:
    #     glMatrixMode(GL_PROJECTION)
    #     glLoadIdentity()
    #     gluPerspective(fov, aspect, near, far)
    #     gluLookAt(0, 0, 4 + scale, 0, 0, 0, 0, 1, 0)
    #     glMatrixMode(GL_MODELVIEW)
    # elif ortho:
    #     glMatrixMode(GL_PROJECTION)
    #     glLoadIdentity()
    #     glOrtho(-1.5, 1.5, -1.5, 1.5, -10.0, 10.0)
    #     glMatrixMode(GL_MODELVIEW)


def init():
    ambient = [0.0, 0.0, 0.0, 1.0]
    diffuse = [1.0, 1.0, 1.0, 1.0]
    specular = [1.0, 1.0, 1.0, 1.0]
    position = [0.0, 3.0, 3.0, 0.0]

    lmodel_ambient = [0.2, 0.2, 0.2, 1.0]
    local_view = [0.0]

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

    #  be efficient--make teapot display list 
    global teapotList
    teapotList = glGenLists(1)
    glNewList (teapotList, GL_COMPILE)
    glutSolidTeapot(1.0)
    #   glutWireTeapot(1.0)
    #   glutSolidSphere( 1.0, 8, 8 )
    glEndList ()
    
def renderVBO(x, y, ambr, ambg, ambb, difr, difg, 
                      difb, specr, specg, specb, shine):
    mat = [0, 0, 0, 0]

    glPushMatrix()
    # glTranslatef(x, y, 0.0)
    mat[0] = ambr; mat[1] = ambg; mat[2] = ambb; mat[3] = 1.0
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat)
    mat[0] = difr; mat[1] = difg; mat[2] = difb
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat)
    mat[0] = specr; mat[1] = specg; mat[2] = specb
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat)
    glMaterialf(GL_FRONT, GL_SHININESS, shine * 128.0)

    my_vbo.bind()

    # glColor(color[0], color[1], color[2])  # render stuff
    # glLoadIdentity()

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)

    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glVertexPointer(3, GL_FLOAT, 24, my_vbo)
    glNormalPointer(GL_FLOAT, 24, my_vbo + 12)

    glTranslate(newX, newY, 0.0)
    glRotate(angle, 1, 0, 0)
    glRotate(angle, 0, 1, 0)
    glRotate(angle, 0, 0, 1)
    glMultMatrixf(actOri * rotate(angle, axis))
    glScale(scale, scale, scale)
    glTranslate(-center[0], -center[1], -center[2])

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glDrawArrays(GL_TRIANGLES, 0, len(data))

    my_vbo.unbind()

    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_NORMAL_ARRAY)
    glutSwapBuffers()  # swap buffer
    glPopMatrix()

def renderTeapot(x, y, ambr, ambg, ambb, difr, difg, 
                      difb, specr, specg, specb, shine):
    mat = [0, 0, 0, 0]

    glPushMatrix()
    glTranslatef(x, y, 0.0)
    mat[0] = ambr; mat[1] = ambg; mat[2] = ambb; mat[3] = 1.0
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat)
    mat[0] = difr; mat[1] = difg; mat[2] = difb
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat)
    mat[0] = specr; mat[1] = specg; mat[2] = specb
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat)
    glMaterialf(GL_FRONT, GL_SHININESS, shine * 128.0)
    # Linux GLUT seems to optimize away the actual generation of the 
    # teapot on modern GLUT when using display-lists, so we have to 
    # use direct calls here...
    #   glCallList(teapotList)
    glutSolidTeapot(1.0)
    glPopMatrix()

def display():
    #print center
    """ Render all objects"""
    # white_light = [1.0, 1.0, 1.0, 1.0]
    global teapotList
    if not teapotList:
        init();
    glClearColor( 1.0,1.0,1.0, 1.0 )
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # clear screen

    renderTeapot(2.0, 17.0, 0.0215, 0.1745, 0.0215,
      0.07568, 0.61424, 0.07568, 0.633, 0.727811, 0.633, 0.6)
    renderTeapot(2.0, 14.0, 0.135, 0.2225, 0.1575,
      0.54, 0.89, 0.63, 0.316228, 0.316228, 0.316228, 0.1)
    renderTeapot(2.0, 11.0, 0.05375, 0.05, 0.06625,
      0.18275, 0.17, 0.22525, 0.332741, 0.328634, 0.346435, 0.3)
    renderTeapot(2.0, 8.0, 0.25, 0.20725, 0.20725,
      1, 0.829, 0.829, 0.296648, 0.296648, 0.296648, 0.088)
    renderTeapot(2.0, 5.0, 0.1745, 0.01175, 0.01175,
      0.61424, 0.04136, 0.04136, 0.727811, 0.626959, 0.626959, 0.6)
    renderTeapot(2.0, 2.0, 0.1, 0.18725, 0.1745,
      0.396, 0.74151, 0.69102, 0.297254, 0.30829, 0.306678, 0.1)
    renderTeapot(6.0, 17.0, 0.329412, 0.223529, 0.027451,
      0.780392, 0.568627, 0.113725, 0.992157, 0.941176, 0.807843,
      0.21794872);
    renderTeapot(6.0, 14.0, 0.2125, 0.1275, 0.054,
      0.714, 0.4284, 0.18144, 0.393548, 0.271906, 0.166721, 0.2)
    renderTeapot(6.0, 11.0, 0.25, 0.25, 0.25,
      0.4, 0.4, 0.4, 0.774597, 0.774597, 0.774597, 0.6)
    renderTeapot(6.0, 8.0, 0.19125, 0.0735, 0.0225,
      0.7038, 0.27048, 0.0828, 0.256777, 0.137622, 0.086014, 0.1)
    renderTeapot(6.0, 5.0, 0.24725, 0.1995, 0.0745,
      0.75164, 0.60648, 0.22648, 0.628281, 0.555802, 0.366065, 0.4)
    renderTeapot(6.0, 2.0, 0.19225, 0.19225, 0.19225,
      0.50754, 0.50754, 0.50754, 0.508273, 0.508273, 0.508273, 0.4)
    renderTeapot(10.0, 17.0, 0.0, 0.0, 0.0, 0.01, 0.01, 0.01,
      0.50, 0.50, 0.50, .25)
    renderTeapot(10.0, 14.0, 0.0, 0.1, 0.06, 0.0, 0.50980392, 0.50980392,
      0.50196078, 0.50196078, 0.50196078, .25)
    renderTeapot(10.0, 11.0, 0.0, 0.0, 0.0,
      0.1, 0.35, 0.1, 0.45, 0.55, 0.45, .25);
    renderTeapot(10.0, 8.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0,
      0.7, 0.6, 0.6, .25)
    renderTeapot(10.0, 5.0, 0.0, 0.0, 0.0, 0.55, 0.55, 0.55,
      0.70, 0.70, 0.70, .25)
    renderTeapot(10.0, 2.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.0,
      0.60, 0.60, 0.50, .25)
    renderTeapot(14.0, 17.0, 0.02, 0.02, 0.02, 0.01, 0.01, 0.01,
      0.4, 0.4, 0.4, .078125)
    renderTeapot(14.0, 14.0, 0.0, 0.05, 0.05, 0.4, 0.5, 0.5,
      0.04, 0.7, 0.7, .078125)
    renderTeapot(14.0, 11.0, 0.0, 0.05, 0.0, 0.4, 0.5, 0.4,
      0.04, 0.7, 0.04, .078125)
    renderTeapot(14.0, 8.0, 0.05, 0.0, 0.0, 0.5, 0.4, 0.4,
      0.7, 0.04, 0.04, .078125)
    renderTeapot(14.0, 5.0, 0.05, 0.05, 0.05, 0.5, 0.5, 0.5,
      0.7, 0.7, 0.7, .078125)
    renderTeapot(14.0, 2.0, 0.05, 0.05, 0.0, 0.5, 0.5, 0.4,
      0.7, 0.7, 0.04, .078125)
    glutSwapBuffers()


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


def reshape(width, height):
    """ adjust projection matrix to window size"""
    global WIDTH, HEIGHT, aspect
    WIDTH, HEIGHT = width, height
    glViewport(0, 0, WIDTH, HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if ortho:
        if WIDTH <= HEIGHT:
            glOrtho(-1.5, 1.5, -1.5 * HEIGHT / WIDTH, 1.5 * HEIGHT / WIDTH,
                    -10.0, 10.0)
        else:
            glOrtho(-1.5 * WIDTH / HEIGHT, 1.5 * WIDTH / HEIGHT,
                    -1.5, 1.5, -10.0, 10.0)
    if perspect:
        if WIDTH <= HEIGHT:
            aspectHeight = float(HEIGHT) / WIDTH
            aspect = float(WIDTH) / HEIGHT
            gluPerspective(fov * aspectHeight, aspect, near, far)
        else:
            aspect = float(WIDTH / HEIGHT)
            gluPerspective(fov, aspect, near, far)
        gluLookAt(0, 0, 4 + scale, 0, 0, 0, 0, 1, 0)

    glMatrixMode(GL_MODELVIEW)


def projectOnSphere(x, y, r):
    x, y = x - WIDTH / 2.0, HEIGHT / 2.0 - y
    a = min(r * r, x ** 2 + y ** 2)
    z = sqrt(r * r - a)
    l = sqrt(x ** 2 + y ** 2 + z ** 2)
    return x / l, y / l, z / l


def keyPressed(key, x, y):
    """ handle keypress events """
    global angleX, angleY, angleZ, angle, actOri
    global scale
    global bgColor, objColor, color
    global perspect, ortho

    if key == chr(27):  # chr(27) = ESCAPE
        sys.exit()
    #Rotation x down
    elif key == 's':
        angle = (angle + 10) / float(WIDTH)
        axis = [1, 0, 0]
        actOri = actOri * rotate(angle, axis)
    #Rotation x up
    elif key == 'w':
        angle = (angle - 10) / float(WIDTH)
        axis = [1, 0, 0]
        actOri = actOri * rotate(angle, axis)
    #Rotation y right
    elif key == 'd':
        angle = (angle + 10) / float(HEIGHT)
        axis = [0, 1, 0]
        actOri = actOri * rotate(angle, axis)
    #Rotation y left
    elif key == 'a':
        angle = (angle - 10) / float(HEIGHT)
        axis = [0, 1, 0]
        actOri = actOri * rotate(angle, axis)
    #Rotate z left
    elif key == 'q':
        angle = (angle + 10) / float(HEIGHT)
        axis = [0, 0, 1]
        actOri = actOri * rotate(angle, axis)
    #Rotate z right
    elif key == 'e':
        angle = (angle - 10) / float(HEIGHT)
        axis = [0, 0, 1]
        actOri = actOri * rotate(angle, axis)

    #backcolor
    if key == '+':
        if bgColor == 5:
            bgColor = 0
        else:
            bgColor += 1

    if key == "c":
        if objColor == 5:
            objColor = 0
        else:
            objColor += 1

    if key == "p":
        if perspect:
            perspect = False
            ortho = True
        else:
            perspect = True
            ortho = False
        init(WIDTH, HEIGHT)

    if bgColor == 0:
        glClearColor(0.0, 0.0, 0.0, 0.0)  # black
    elif bgColor == 1:
        glClearColor(0.0, 1.0, 0.0, 0.0)  # gree
    elif bgColor == 2:
        glClearColor(1.0, 0.0, 0.0, 0.0)  # red
    elif bgColor == 3:
        glClearColor(0.0, 0.0, 1.0, 0.0)  # blue
    elif bgColor == 4:
        glClearColor(1.0, 1.0, 1.0, 0.0)  # white
    elif bgColor == 5:
        glClearColor(1.0, 1.0, 0.0, 0.0)  # yellow

    if objColor == 0:
        color = (1.0, 1.0, 0.0)  # yellow
    elif objColor == 1:
        color = (0.0, 1.0, 0.0)  # green
    elif objColor == 2:
        color = (1.0, 0.0, 0.0)  # red
    elif objColor == 3:
        color = (1.0, 1.0, 1.0)  # white
    elif objColor == 4:
        color = (0.0, 0.0, 0.0)  # black
    elif objColor == 5:
        color = (0.0, 0.0, 10)  # blue

    glutPostRedisplay()


def mousebuttonpressed(button, state, x, y):
    global startP, actOri, angle, doRot, scale, doZoom, doTrans, oldX, oldY
    r = min(WIDTH, HEIGHT) / 2.0
    oldX, oldY = 0, 0
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            doRot = True
            startP = projectOnSphere(x, y, r)
        if state == GLUT_UP:
            doRot = False
            actOri = actOri * rotate(angle, axis)
            angle = 0
    elif button == GLUT_MIDDLE_BUTTON:
        if state == GLUT_DOWN:
            doZoom = True
        if state == GLUT_UP:
            doZoom = False
    elif button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            doTrans = True
        if state == GLUT_UP:
            doTrans = False


def mouseMotion(x, y):
    global angle, axis, oldY, oldX, oldZ, center, angleX, angleY, anglez,\
           newX, newY, distance, scale
    transX, transY = 0, 0
    if oldX:
        transX = x - oldX
    if oldY:
        transY = y - oldY

    if doRot:
        r = min(WIDTH, HEIGHT) / 2.0
        moveP = projectOnSphere(x, y, r)
        angle = acos(dot(startP, moveP))
        axis = cross(startP, moveP)
    elif doZoom:
        print oldY, y
        if oldY > y:
            scale = scale * 1.1
        if oldY < y:
            scale = scale * 0.9
    elif doTrans:
        print "old", newX, newY
        if x - oldX != 0:
            newX = newX + transX / float(WIDTH)
        if y - oldY != 0:
            newY = newY - transY / float(HEIGHT)
        print "new", newX, newY
    oldX = x
    oldY = y
    glutPostRedisplay()


def menu_func(value):
    """ handle menue selection """
    print "menue entry ", value, "choosen..."
    if value == EXIT:
        sys.exit()
        glutPostRedisplay()


def main():
    # Hack for Mac OS X
    # cwd = os.getcwd()
    # glutInit(sys.argv)
    # os.chdir(cwd)

    # glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    # glutInitWindowSize(500, 500)
    # glutCreateWindow("test OBJ")

    # glutDisplayFunc(display)  # register display function
    # glutReshapeFunc(reshape)  # register reshape function
    # glutKeyboardFunc(keyPressed)  # register keyboard function
    # glutMouseFunc(mousebuttonpressed)  # register pressed function
    # glutMotionFunc(mouseMotion)  # register motion function
    # glutCreateMenu(menu_func)  # register menue function

    # glutAddMenuEntry("First Entry", FIRST)  # Add a menu entry
    # glutAddMenuEntry("EXIT", EXIT)  # Add another menu entry
    # # glutAttachMenu(GLUT_RIGHT_BUTTON)  # Attach mouse button to menue

    # init(WIDTH, HEIGHT)  # initialize OpenGL state

    # glutMainLoop()  # start even processing
    glutInit(sys.argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
    glutInitWindowSize(500, 600);
    glutInitWindowPosition(50,50);
    glutCreateWindow(sys.argv[0]);
    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    glutKeyboardFunc(keyPressed)
    glutMainLoop()

if __name__ == "__main__":
    main()