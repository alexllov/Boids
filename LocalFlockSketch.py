from tkinter import *
from tkinter import messagebox
from LocalFlockBoid import *
import time
import random
from copy import deepcopy

#Determine size of window
HEIGHT = 500
WIDTH = 700

#Set up the window w/ Tkinter, set canvas size
window = Tk()
canvas = Canvas(window, bg="black", width=WIDTH,height=HEIGHT)
window.resizable(height = True, width = True)
canvas.pack()

#Create empty list of boids
boids = []

#Functions to determine the details for each boid
def gen_xPos(): return random.uniform(0,WIDTH)
def gen_yPos(): return random.uniform(0,HEIGHT)
colours = ["white", "red", "orange", "yellow", "green", "blue", "purple", "pink"]
def gen_colour(): return random.choice(colours)
size = 8
speed = 4
vision = size * 4
dispersal = size * 1.5

#Create all the boids & fill empty boids list w/ them
#All the functions set up earlier are called to generate the necessary information for the boid
##as seen in 'def __init__(self,canvas,xPos,yPos,xVelocity,yVelocity,color, cHeight, cWidth)'
for x in range(300):
    ##Old boid has x&yVelocities set for it & fixed
    #x = boid(canvas,gen_xPos(), gen_yPos(), gen_xVel(), gen_yVel(), gen_direction(), gen_colour(), HEIGHT, WIDTH)
    x = boid(canvas,gen_xPos(), gen_yPos(), size, speed, vision, dispersal, gen_colour(), HEIGHT, WIDTH)
    boids.append(x)

#for boidlet in boids:
#    boidlet.flock = boids
def flockFly():
    snapshotFlock = boids[:]
    for boidlet in boids:
        boidlet.fly(snapshotFlock)
    canvas.after(1, flockFly)

flockFly()
#This is the main loop that updates the tkinter window.
window.mainloop()
