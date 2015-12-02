from visual import *
from visual.filedialog import get_file

# Convert 3D .stl file ("stereo lithography") to faces object.

# Original converter and STLbot by Derek Lura 10/06/09
# Be sure to look at the bottom of the STLbot figure!
# Part1.stl found at 3Dcontentcentral.com; also see 3dvia.com

# Factory function and handling of binary files by Bruce Sherwood 1/26/10

# Give this factory function an .stl file and it returns a faces object
# embedded in a default frame, to permit moving and rotating.

# Specify the file either as a file name or a file descriptor.

# See http://en.wikipedia.org/wiki/STL_(file_format)
# Text .stl file starts with a header that begins with the word "solid".
# Binary .stl file starts with a header that should NOT begin with the word "solid",
# but this rule seems not always to be obeyed.
# Currently the 16-bit unsigned integer found after each triangle in a binary
# file is ignored; some versions of .stl files put color information in this value.

def stl_to_faces(fileinfo): # specify file
    # Accept a file name or a file descriptor; make sure mode is 'rb' (read binary)
    if isinstance(fileinfo, str):
        fd = open(fileinfo, mode='rb')
    elif isinstance(fileinfo, file):
        if fileinfo.mode != 'rb':
            filename = fileinfo.name
            fileinfo.close()
            fd = open(filename, mode='rb')
        else:
            fd = fileinfo
    else:
        raise TypeError, "Specify a file"
    text = fd.read()
    if chr(0) in text: # if binary file
        text = text[84:]
        L = len(text)
        N = 2*(L//25) # 25/2 floats per point: 4*3 float32's + 1 uint16
        triNor = zeros((N,3), dtype=float32)
        triPos = zeros((N,3), dtype=float32)
        n = i = 0
        while n < L:
            if n % 200000 == 0:
                print ("%d" % (100*n/L))+"%",
            triNor[i] = fromstring(text[n:n+12], float32)
            triPos[i] = fromstring(text[n+12:n+24], float32)
            triPos[i+1] = fromstring(text[n+24:n+36], float32)
            triPos[i+2] = fromstring(text[n+36:n+48], float32)
            colors = fromstring(text[n+48:n+50], uint16)
            if colors != 0:
                print '%x' % colors
            if triNor[i].any():
                triNor[i] = triNor[i+1] = triNor[i+2] = norm(vector(triNor[i]))
            else:
                triNor[i] = triNor[i+1] = triNor[i+2] = \
                    norm(cross(triPos[i+1]-triPos[i],triPos[i+2]-triPos[i]))
            n += 50
            i += 3
    else:
        fd.seek(0)
        fList = fd.readlines()
        triPos = []
        triNor = []

        # Decompose list into vertex positions and normals
        for line in fList:
            FileLine = line.split( )
            if FileLine[0] == 'facet':
                for n in range(3):
                    triNor.append( [ float(FileLine[2]), float(FileLine[3]), float(FileLine[4]) ]  )
            elif FileLine[0] == 'vertex':
                triPos.append( [ float(FileLine[1]), float(FileLine[2]), float(FileLine[3]) ]  )

        triPos = array(triPos)
        triNor = array(triNor)

    # Compose faces in default frame
    f = frame()
    return faces(frame=f, pos=triPos, normal=triNor)

if __name__ == '__main__':
    print "Choose an stl file to display. Rotate!"
    # Open .stl file
    while True:
        fd = get_file()
        if not fd: continue
        
        scene.width = scene.height = 800
        scene.autocenter = True
        newobject = stl_to_faces(fd)
        newobject.smooth() # average normals at a vertex
        
        # Examples of modifying the returned object:
##        newobject.frame.pos = (-1,-1,-0.5)
##        newobject.frame.axis = (0,1,0)
        newobject.color = color.orange
        newobject.material = materials.wood
        break
