# Import a library of functions called 'pygame'
import pygame
from math import pi
import numpy as np
from pointManipulator import pointManipulator

DISPLAY_WIDTH = 512
DISPLAY_HEIGHT = 512
zhome = 0
global zdelta
zdelta = 0

xhome = 0
global xdelta
xdelta = 0

yhome = 0
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

fov = np.pi/2
zoomx = 1.0/(np.tan(fov/2))
zoomy = zoomx
f = 100.0
n = 1.0

global clipMat
clipMat = np.matrix([[zoomx, 0, 0, 0], [0, zoomy, 0, 0], [0, 0, (f+n)/(f-n), -2*n*f/(f-n)], [0, 0, 1, 0]])
#projectionMat = np.matrix([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,1/f,0]])
global screenSpace_mat
screenSpace_mat = np.matrix([[DISPLAY_WIDTH/2, 0, DISPLAY_WIDTH/2], [0, -DISPLAY_HEIGHT/2, DISPLAY_HEIGHT/2], [0, 0, 1]])

global transMat
transMat = []

class Point:
	def __init__(self,x,y):
		self.x = x
		self.y = y

class Point3D:
	def __init__(self,x,y,z):
		self.x = x
		self.y = y
		self.z = z
		
class Line3D():
	
	def __init__(self, start, end):
		self.start = start
		self.end = end

def loadOBJ(filename):
	
	vertices = []
	indices = []
	lines = []
	
	f = open(filename, "r")
	for line in f:
		t = str.split(line)
		if not t:
			continue
		if t[0] == "v":
			vertices.append(Point3D(float(t[1]),float(t[2]),float(t[3])))
			
		if t[0] == "f":
			for i in range(1,len(t) - 1):
				index1 = int(str.split(t[i],"/")[0])
				index2 = int(str.split(t[i+1],"/")[0])
				indices.append((index1,index2))
			
	f.close()
	
	#Add faces as lines
	for index_pair in indices:
		index1 = index_pair[0]
		index2 = index_pair[1]
		lines.append(Line3D(vertices[index1 - 1],vertices[index2 - 1]))
		
	#Find duplicates
	duplicates = []
	for i in range(len(lines)):
		for j in range(i+1, len(lines)):
			line1 = lines[i]
			line2 = lines[j]
			
			# Case 1 -> Starts match
			if line1.start.x == line2.start.x and line1.start.y == line2.start.y and line1.start.z == line2.start.z:
				if line1.end.x == line2.end.x and line1.end.y == line2.end.y and line1.end.z == line2.end.z:
					duplicates.append(j)
			# Case 2 -> Start matches end
			if line1.start.x == line2.end.x and line1.start.y == line2.end.y and line1.start.z == line2.end.z:
				if line1.end.x == line2.start.x and line1.end.y == line2.start.y and line1.end.z == line2.start.z:
					duplicates.append(j)
					
	duplicates = list(set(duplicates))
	duplicates.sort()
	duplicates = duplicates[::-1]
	
	#Remove duplicates
	for j in range(len(duplicates)):
		del lines[duplicates[j]]
	
	return lines

def loadHouse():
    house = []
    #Floor
    house.append(Line3D(Point3D(-5, 0, -5), Point3D(5, 0, -5)))
    house.append(Line3D(Point3D(5, 0, -5), Point3D(5, 0, 5)))
    house.append(Line3D(Point3D(5, 0, 5), Point3D(-5, 0, 5)))
    house.append(Line3D(Point3D(-5, 0, 5), Point3D(-5, 0, -5)))
    #Ceiling
    house.append(Line3D(Point3D(-5, 5, -5), Point3D(5, 5, -5)))
    house.append(Line3D(Point3D(5, 5, -5), Point3D(5, 5, 5)))
    house.append(Line3D(Point3D(5, 5, 5), Point3D(-5, 5, 5)))
    house.append(Line3D(Point3D(-5, 5, 5), Point3D(-5, 5, -5)))
    #Walls
    house.append(Line3D(Point3D(-5, 0, -5), Point3D(-5, 5, -5)))
    house.append(Line3D(Point3D(5, 0, -5), Point3D(5, 5, -5)))
    house.append(Line3D(Point3D(5, 0, 5), Point3D(5, 5, 5)))
    house.append(Line3D(Point3D(-5, 0, 5), Point3D(-5, 5, 5)))
    #Door
    house.append(Line3D(Point3D(-1, 0, 5), Point3D(-1, 3, 5)))
    house.append(Line3D(Point3D(-1, 3, 5), Point3D(1, 3, 5)))
    house.append(Line3D(Point3D(1, 3, 5), Point3D(1, 0, 5)))
    #Roof
    house.append(Line3D(Point3D(-5, 5, -5), Point3D(0, 8, -5)))
    house.append(Line3D(Point3D(0, 8, -5), Point3D(5, 5, -5)))
    house.append(Line3D(Point3D(-5, 5, 5), Point3D(0, 8, 5)))
    house.append(Line3D(Point3D(0, 8, 5), Point3D(5, 5, 5)))
    house.append(Line3D(Point3D(0, 8, 5), Point3D(0, 8, -5)))
	
    return house

def loadCar():
    car = []
    #Front Side
    car.append(Line3D(Point3D(-3, 2, 2), Point3D(-2, 3, 2)))
    car.append(Line3D(Point3D(-2, 3, 2), Point3D(2, 3, 2)))
    car.append(Line3D(Point3D(2, 3, 2), Point3D(3, 2, 2)))
    car.append(Line3D(Point3D(3, 2, 2), Point3D(3, 1, 2)))
    car.append(Line3D(Point3D(3, 1, 2), Point3D(-3, 1, 2)))
    car.append(Line3D(Point3D(-3, 1, 2), Point3D(-3, 2, 2)))

    #Back Side
    car.append(Line3D(Point3D(-3, 2, -2), Point3D(-2, 3, -2)))
    car.append(Line3D(Point3D(-2, 3, -2), Point3D(2, 3, -2)))
    car.append(Line3D(Point3D(2, 3, -2), Point3D(3, 2, -2)))
    car.append(Line3D(Point3D(3, 2, -2), Point3D(3, 1, -2)))
    car.append(Line3D(Point3D(3, 1, -2), Point3D(-3, 1, -2)))
    car.append(Line3D(Point3D(-3, 1, -2), Point3D(-3, 2, -2)))
    
    #Connectors
    car.append(Line3D(Point3D(-3, 2, 2), Point3D(-3, 2, -2)))
    car.append(Line3D(Point3D(-2, 3, 2), Point3D(-2, 3, -2)))
    car.append(Line3D(Point3D(2, 3, 2), Point3D(2, 3, -2)))
    car.append(Line3D(Point3D(3, 2, 2), Point3D(3, 2, -2)))
    car.append(Line3D(Point3D(3, 1, 2), Point3D(3, 1, -2)))
    car.append(Line3D(Point3D(-3, 1, 2), Point3D(-3, 1, -2)))

    return car

def loadTire():
    tire = []
    #Front Side
    tire.append(Line3D(Point3D(-1, .5, .5), Point3D(-.5, 1, .5)))
    tire.append(Line3D(Point3D(-.5, 1, .5), Point3D(.5, 1, .5)))
    tire.append(Line3D(Point3D(.5, 1, .5), Point3D(1, .5, .5)))
    tire.append(Line3D(Point3D(1, .5, .5), Point3D(1, -.5, .5)))
    tire.append(Line3D(Point3D(1, -.5, .5), Point3D(.5, -1, .5)))
    tire.append(Line3D(Point3D(.5, -1, .5), Point3D(-.5, -1, .5)))
    tire.append(Line3D(Point3D(-.5, -1, .5), Point3D(-1, -.5, .5)))
    tire.append(Line3D(Point3D(-1, -.5, .5), Point3D(-1, .5, .5)))

    #Back Side
    tire.append(Line3D(Point3D(-1, .5, -.5), Point3D(-.5, 1, -.5)))
    tire.append(Line3D(Point3D(-.5, 1, -.5), Point3D(.5, 1, -.5)))
    tire.append(Line3D(Point3D(.5, 1, -.5), Point3D(1, .5, -.5)))
    tire.append(Line3D(Point3D(1, .5, -.5), Point3D(1, -.5, -.5)))
    tire.append(Line3D(Point3D(1, -.5, -.5), Point3D(.5, -1, -.5)))
    tire.append(Line3D(Point3D(.5, -1, -.5), Point3D(-.5, -1, -.5)))
    tire.append(Line3D(Point3D(-.5, -1, -.5), Point3D(-1, -.5, -.5)))
    tire.append(Line3D(Point3D(-1, -.5, -.5), Point3D(-1, .5, -.5)))

    #Connectors
    tire.append(Line3D(Point3D(-1, .5, .5), Point3D(-1, .5, -.5)))
    tire.append(Line3D(Point3D(-.5, 1, .5), Point3D(-.5, 1, -.5)))
    tire.append(Line3D(Point3D(.5, 1, .5), Point3D(.5, 1, -.5)))
    tire.append(Line3D(Point3D(1, .5, .5), Point3D(1, .5, -.5)))
    tire.append(Line3D(Point3D(1, -.5, .5), Point3D(1, -.5, -.5)))
    tire.append(Line3D(Point3D(.5, -1, .5), Point3D(.5, -1, -.5)))
    tire.append(Line3D(Point3D(-.5, -1, .5), Point3D(-.5, -1, -.5)))
    tire.append(Line3D(Point3D(-1, -.5, .5), Point3D(-1, -.5, -.5)))
    
    return tire

################################################################################################## Helper Functions

def getCan(point):
	global clipMat
	#print 'input point'
	#print point

	#print 'clip mat'
	#print clipMat

	newPoint = clipMat * point
	divisor = newPoint[3]
	#print 'new point1'
	#print newPoint

	newPoint = newPoint / divisor
	#print 'new point2'
	#print newPoint

	#print 'divisor'
	#print divisor

	return newPoint

def checkFrust(bPoint, ePoint):
	begin = True
	end = True
	# neither point can be in front of near plane
	if bPoint[2] < -1:
		return False
	if ePoint[2] < -1:
		return False
	
	if ePoint[0] < -1 and bPoint[0] < -1:
		return False

	if ePoint[0] > 1 and bPoint[0] > 1:
		return False

	if ePoint[1] < -1 and bPoint[1] < -1:
		return False

	if ePoint[1] > 1 and bPoint[1] > 1:
		return False

	if ePoint[2] < -1 and bPoint[2] < -1:
		return False

	if ePoint[2] > 1 and bPoint[2] > 1:
		return False

	return True



def display():
    global xdelta
    global ydelta
    global zdelta
    global transMat
    
    translate = manip.translationMatrix(-xhome-xdelta,-yhome-ydelta,-zhome-zdelta)
	rotation = manip.yRotation(-thetahome-thetadelta)
	world2Cam_mat = rotation*translate


######################################################################################
# Initialize the game engine
pygame.init()
 
# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

# Set the height and width of the screen
size = [DISPLAY_WIDTH, DISPLAY_HEIGHT]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Shape Drawing")
 
#Set needed variables
done = False
clock = pygame.time.Clock()
start = Point(0.0,0.0)
end = Point(0.0,0.0)
linelist = loadHouse()

manip = pointManipulator()

#Loop until the user clicks the close button.
while not done:
 
	

	# This limits the while loop to a max of 100 times per second.
	# Leave this out and we will use all CPU we can.
	clock.tick(10)

	# Clear the screen and set the screen background
	screen.fill(BLACK)



	#Controller Code#
	#####################################################################

	for event in pygame.event.get():
		if event.type == pygame.QUIT: # If user clicked close
			done=True
			
	pressed = pygame.key.get_pressed()


	# Move Left
	if pressed[pygame.K_a]:
		print("a is pressed")
		xdelta -= (1 * np.cos(thetadelta*np.pi/180))
		zdelta += (1 * np.sin(thetadelta*np.pi/180))
		print(xdelta)
		print(ydelta)
		print(zdelta)
		print(thetadelta)


	# Move Right
	if pressed[pygame.K_d]:
		print("d is pressed")
		xdelta += (1 * np.cos(thetadelta*np.pi/180))
		zdelta -= (1 * np.sin(thetadelta*np.pi/180))


	# Move Forward
	if pressed[pygame.K_w]:
		print("w is pressed")
		zdelta -= np.cos(thetadelta*np.pi/180)
		xdelta -= np.sin(thetadelta*np.pi/180)


	# Move Backward
	if pressed[pygame.K_s]:
		print("s is pressed")
		zdelta += np.cos(thetadelta*np.pi/180)
		xdelta += np.sin(thetadelta*np.pi/180)


	# Turn Left
	if pressed[pygame.K_q]:
		print("q is pressed")
		thetadelta += 1


	# Turn Right
	if pressed[pygame.K_e]:
		print("e is pressed")
		thetadelta -= 1


	# Move Up
	if pressed[pygame.K_r]:
		print("r is pressed")
		ydelta += 1


	# Move Down
	if pressed[pygame.K_f]:
		print("f is pressed")
		ydelta -= 1


	# Return to Home Position
	if pressed[pygame.K_h]:
		print("h is pressed")
		ydelta = 0
		zdelta = 0
		xdelta = 0
		thetadelta = 0
		carDelta = 0
		tireRot = 0

	#Viewer Code#
	#####################################################################
	display()
	# Build the world to camera transformation matrix




	#BOGUS DRAWING METHOD SO YOU CAN SEE THE HOUSE WHEN YOU START UP
	for s in linelist:
		##### world to camera
		worldStart = np.matrix([[s.start.x],[s.start.y],[s.start.z],[1]])
		worldEnd = np.matrix([[s.end.x],[s.end.y],[s.end.z],[1]])
		cameraStart = world2Cam_mat * worldStart
		cameraEnd = world2Cam_mat * worldEnd

		##### get canotical points
		canStart = getCan(cameraStart)
		canEnd = getCan(cameraEnd)

		##### check if line is within frustrum
		isInside = checkFrust(canStart, canEnd)
		print canStart
		print canEnd
		print isInside

		canStart = canStart[0:3]
		canStart[2] = 1
		canEnd = canEnd[0:3]
		canEnd[2] = 1

		if isInside == True:
			screenStart = screenSpace_mat * canStart
			screenEnd = screenSpace_mat * canEnd
			pygame.draw.line(screen, BLUE, (screenStart[0], screenStart[1]), (screenEnd[0], screenEnd[1]))
		#pygame.draw.line(screen, BLUE, (20*s.start.x+200, -20*s.start.y+200), (20*s.end.x+200, -20*s.end.y+200))

	# Go ahead and update the screen with what we've drawn.
	# This MUST happen after all the other drawing commands.
	pygame.display.flip()
 
# Be IDLE friendly
pygame.quit()
