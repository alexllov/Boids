

class Roost:
    """
    Roost object...
    """
    def __init__(self, canvas, xPos, yPos, size):
        self.canvas = canvas
        self.xPos = xPos
        self.yPos = yPos
        self.colour = "white"
        self.originalColour = "white"
        self.size = size
        self.image = canvas.create_oval(xPos,yPos, xPos+size,
                                        yPos+size, fill="white")
        