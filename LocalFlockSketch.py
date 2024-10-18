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
speed = 3
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

#divide the screen into 9 overlapping quarters
#flock becomes an array of 9 arrays, each holding all the boids within one "quarter" of the screen
#@ start of fly(), a boid's vision area is measured & we determine all of the "buckets" it can see into
#All future comparrisons are made against the boids in those baskets, thus reducing the amount of comparisons
 

#for boidlet in boids:
#    boidlet.flock = boids
def flockFly():
    snapshotFlock = boids[:]
    for boidlet in boids:
        boidlet.fly(snapshotFlock)
    canvas.after(1, flockFly)

flockFly()

#Run boidlet fly, have it return position. Use position to assign it to a quadrant of the screen
#[(-1.2132070587298869, -2.7437435435273425), (11.07896248125013, -7.636728685370592)]
#[(-2.8318384157378973, -0.9902985343577336), (-12.196602589196402, 4.612880626516947)]
#[(-1.2132070587298869, -2.7437435435273425), (-9.173349159810414, 5.68652854248252)]
#[(-2.8318384157378973, -0.9902985343577336), (-11.702309713784302, 5.464365367741422)]
#[(-1.2132070587298869, -2.7437435435273425), (-8.615844599748158, 6.527537836641791)]
#[(-2.8318384157378973, -0.9902985343577336), (-11.674768086191648, 6.220271423135692)]
#[(-1.2132070587298869, -2.7437435435273425), (-8.473106091566763, 7.281593558510046)]
#[(-2.8318384157378973, -0.9902985343577336), (-11.58743669223955, 7.77295903905339)]


##def flockFly():
#    snapshotFlock = boids
#    newSnapshot = (boidlet.fly(snapshotFlock) for boidlet in boids)
#    snapshotFlock = list(newSnapshot)
#    canvas.after(10, flockFly())



#This is the main loop that updates the tkinter window.
window.mainloop()




#Old idea was using the snapshot & determining distances, then sorting that to whittle down who to compare to
#HOWEVER, this means EVERY BOID IS STILL comparing itself to every other, so would not actually save time