from Boid import Boid

class Predator(Boid):

    def __init__(self, canvas, xPos, yPos, size,
                 speed, colour, cHeight, cWidth):
          super().__init__(canvas, xPos, yPos, size,
                 speed, colour, cHeight, cWidth)
    
    def fly(self, prey, predators):
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
        flock = [*prey, *predators]
        self._analyseLocalFlock(flock)

        # Steer away from edge of screen
        self._avoidEdges()

        # Check speed & limit to self.speed if too high + raise if too low
        self._applySpeedLimit()

        # Move the boid relative to current position
        self.canvas.move(self.image, self.xVelocity, self.yVelocity)

        # Sets the x & y Pos based off of boids new position
        self.xPos, self.yPos = self.canvas.coords(self.image)[0:2]