import math
import random
from Boid import Boid

class SoloRoostBoid(Boid):
    """
    RoostBoid object, holds data for each roosting boid.

    Changed Methods:
    init()
    fly()
    """

    def __init__(self, canvas, xPos, yPos, size,
                 speed, colour, cHeight, cWidth, roost):
        """
        Constructor for boid class.

        Keyword Arguments:
        Required:
        canvas: corresponding tkinter canvas 
        xPos: x position on canvas
        yPos: y position on canvas
        size: INT size of boid
        colour,
        cHeight: height of canvas 
        cWidth: width of canvas

        Derived Args:
        vision: range around itself in which the boid can 'see' other boids
        dispersal: defines the point where other boids are too close
                   & should be moved away from
        xVelocity
        yVelocity
        xMagnitude
        yMagnitude
        """

        # Related to movement
        self.vision = size * 7
        self.dispersal = size * 1.5
        # Default values = 0.05, 0.05, 0.005
        self.separationFactor = 0.05
        self.alignmentFactor = 0.05
        self.cohesionFactor = 0.005

        # Related to self
        self.xPos = xPos
        self.yPos = yPos
        self.colour = colour
        self.cHeight = cHeight
        self.cWidth = cWidth
        self.size = size
        self.image = canvas.create_oval(xPos,yPos, xPos+size,
                                        yPos+size, fill=colour)
        self.speed = speed

        # X & Y Velocities randomly generated based on speed given
        self.xVelocity = random.uniform(-speed,speed)
        # Velocity squared & square rooted to find the magnitude
        self.xMagnitude = math.sqrt(self.xVelocity*self.xVelocity)
        # Final side of triangle found using c2 - a2 = b2
        self.yMagnitude = math.sqrt((speed * speed)
                                    - (self.xMagnitude * self.xMagnitude))
        # yVelocity set to + or - randomly
        flip = random.randint(0,1)
        if flip == 0:
            self.yVelocity = 0 - self.yMagnitude
        else:
            self.yVelocity = self.yMagnitude
        
        # Related to env
        self.canvas = canvas
        self.roost = roost
        # Personal Best
        self.PBCoords = [xPos, yPos]
        self.PBError = self._calcError(roost)
        self.BPRoostFactor = 0.01
    
    def _calcError(self, objectB):
        x1, y1 = self.xPos, self.yPos
        x2, y2 = objectB.xPos, objectB.yPos
        xd = x1 - x2
        yd = y1 - y2
        hypot = (xd**2) + (yd**2)
        return hypot
    
    def _PBRoostSteer(self):
        dx = self.PBCoords[0] - self.xPos
        dy = self.PBCoords[1] - self.yPos
        self.xVelocity += dx *self.BPRoostFactor
        self.yVelocity += dy *self.BPRoostFactor
    
    def _updatePB(self):
        newDist = self._calcError(self.roost)
        if newDist < self.PBError:
            self.PBError = newDist
            self.PBCoords = [self.xPos, self.yPos]

    def fly(self, boids):
        """
        Takes the boid and a deep copy of the canvas, 
        moves the boid based on the update rules and pressures.

        Keyword Arguments:
        boids: list of all boids
        """
        # Coordinates of the boid are set to its current coords on the canvas
        self.coordinates = self.canvas.coords(self.image)

        # Collect ALL relevant info from local flock
        #   & apply velocity changes according to the 3 base rules
        self._analyseLocalFlock(boids)

        # Steer away from edge of screen
        self._avoidEdges()

        # Steer towards PB from roost & update PB
        self._PBRoostSteer()
        self._updatePB()

        # Check speed & limit to self.speed if too high + raise if too low
        self._applySpeedLimit()

        # Move the boid relative to current position
        self.canvas.move(self.image, self.xVelocity, self.yVelocity)

        # Sets the x & y Pos based off of boids new position
        self.xPos, self.yPos = self.canvas.coords(self.image)[0:2]