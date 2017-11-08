import sys
import numpy as np

try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GL import glOrtho
    from OpenGL.GLU import gluPerspective
    from OpenGL.GL import glRotated
    from OpenGL.GL import glTranslated
    from OpenGL.GL import glLoadIdentity
    from OpenGL.GL import glMatrixMode
    from OpenGL.GLUT import glutTimerFunc
except:
    print("ERROR: PyOpenGL not installed properly. ")

global perspective
perspective = 1
DISPLAY_WIDTH = 500.0
DISPLAY_HEIGHT = 500.0
zhome = 51
global zdelta
zdelta = 0

xhome = 22
global xdelta
xdelta = 0

yhome = 22
global ydelta

ydelta = 0
global thetadelta
thetadelta = 0
thetahome = 0

global spacing
spacing = 17

global cs
cs = 2

global carDelta 
carDelta = 0

global carInc
carInc = 0.15

global tireRot
tireRot = 0

def init(): 
    glClearColor (0.0, 0.0, 0.0, 0.0)
    glShadeModel (GL_FLAT)

def drawHouse ():
    glLineWidth(2.5)
    glColor3f(1.0, 0.0, 0.0)
    #Floor
    glBegin(GL_LINES)
    glVertex3f(-5.0, 0.0, -5.0)
    glVertex3f(5, 0, -5)
    glVertex3f(5, 0, -5)
    glVertex3f(5, 0, 5)
    glVertex3f(5, 0, 5)
    glVertex3f(-5, 0, 5)
    glVertex3f(-5, 0, 5)
    glVertex3f(-5, 0, -5)
    #Ceiling
    glVertex3f(-5, 5, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(5, 5, 5)
    glVertex3f(5, 5, 5)
    glVertex3f(-5, 5, 5)
    glVertex3f(-5, 5, 5)
    glVertex3f(-5, 5, -5)
    #Walls
    glVertex3f(-5, 0, -5)
    glVertex3f(-5, 5, -5)
    glVertex3f(5, 0, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(5, 0, 5)
    glVertex3f(5, 5, 5)
    glVertex3f(-5, 0, 5)
    glVertex3f(-5, 5, 5)
    #Door
    glVertex3f(-1, 0, 5)
    glVertex3f(-1, 3, 5)
    glVertex3f(-1, 3, 5)
    glVertex3f(1, 3, 5)
    glVertex3f(1, 3, 5)
    glVertex3f(1, 0, 5)
    #Roof
    glVertex3f(-5, 5, -5)
    glVertex3f(0, 8, -5)
    glVertex3f(0, 8, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(-5, 5, 5)
    glVertex3f(0, 8, 5)
    glVertex3f(0, 8, 5)
    glVertex3f(5, 5, 5)
    glVertex3f(0, 8, 5)
    glVertex3f(0, 8, -5)
    glEnd()

def drawCar():
    glLineWidth(2.5)
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    #Front Side
    glVertex3f(-3, 2, 2)
    glVertex3f(-2, 3, 2)
    glVertex3f(-2, 3, 2)
    glVertex3f(2, 3, 2)
    glVertex3f(2, 3, 2)
    glVertex3f(3, 2, 2)
    glVertex3f(3, 2, 2)
    glVertex3f(3, 1, 2)
    glVertex3f(3, 1, 2)
    glVertex3f(-3, 1, 2)
    glVertex3f(-3, 1, 2)
    glVertex3f(-3, 2, 2)
    #Back Side
    glVertex3f(-3, 2, -2)
    glVertex3f(-2, 3, -2)
    glVertex3f(-2, 3, -2)
    glVertex3f(2, 3, -2)
    glVertex3f(2, 3, -2)
    glVertex3f(3, 2, -2)
    glVertex3f(3, 2, -2)
    glVertex3f(3, 1, -2)
    glVertex3f(3, 1, -2)
    glVertex3f(-3, 1, -2)
    glVertex3f(-3, 1, -2)
    glVertex3f(-3, 2, -2)
    #Connectors
    glVertex3f(-3, 2, 2)
    glVertex3f(-3, 2, -2)
    glVertex3f(-2, 3, 2)
    glVertex3f(-2, 3, -2)
    glVertex3f(2, 3, 2)
    glVertex3f(2, 3, -2)
    glVertex3f(3, 2, 2)
    glVertex3f(3, 2, -2)
    glVertex3f(3, 1, 2)
    glVertex3f(3, 1, -2)
    glVertex3f(-3, 1, 2)
    glVertex3f(-3, 1, -2)
    glEnd()
    
def drawTire():
    glLineWidth(2.5)
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_LINES)
    #Front Side
    glVertex3f(-1, .5, .5)
    glVertex3f(-.5, 1, .5)
    glVertex3f(-.5, 1, .5)
    glVertex3f(.5, 1, .5)
    glVertex3f(.5, 1, .5)
    glVertex3f(1, .5, .5)
    glVertex3f(1, .5, .5)
    glVertex3f(1, -.5, .5)
    glVertex3f(1, -.5, .5)
    glVertex3f(.5, -1, .5)
    glVertex3f(.5, -1, .5)
    glVertex3f(-.5, -1, .5)
    glVertex3f(-.5, -1, .5)
    glVertex3f(-1, -.5, .5)
    glVertex3f(-1, -.5, .5)
    glVertex3f(-1, .5, .5)
    #Back Side
    glVertex3f(-1, .5, -.5)
    glVertex3f(-.5, 1, -.5)
    glVertex3f(-.5, 1, -.5)
    glVertex3f(.5, 1, -.5)
    glVertex3f(.5, 1, -.5)
    glVertex3f(1, .5, -.5)
    glVertex3f(1, .5, -.5)
    glVertex3f(1, -.5, -.5)
    glVertex3f(1, -.5, -.5)
    glVertex3f(.5, -1, -.5)
    glVertex3f(.5, -1, -.5)
    glVertex3f(-.5, -1, -.5)
    glVertex3f(-.5, -1, -.5)
    glVertex3f(-1, -.5, -.5)
    glVertex3f(-1, -.5, -.5)
    glVertex3f(-1, .5, -.5)
    #Connectors
    glVertex3f(-1, .5, .5)
    glVertex3f(-1, .5, -.5)
    glVertex3f(-.5, 1, .5)
    glVertex3f(-.5, 1, -.5)
    glVertex3f(.5, 1, .5)
    glVertex3f(.5, 1, -.5)
    glVertex3f(1, .5, .5)
    glVertex3f(1, .5, -.5)
    glVertex3f(1, -.5, .5)
    glVertex3f(1, -.5, -.5)
    glVertex3f(.5, -1, .5)
    glVertex3f(.5, -1, -.5)
    glVertex3f(-.5, -1, .5)
    glVertex3f(-.5, -1, -.5)
    glVertex3f(-1, -.5, .5)
    glVertex3f(-1, -.5, -.5)
    glEnd()


def display():
    global xdelta
    global ydelta
    global zdelta
    global perspective
    global spacing

    glClear (GL_COLOR_BUFFER_BIT)
    glColor3f (1.0, 1.0, 1.0)
    # viewing transformation 
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if perspective == 1:
        gluPerspective(90,1,1,200)
    else:
        glOrtho(-10,10,-10,10,1,200)



    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    #world to camera    
    glPushMatrix()
    glRotated(-thetadelta - thetahome, 0, 1, 0)
    glTranslated(-xdelta - xhome,-ydelta - yhome,-zdelta - zhome)
    

    drawHouses()

    drawFullCar()


    #pop the world to camera off
    glPopMatrix()
    glFlush ()

def drawHouses():
    #object to world first three houses
    for i in range(0,10):
        glPushMatrix()
        glTranslated(i * spacing,0,0)    
        drawHouse()
        glPopMatrix()

    # side house
    glPushMatrix()
    glTranslated(-spacing,0, spacing)  
    glRotated(90,0,1,0)  
    drawHouse()
    glPopMatrix()  

    # rotate for side houses
    glPushMatrix() 
    glTranslated(0 ,0, 2*spacing) 
    glRotated(180,0,1,0)  
    drawHouse()

    #obect to world oposite side of houses  
    for i in range(0,10):
        glPushMatrix()
        glTranslated(i * -spacing,0,0)    
        drawHouse()
        glPopMatrix()   

    #pop the rotation
    glPopMatrix()

def drawFullCar():

    global cs
    global carDelta
    global tireRot
    #draw the car
    glPushMatrix()
    glTranslated(carDelta, 0, spacing)
    drawCar()


    #draw the tires
    glPushMatrix()
    glTranslated(-cs, 0, cs)
    glRotated(tireRot,0,0,-1)
    drawTire()
    glPopMatrix()

    glPushMatrix()
    glTranslated(-cs, 0, -cs)
    glRotated(tireRot,0,0,-1)
    drawTire()
    glPopMatrix()

    glPushMatrix()
    glTranslated(cs, 0, -cs)
    glRotated(tireRot,0,0,-1)
    drawTire()
    glPopMatrix()

    glPushMatrix()
    glTranslated(cs, 0, cs)
    glRotated(tireRot,0,0,-1)
    drawTire()
    glPopMatrix()

    #Pop the car matrix
    glPopMatrix()

def move(test):
    global carDelta
    global carInc
    global tireRot
    carDelta += carInc
    tireRot += (carInc*180/np.pi)
    display()
    glutPostRedisplay()
    glutTimerFunc(100,move,0)


def keyboard(key, x, y):

    global xdelta
    global zdelta
    global ydelta
    global thetadelta
    global perspective
    global carDelta
    global carInc
    global tireRot
    thetaI = np.pi/180


    if key == chr(27):
        import sys
        sys.exit(0)
  
    # Move Left
    if key == 'a':
        print("a is pressed")
        xdelta -= (1 * np.cos(thetadelta*np.pi/180))
        zdelta += (1 * np.sin(thetadelta*np.pi/180))
        print(xdelta)
        print(ydelta)
        print(zdelta)
        print(thetadelta)
        display()

    # Move Right
    if key == 'd':
        print("d is pressed")
        xdelta += (1 * np.cos(thetadelta*np.pi/180))
        zdelta -= (1 * np.sin(thetadelta*np.pi/180))
        display()

    # Move Forward
    if key == 'w':
        print("w is pressed")
        zdelta -= np.cos(thetadelta*np.pi/180)
        xdelta -= np.sin(thetadelta*np.pi/180)
        display()

    # Move Backward
    if key == 's':
        print("s is pressed")
        zdelta += np.cos(thetadelta*np.pi/180)
        xdelta += np.sin(thetadelta*np.pi/180)
        display()

    # Turn Left
    if key == 'q':
        print("q is pressed")
        thetadelta += 1
        display()

    # Turn Right
    if key == 'e':
        print("e is pressed")
        thetadelta -= 1
        display()

    # Move Up
    if key == 'r':
        print("r is pressed")
        ydelta += 1
        display()
    
    # Move Down
    if key == 'f':
        print("f is pressed")
        ydelta -= 1
        display()

    # Return to Home Position
    if key == 'h':
        print("h is pressed")
        ydelta = 0
        zdelta = 0
        xdelta = 0
        thetadelta = 0
        carDelta = 0
        tireRot = 0

    # Switch to orthographic projection
    if key == 'o':
        print("o is pressed")
        perspective = 0
        display()

    # switch to perspective
    if key == 'p':
        print("p is pressed")
        perspective = 1
        display()

    # move the car
    if key == 'm':
        carDelta += carInc
        tireRot += (carInc*180/np.pi)
        display()

    glutPostRedisplay()


glutInit(sys.argv)
glutInitDisplayMode (GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize (int(DISPLAY_WIDTH), int(DISPLAY_HEIGHT))
glutInitWindowPosition (100, 100)
glutCreateWindow (b'OpenGL Lab')
init ()
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutTimerFunc(500,move,0)
glutMainLoop()
