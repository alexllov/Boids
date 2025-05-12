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
        super().__init__(canvas, xPos, yPos, size,
                         speed, colour, cHeight, cWidth)
        
        # Related to env
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