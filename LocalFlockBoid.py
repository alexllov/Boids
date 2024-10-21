from collections import Counter
import math
import random
from operator import attrgetter
from operator import itemgetter

class boid:
    def __init__(self, canvas, xPos, yPos, size, speed, colour, cHeight, cWidth):
        """
        Constructor for boid class

        Required Variables: 
        canvas: corresponding tkinter canvas 
        xPos: x position on canvas
        yPos: y position on canvas
        size: INT size of boid
        colour,
        cHeight: height of canvas 
        cWidth: width of canvas

        Derived Variables:
        vision: range around itself in which the boid can 'see' other boids
        dispersal: defines the point where other boids are too close & should be moved away from
        xVelocity
        yVelocity
        xMagnitude
        yMagnitude
        flock
        """
        self.canvas = canvas
        self.xPos = xPos
        self.yPos = yPos
        self.colour = colour
        self.originalColour = colour
        self.size = size
        self.image = canvas.create_oval(xPos,yPos,xPos+size,yPos+size, fill=colour)
        self.speed = speed
        #X & Y Velocities randomly generated based on speed given
        #xVel set to random value between + & - speed
        self.xVelocity = random.uniform(-speed,speed)
        #Velocity squared & square rooted to find the magnitude
        self.xMagnitude = math.sqrt(self.xVelocity*self.xVelocity)
        #Final side of triangle found using c2 - a2 = b2 (rearranged a2 + b2 = c2)
        self.yMagnitude = math.sqrt((speed * speed) - (self.xMagnitude * self.xMagnitude))
        #yVelocity needs to be set to + or -, coin flipped to randomly determine
        #if coin flip = 0, yVelocity set to negative using yVel = 0 - yMagnitude, otherwise yVel = yMag
        flip = random.randint(0,1)
        if flip == 0:
            self.yVelocity = 0 - self.yMagnitude
        else:
            self.yVelocity = self.yMagnitude
        
        self.vision = size * 4
        self.dispersal = size * 1.5
        self.cHeight = cHeight
        self.cWidth = cWidth
        self.flock = []


    def averageVector(self, vectorList):
        """
        Takes list of vectors, returns average vector from them.
        
        Variables: VectorList
        """
        averageXComp = 0
        averageYComp = 0
        for vector in vectorList:
            averageXComp += vector[0]
            averageYComp += vector[1]
        averageXComp = averageXComp/len(vectorList)
        averageYComp = averageYComp/len(vectorList)
        avgVector = (averageXComp, averageYComp)
        return avgVector
    
    def unitizedVector(self, vector):
            """
            Takes a vector, returns the corresponding unit vector

            Variables: vector
            """
            unitCompX = vector[0]/(math.hypot(*vector))
            unitCompY = vector[1]/(math.hypot(*vector)) 
            unitVector = [unitCompX, unitCompY]
            return unitVector
    

    def fly(self, snapshot):
        """
        Takes the boid and a deep copy of the canvas, returns the new position of the boid
        """
        #Coordinates of the boid are set to its current coordinates on the canvas
        self.coordinates = self.canvas.coords(self.image)

        #Wrap Over Canvas Edges
        if self.coordinates[0] >= self.cWidth:
            self.xPos = 0
        if self.coordinates[0] < 0:
            self.xPos = self.cWidth
        if self.coordinates[1] >= self.cHeight:
            self.yPos = 0
        if self.coordinates[1] < 0:
            self.yPos = self.cHeight

        #This moves the boid to its x & y pos after changed during wrap (otherwise it disappears once it goes off the edge)
        ##FROM THE DOCUMENTATION vv - This is distinct from 'move', which alters the x & y val by a given amont,
        ##instead, #moveto' picks it up & sets it t the new co-ordinates given
        ##pathName moveto tagOrId xPos yPos
        ##Move the items given by tagOrId in the canvas coordinate space so that the first coordinate pair (the upper-left corner of the bounding box) of the first item (the lowest in the display list) with tag tagOrId is located at position (xPos,yPos). xPos and yPos may be the empty string, in which case the corresponding coordinate will be unchanged. All items matching tagOrId remain in the same positions relative to each other. This command returns an empty string.
        self.canvas.moveto(self.image, self.xPos, self.yPos)
        self.canvas
        #boid's current vector
        currentVector = [self.xVelocity, self.yVelocity]
        #ALL CHANGES RELYING ON OTHER BOIDS
        #run through all the other boids
        localVectors = []
        localPositions = []
        tooClosePositions = []
        localColours = []

        xSortedSnapshot = sorted(snapshot, key=lambda boidlet: boidlet.xPos)
        xSlice = []
        for boidlet in xSortedSnapshot:
            if self.xPos - self.vision < boidlet.xPos and self.xPos + self.vision > boidlet.xPos:
                xSlice.append(boidlet) 
        xySlice = []
        for boidlet in xSlice:
            if self.yPos - self.vision < boidlet.yPos and self.yPos + self.vision > boidlet.yPos:
                xySlice.append(boidlet)

        #CHECK ALL THE OTHER BOIDS & GATHER RELEVANT INFO
        for boidlet in xySlice:
            #set some variables from the other boid to compare from
            otherXPos = boidlet.xPos
            otherYPos = boidlet.yPos
            otherCoords = (otherXPos, otherYPos)
            #otherCoords = [otherXPos, otherYPos]
            otherVector = (boidlet.xVelocity, boidlet.yVelocity)
            xDistance = otherXPos - self.xPos
            yDistance = otherYPos - self.yPos
            trueDistance = math.sqrt((xDistance * xDistance)+(yDistance * yDistance))
            #COLLECT POSITIONS OF LOCAL FLOCK
            if trueDistance <= self.vision and boidlet != self:
                localVectors.append(otherVector)
                #THIS gets colours for old => Avg colour in sight (currently not used)
                localColours.append(boidlet.colour)
                if trueDistance > self.dispersal:
                    localPositions.append(otherCoords)
                #COLLECT POSITIONS OF THOSE TOO CLOSE
                elif trueDistance <= self.dispersal:
                    tooClosePositions.append(otherCoords)

        finalPressures = []
        self.canvas.itemconfig(self.image,fill=self.originalColour)

        #CALC AVG DIRECTION OF LOCAL FLOCK + add to averagedPressures list
        if len(localVectors) > 0:
            #ALL LOCAL VECTORS ARE ADDED TO PRESSURE TO ENCOURAGE MOVING FORWARDS
            for vector in localVectors:
                finalPressures.append(vector)
        
        #CALC AVG POSITION OF LOCAL FLOCK
        if len(localPositions) > 0:
            avgLocalPosition = self.averageVector(localPositions)
            #Work out dist to that position
            xToLocalCentre = avgLocalPosition[0]
            yToLocalCentre = avgLocalPosition[1]
            vectorXComp = xToLocalCentre - self.xPos
            vectorYComp = yToLocalCentre - self.yPos
            #Vector to that position is calculated & added to averagedPressures
            #Only one Vector is added here as its to move towards a single point
            vectorToLocalCentre = (vectorXComp, vectorYComp)
            finalPressures.append(vectorToLocalCentre)

        #CALC THE VELOCITY AWAY FROM THOSE TOO CLOSE & FIND AVG
        if len(tooClosePositions) > 0:
            for tooClose in tooClosePositions:
                #The vectors away from each boid too close is calculated
                vectorXComp = self.xPos - tooClose[0]
                vectorYComp = self.yPos - tooClose[1]
                vectorAwayFromTooClose = (vectorXComp, vectorYComp)
                #These are each appended to pressures, so that moving away from each boids matters
                finalPressures.append(vectorAwayFromTooClose)

        #SET NEW VECTOR
        if len(finalPressures) > 0:
            #print(finalPressures)
            #i, average pressures are averaged out into the desired vector
            desiredVector = self.averageVector(finalPressures)

            #2, Average of Desired & Current is found & newVector is set to that
            newXComp = (desiredVector[0] + currentVector[0])/2
            newYComp = (desiredVector[1] + currentVector[1])/2
            newVector = [newXComp, newYComp]
        else:
            newVector = [currentVector[0],currentVector[1]]

        #Current Vector set to the new vector
        currentVector = [newVector[0], newVector[1]]
        #Check speed & limit @ self.speed
        if math.sqrt(currentVector[0]**2 + currentVector[1]**2) > self.speed:
            #unit the vector, then mult by speed
            currentVector = self.unitizedVector(currentVector)
            currentVector[0] = currentVector[0] * self.speed
            currentVector[1] = currentVector[1] * self.speed

        #I dont know why, but TK moves the boid circles by +1,+1 (ie if xVel = 0, it will still move +1)
        #This throws off all the velocities, so these counter that
        xMove = currentVector[0] - 1
        yMove = currentVector[1] - 1
        
        #This moves the boid, "by adding x amount to the x axis & y amount...", THIS is why xVelocity & yVel... are needed 
        self.canvas.move(self.image, xMove, yMove)

        #Sets the x & y Pos based off of boids new position, otherwise they just jiggle around one spot
        self.xPos, self.yPos = self.canvas.coords(self.image)[0:2]

        ##CHANGE COLOUR BASED ON BOID SPEED
        currentSpeed = math.sqrt(currentVector[0]**2 + currentVector[1]**2)
        if currentSpeed > (self.speed / 5)*4:
            self.colour = "red"
        elif currentSpeed > (self.speed / 5)*3:
            self.colour = "yellow"
        elif currentSpeed > (self.speed / 5)*2:
            self.colour = "green"
        elif currentSpeed > (self.speed / 5):
            self.colour = "blue"
        else:
            self.colour = "purple"
        #Change the colour of a drawn item after drawing
        self.canvas.itemconfig(self.image,fill=self.colour)


