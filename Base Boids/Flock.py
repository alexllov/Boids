from Boid import Boid
import random

class Flock():
    """
    Container obj to hold 'Boids'.

    Public Methods:
    fly()
    """
    def __init__(self, canvas, WIDTH, HEIGHT, num=200):
        """
        Flock obj constructor.

        Args:
        canvas: Tkinter Canvas obj
        WIDTH: INT, canvas width
        HEIGHT: INT, canvas height
        num: INT number of boids to create
        """
        def gen_xPos(): return random.uniform(0,WIDTH)
        def gen_yPos(): return random.uniform(0,HEIGHT)
        colours = ["red", "orange", "yellow", "green", "blue", "purple"]
        def gen_colour(): return random.choice(colours)
        size = 8
        speed = 4

        self.boids = []
        for x in range(200):
            x = Boid(canvas, gen_xPos(), gen_yPos(), size,
                    speed, gen_colour(), HEIGHT, WIDTH)
            self.boids.append(x)
    
    def __getitem__(self, i):
        return self.boids[i]

    def fly(self):
        """Calls the fly() func of all boids within the flock."""
        for boidlet in self.boids:
            boidlet.fly(self.boids)