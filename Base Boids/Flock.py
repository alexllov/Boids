from Boid import Boid
import random

class Flock():
    def __init__(self, canvas, WIDTH, HEIGHT, num=200):
        def gen_xPos(): return random.uniform(0,WIDTH)
        def gen_yPos(): return random.uniform(0,HEIGHT)
        colours = ["red", "orange", "yellow", "green", "blue", "purple"]
        def gen_colour(): return random.choice(colours)
        size = 8
        speed = 4

        #Create all the boids
        self.boids = []
        for x in range(200):
            x = Boid(canvas, gen_xPos(), gen_yPos(), size,
                    speed, gen_colour(), HEIGHT, WIDTH)
            self.boids.append(x)
    
    def __getitem__(self, i):
        return self.boids[i]

    def fly(self):
        for boidlet in self.boids:
            boidlet.fly(self.boids)