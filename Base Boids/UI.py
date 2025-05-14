from tkinter import *
from Flock import Flock


def createChangeHandler(attribute):
    """Helper func for creating slider's commands."""
    def changeHandler(val):
        val = float(val)
        for boidlet in flock:
            setattr(boidlet, attribute, val)
    return changeHandler

def createSlider(panel, label, attribute, from_, to, initial, resolution=1):
    """Func to create Slider obj to control a given attribute."""
    frame = Frame(panel, bg="white")
    frame.pack(side="left", padx=20)
    Label(frame, text=label, bg="white", fg="grey").pack(pady=10)
    slider = Scale(
        frame,
        from_=from_,
        to=to,
        orient=HORIZONTAL,
        command=createChangeHandler(attribute),
        resolution=resolution
    )
    slider.set(initial)
    slider.pack()
    return slider

def onResize(event):
    """Event listener to update boids when canvas size changes."""
    newDimensions = (event.width, event.height)
    for boidlet in flock.boids:
        boidlet.setCanvasSize(newDimensions)

def flockFly():
    """Core loop to have all boids in flock obj fly."""
    flock.fly()
    canvas.after(1, flockFly)

# Set up the window, canvas, & controls
HEIGHT = 500
WIDTH = 700
window = Tk()
window.title("Boids")
window.geometry(f"{WIDTH}x{HEIGHT}")
window.resizable(height=True, width=True)

outerFrame = Frame(window)
outerFrame.pack(fill="both", expand=True)

canvas = Canvas(outerFrame, bg="black", width=WIDTH,height=HEIGHT*0.8)
canvas.pack(side="top", fill="both", expand=True)

controlPanel = Frame(outerFrame, bg="white", width=WIDTH, height=HEIGHT*0.2)
controlPanel.pack(side="bottom", fill="x")

# Bind the resize event to the on_resize function 
canvas.bind("<Configure>", onResize)

# Create flock of boids
flock = Flock(canvas, WIDTH, HEIGHT, num=200)

speed = flock[0].speed
speedSlider = createSlider(controlPanel, "Speed", "speed", 1, 10, speed)

alignment = flock[0].alignmentFactor
alignmentSlider = createSlider(controlPanel, "Alignment", "alignmentFactor", 0.0, 0.1, alignment, 0.01)

separation = flock[0].separationFactor
separationSlider = createSlider(controlPanel, "Separation", "separationFactor", 0.0, 0.1, separation, 0.01)

cohesion = flock[0].cohesionFactor
cohesionSlider = createSlider(controlPanel, "Cohesion", "cohesionFactor", 0.0, 0.01, cohesion, 0.001)

flockFly()

window.mainloop()
