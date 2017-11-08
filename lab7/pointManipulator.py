import numpy as np 


class pointManipulator:
    '''
        Model the physical system
    '''

    def __init__(self):
        self = self

    def translationMatrix(self, x, y, z=1):
        '''
            Returns a translation matrix
        '''
        
        return np.matrix([[1, 0, 0, x],[0, 1, 0, y],[0, 0, 1, z],[0, 0, 0, 1]])

    def xRotation(self, theta):
        '''
            Returns a rotation matrix about x
        '''

        thetaRad = 2*np.pi*theta/360
        return np.matrix([[1, 0, 0, 0],[0, np.cos(thetaRad), -np.sin(thetaRad), 0],[0, np.sin(thetaRad), np.cos(thetaRad), 0],[0, 0, 0, 1]])

    def yRotation(self,theta):
        '''
            Returns a rotation matrix about y: cos(thetaRad) sin(thetaRad)
        '''

        thetaRad = 2*np.pi*theta/360
        return np.matrix([[np.cos(thetaRad), 0, np.sin(thetaRad), 0],[0, 1, 0, 0],[-np.sin(thetaRad), 0, np.cos(thetaRad), 0],[0, 0, 0, 1]])

    def zRotation(self,theta):
        '''
            Returns a rotation matrix about y: cos(thetaRad) sin(thetaRad)
        '''

        thetaRad = 2*np.pi*theta/360
        return np.matrix([[np.cos(thetaRad), -np.sin(thetaRad), 0, 0],[np.sin(thetaRad), np.cos(thetaRad), 0, 0],[0, 0, 1, 0],[0, 0, 0, 1]])
