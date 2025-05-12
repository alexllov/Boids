from SoloRoostBoid import SoloRoostBoid

class GlobalRoostBoid(SoloRoostBoid):
    """
    RoostBoid object, holds data for each roosting boid.

    Changed Methods:
    init()
    fly()
    """

    def __init__(self, canvas, xPos, yPos, size,
                 speed, colour, cHeight, cWidth, roost):
        super().__init__(canvas, xPos, yPos, size,
                         speed, colour, cHeight, cWidth, roost)

        # Global Best
        self.GBRoostFactor = 0.01

    def fly(self, boids, globalBestCoords):
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

        # Steer towards GB coords from Global Flock
        dx = globalBestCoords[0] - self.xPos
        dy = globalBestCoords[1] - self.yPos
        self.xVelocity += dx *self.GBRoostFactor
        self.yVelocity += dy *self.GBRoostFactor

        # Check speed & limit to self.speed if too high + raise if too low
        self._applySpeedLimit()

        # Move the boid relative to current position
        self.canvas.move(self.image, self.xVelocity, self.yVelocity)

        # Sets the x & y Pos based off of boids new position
        self.xPos, self.yPos = self.canvas.coords(self.image)[0:2]

        # Return how well the boid has done to update globals
        return self.PBError, self.PBCoords