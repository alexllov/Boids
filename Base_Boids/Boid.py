from math import sqrt, hypot
import random

class Boid:
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

    def setCanvasSize(self, canvasDimensions):
        """
        Setter function applied when canvas size is changed

        Keyword Arguments:
        canvasDimensions
        """
        self.cWidth = canvasDimensions[0]
        self.cHeight = canvasDimensions[1]
    
    def _unitizedVector(self, vector):
        """
        Takes a vector, returns the corresponding unit vector.

        Keyword Arguments: 
        vector
        """
        unitCompX = vector[0]/(hypot(*vector))
        unitCompY = vector[1]/(hypot(*vector)) 
        unitVector = [unitCompX, unitCompY]
        return unitVector

    def _avoidEdges(self):
        """Adjusts boid's velocity to steer away from the edge of the env."""
        margin = 10
        steerPressure = 1
        # Wrap Over Canvas Edges
        if self.xPos >= self.cWidth-margin:
            self.xVelocity -= steerPressure
        elif self.xPos <= margin:
            self.xVelocity += steerPressure
        if self.yPos >= self.cHeight-margin:
            self.yVelocity -= steerPressure
        elif self.yPos <= margin:
            self.yVelocity += steerPressure
    
    def _analyseLocalFlock(self, flock):
        """
        Finds boids within vision range, calculates alignment, coherence,
        and separation velocities based on the others, and updates velocities
        accordingly.

        Takes: flock
        """
        localFlock, tooClose = [], []
        xVel, yVel, xPos, yPos, closeDx, closeDy = 0, 0, 0, 0, 0, 0
        for boidlet in flock:
            if boidlet is self:
                continue
            dx = boidlet.xPos - self.xPos
            dy = boidlet.yPos - self.yPos
            distanceSquared = (dx * dx) + (dy * dy)
            if distanceSquared <= self.vision * self.vision:
                # Within Sight but not too close
                # Align & Converge
                localFlock.append(boidlet)
                xVel += boidlet.xVelocity
                yVel += boidlet.yVelocity
                xPos += boidlet.xPos
                yPos += boidlet.yPos

            if distanceSquared <= self.dispersal * self.dispersal:
                # Too Close => Separate
                tooClose.append(boidlet)
                closeDx += self.xPos - boidlet.xPos
                closeDy += self.yPos - boidlet.yPos

        # Separate
        self.xVelocity += closeDx * self.separationFactor
        self.yVelocity += closeDy * self.separationFactor
        
        if len(localFlock) > 0:
            # Align
            xVel = xVel/len(localFlock)
            yVel = yVel/len(localFlock)
            self.xVelocity += xVel * self.alignmentFactor
            self.yVelocity += yVel * self.alignmentFactor
            # Converge
            xPos = xPos/len(localFlock) - self.xPos
            yPos = yPos/len(localFlock) - self.yPos
            self.xVelocity += xPos * self.cohesionFactor
            self.yVelocity += yPos * self.cohesionFactor

    def _applySpeedLimit(self):
        """
        Sets upper and lower bounds for boid speed to ensure they continue
        moving, but don't exceed a preset limit. Scales the current vectors.
        """
        trueVel = sqrt(self.xVelocity**2 + self.yVelocity**2)
        currentVector = [self.xVelocity, self.yVelocity]
        # Upper Bound
        if trueVel > self.speed:
            # Unit the vector, then mult by speed
            currentVector = self._unitizedVector(currentVector)
            currentVector[0] = currentVector[0] * self.speed
            currentVector[1] = currentVector[1] * self.speed
        # Lower Bound
        elif trueVel < self.speed/5:
            # Unit the vector, then mult by speed
            currentVector = self._unitizedVector(currentVector)
            currentVector[0] = currentVector[0] * self.speed/5
            currentVector[1] = currentVector[1] * self.speed/5
        self.xVelocity = currentVector[0]
        self.yVelocity = currentVector[1]
    
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

        # Check speed & limit to self.speed if too high + raise if too low
        self._applySpeedLimit()

        # Move the boid relative to current position
        self.canvas.move(self.image, self.xVelocity, self.yVelocity)

        # Sets the x & y Pos based off of boids new position
        self.xPos, self.yPos = self.canvas.coords(self.image)[0:2]


## Devolved Features

    def _checkEdgeWrap(self):
        """
        An alternate edge behaviour to allow boids to wrap over the screen.
        """
        # Wrap Over Canvas Edges
        if self.coordinates[0] >= self.cWidth:
            self.xPos = 0
        if self.coordinates[0] < 0:
            self.xPos = self.cWidth
        if self.coordinates[1] >= self.cHeight:
            self.yPos = 0
        if self.coordinates[1] < 0:
            self.yPos = self.cHeight
        # Move boid to its x & y pos after changed during wrap 
        self.canvas.moveto(self.image, self.xPos, self.yPos)