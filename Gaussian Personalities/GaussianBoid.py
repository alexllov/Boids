from math import sqrt, hypot
import random
from Boid import Boid

class GaussianBoid(Boid):
    """
    Boid object, holds data for each boid.

    Public Methods:
    fly()
    setCanvasSize()
    """
    def __init__(self, canvas, xPos, yPos, size,
                 speed, colour, cHeight, cWidth):
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

        # Related to env
        self.canvas = canvas

        # Related to movement
        self.vision = size * 7
        self.dispersal = size * 1.5
        # Default values = 0.05, 0.05, 0.005
        self.separationFactor = random.gauss(1,0.5)*0.05
        self.alignmentFactor = random.gauss(1,1)*0.05
        self.cohesionFactor = random.gauss(1,1)*0.005

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
        self.xMagnitude = sqrt(self.xVelocity*self.xVelocity)
        # Final side of triangle found using c2 - a2 = b2
        self.yMagnitude = sqrt((speed * speed)
                                    - (self.xMagnitude * self.xMagnitude))
        # yVelocity set to + or - randomly
        flip = random.randint(0,1)
        if flip == 0:
            self.yVelocity = 0 - self.yMagnitude
        else:
            self.yVelocity = self.yMagnitude
