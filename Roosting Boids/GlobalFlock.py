class GlobalFlock():
    def __init__(self, array):
        self.flock = array
        # Cheating by taking a random boid's stats for the first frame
        self.GBCoords = self.flock[0].PBCoords
        self.GBError = self.flock[0].PBError

    def fly(self):
        errors, coords = [], []
        for boidlet in self.flock:
            error, coord = boidlet.fly(self.flock, self.GBCoords)
            errors.append(error)
            coords.append(coord)
        minError = min(errors)
        minErrorIndex = errors.index(minError)
        if minError < self.GBError:
            self.GBError = minError
            self.GBCoords = coords[minErrorIndex]
