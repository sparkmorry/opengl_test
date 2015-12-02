#import oglFixme
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL.arrays import vbo
from numpy import *
from math import *
import sys
import os

boundingBox = []
my_vbo = None
scale = []
moScale = 1.0
center = []
data = []

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
    # print boundingBox
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


def load_obj(obj_file):
	readfle(obj_file)
	return my_vbo, scale, center, data