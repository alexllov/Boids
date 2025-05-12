from Boid import Boid

class Prey(Boid):

    def __init__(self, canvas, xPos, yPos, size,
                 speed, colour, cHeight, cWidth):
          super().__init__(canvas, xPos, yPos, size,
                 speed, colour, cHeight, cWidth)
          
          self.avoidPredatorPressure = 0.05

    def _avoidPredators(self, predators):
        xPos, yPos = 0, 0
        for predator in predators:
            dx = self.xPos - predator.xPos
            dy = self.yPos - predator.yPos
            distanceSquared = (dx * dx) + (dy * dy)
            if distanceSquared <= self.vision * self.vision:
                 xPos += self.xPos - predator.xPos
                 yPos += self.yPos - predator.yPos
        
        self.xVelocity += xPos * self.avoidPredatorPressure
        self.yVelocity += yPos * self.avoidPredatorPressure

    def fly(self, flock, predators):
            """
            Calculates Boid's next position based on update rules & env.

            Keyword Arguments:
            flock: list of all prey boids
            predators: list of all predator boids
            """
            # Coordinates of the boid are set to its current coords on the canvas
            self.coordinates = self.canvas.coords(self.image)

            # Collect ALL relevant info from local flock
            #   & apply velocity changes according to the 3 base rules
            self._analyseLocalFlock(flock)

            ### Add Avoid Predators
            self._avoidPredators(predators)

            # Steer away from edge of screen
            self._avoidEdges()

            # Check speed & limit to self.speed if too high + raise if too low
            self._applySpeedLimit()

            # Move the boid relative to current position
            self.canvas.move(self.image, self.xVelocity, self.yVelocity)

            # Sets the x & y Pos based off of boids new position
            self.xPos, self.yPos = self.canvas.coords(self.image)[0:2]