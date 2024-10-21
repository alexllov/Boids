from tkinter import *
from tkinter import messagebox
from LocalFlockBoid import *
import time
import random

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
colours = ["red", "orange", "yellow", "green", "blue", "purple"]
def gen_colour(): return random.choice(colours)
size = 8
speed = 4

#Create all the boids & fill empty boids list with them
for x in range(400):
    x = boid(canvas, gen_xPos(), gen_yPos(), size,
             speed, gen_colour(), HEIGHT, WIDTH)
    boids.append(x)

def flockFly():
    for boidlet in boids:
        boidlet.fly(boids)
    canvas.after(1, flockFly)

flockFly()
#This is the main loop that updates the tkinter window.
window.mainloop()
