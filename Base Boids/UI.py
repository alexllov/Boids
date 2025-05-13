from tkinter import *
from Boid import Boid
import random

# Determine size of window
HEIGHT = 500
WIDTH = 700

# Set up the window w/ Tkinter, set canvas size
window = Tk()
window.title("Boids")
window.geometry(f"{WIDTH}x{HEIGHT}")
window.resizable(height = True, width = True)

outerFrame = Frame(window)
outerFrame.pack(fill="both", expand=True)

canvas = Canvas(outerFrame, bg="black", width=WIDTH,height=HEIGHT*0.8)
canvas.pack(side="top", fill="both", expand=True)

controlPanel = Frame(outerFrame, bg="white", width=WIDTH, height=HEIGHT*0.2)
controlPanel.pack(side="bottom", fill="x")

def on_resize(event): 
    newDimensions = (event.width, event.height)
    for boidlet in boids:
        boidlet.setCanvasSize(newDimensions)

# Bind the resize event to the on_resize function 
canvas.bind("<Configure>", on_resize) 

# Functions to determine the details for each boid
def gen_xPos(): return random.uniform(0,WIDTH)
def gen_yPos(): return random.uniform(0,HEIGHT)
colours = ["red", "orange", "yellow", "green", "blue", "purple"]
def gen_colour(): return random.choice(colours)
size = 8
speed = 4

#Create all the boids
boids = []
for x in range(200):
    x = Boid(canvas, gen_xPos(), gen_yPos(), size,
             speed, gen_colour(), HEIGHT, WIDTH)
    boids.append(x)

# Collect Pressure Defaults
alignment = boids[0].alignmentFactor
separation = boids[0].separationFactor
cohesion = boids[0].cohesionFactor


def flockFly():
    for boidlet in boids:
        boidlet.fly(boids)
    canvas.after(1, flockFly)

def changeSpeed(val):
    speed = float(val)
    for boidlet in boids:
        boidlet.speed = speed

def changeAlignment(val):
    alignment = float(val)
    for boidlet in boids:
        boidlet.alignmentFactor = alignment

def changeSeparation(val):
    separation = float(val)
    for boidlet in boids:
        boidlet.separationFactor = separation

def changeCohesion(val):
    cohesion = float(val)
    for boidlet in boids:
        boidlet.cohesionFactor = cohesion

speedFrame = Frame(controlPanel, bg="white")
speedFrame.pack(side="left", padx=20)
Label(speedFrame, text="Speed", bg="white", fg="grey").pack(pady=10)
speedSlider = Scale(speedFrame, from_=1, to=10, orient=HORIZONTAL, command=changeSpeed)
speedSlider.set(speed)
speedSlider.pack()

alignmentFrame = Frame(controlPanel, bg="white")
alignmentFrame.pack(side="left", padx=20)
Label(alignmentFrame, text="Alignment", bg="white", fg="grey").pack(pady=10)
alignmentSlider = Scale(alignmentFrame, from_=0.0, to=0.1, orient=HORIZONTAL, command=changeAlignment, resolution=0.01)
alignmentSlider.set(alignment)
alignmentSlider.pack()

separationFrame = Frame(controlPanel, bg="white")
separationFrame.pack(side="left", padx=20)
Label(separationFrame, text="Separation", bg="white", fg="grey").pack(pady=10)
separationSlider = Scale(separationFrame, from_=0.0, to=0.1, orient=HORIZONTAL, command=changeSeparation, resolution=0.01)
separationSlider.set(separation)
separationSlider.pack()

cohesionFrame = Frame(controlPanel, bg="white")
cohesionFrame.pack(side="left", padx=20)
Label(cohesionFrame, text="Cohesion", bg="white", fg="grey").pack(pady=10)
cohesionSlider = Scale(cohesionFrame, from_=0.0, to=0.01, orient=HORIZONTAL, command=changeCohesion, resolution=0.001)
cohesionSlider.set(cohesion)
cohesionSlider.pack()

flockFly()
#This is the main loop that updates the tkinter window.
window.mainloop()
