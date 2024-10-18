from collections import Counter
import math
import random
from operator import attrgetter
from operator import itemgetter

#create the class boids
class boid:
    #this is the initial setup of the boid, __init__ gives all the initial data needed to create one
    #self.x = x attributes the x property of the boid to the data entered in that category on generation
    #self.image = canvas.create_oval <- draws the ovals that are each individual boid
    #def __init__(self, canvas, xPos, yPos, xVelocity, yVelocity, direction, colour, cHeight, cWidth):
    def __init__(self, canvas, xPos, yPos, size, speed, vision, dispersal, colour, cHeight, cWidth):
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
        #Velocity squared & square rooted to remove the sign (+ or -), giving the pure magnitude
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
        
        self.vision = vision
        self.dispersal = dispersal
        self.cHeight = cHeight
        self.cWidth = cWidth
        self.flock = []

    #def average(self, lst): return sum(lst)/len(lst)

    def averageVector(self, vectorList):
        #Take in Vector List, split it up into a list of X & Ys, find avg of each, return those two combined
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
            unitCompX = vector[0]/(math.hypot(*vector))
            unitCompY = vector[1]/(math.hypot(*vector)) 
            unitVector = (unitCompX, unitCompY)
            return unitVector
    

    def fly(self, snapshot):
        def average(lst): return sum(lst)/len(lst)
        #Coordinates of the boid are set to its current coordinates on the canvas
        self.coordinates = self.canvas.coords(self.image)

        #✔✔✔✔✔✔✔✔✔✔✔✔✔✔✔✔
        #WRAP OFF EDGES
        #Boid's position is checked, if it is at any edge of the canvas, it is wrapped to the opposite edge
        if self.coordinates[0] >= self.cWidth:
            self.xPos = 0
        if self.coordinates[0] < 0:
            self.xPos = self.cWidth
        if self.coordinates[1] >= self.cHeight:
            self.yPos = 0
        if self.coordinates[1] < 0:
            self.yPos = self.cHeight

        #✔✔✔✔✔✔✔✔✔✔✔✔✔✔✔✔
        #This moves the boid to its x & y pos after changed during wrap (otherwise it disappears once it goes off the edge)
        ##FROM THE DOCUMENTATION vv - This is distinct from 'move', which alters the x & y val by a given amont,
        ##instead, #moveto' picks it up & sets it t the new co-ordinates given
        ##pathName moveto tagOrId xPos yPos
        ##Move the items given by tagOrId in the canvas coordinate space so that the first coordinate pair (the upper-left corner of the bounding box) of the first item (the lowest in the display list) with tag tagOrId is located at position (xPos,yPos). xPos and yPos may be the empty string, in which case the corresponding coordinate will be unchanged. All items matching tagOrId remain in the same positions relative to each other. This command returns an empty string.
        self.canvas.moveto(self.image, self.xPos, self.yPos)
        self.canvas


        #Make a tuple of the boid's current vector
        currentVector = [self.xVelocity, self.yVelocity]
        


        #ALL CHANGES RELYING ON OTHER BOIDS
        #run through all the other boids
        localVectors = []
        localSpeeds = []
        localPositions = []
        tooClosePositions = []
        localColours = []


############################################################################################
############################################################################################
############################################################################################

#The idea of this section is to create a smaller list for each boid to make comparisons to in order to save time,
#However, looking at it, surely its still each boid comparing all the others to itself? only now in 2 steps so even worse?
#Unless I can somehow sort by hypot & then axe those outside of view? - BUT THAT IS COMPARING THE BOID TO ALL OTHERS!!!!
#I believe this approach is fundamentally flawed

#        #Slicing down the whole flock to the local group
#        #flock sorted by x coordinate
#        xSortedSnapshot = sorted(snapshot, key=lambda boidlet: boidlet.xPos)
#        #new array of boids made from all with x coordainate in range of vision from boid's x position
#        xSlice = xSortedSnapshot[int(self.xPos-self.vision):int(self.xPos+self.vision)]
#        print (len(xSortedSnapshot), len(xSlice))
#        ySortedxSlice = sorted(xSlice, key=lambda boidlet: boidlet.yPos)
#        xySlice = ySortedxSlice[int(self.xPos-self.vision):int(self.xPos+self.vision)]
#        #if len(ySortedxSlice) > 0:
#        #    print("Boidlet is at", self.xPos, self.yPos, "array info:", ySortedxSlice[0].xPos,ySortedxSlice[0].yPos)



        xSortedSnapshot = sorted(snapshot, key=lambda boidlet: boidlet.xPos) #key=attrgetter('xPos'))
        #xSlice = xSortedSnapshot[int(self.xPos-self.vision):int(self.xPos+self.vision)]
        #print (len(xSortedSnapshot), len(xSlice))
        #ySortedxSlice = sorted(xSlice, key=lambda boidlet: boidlet.yPos)
        #xySlice = ySortedxSlice[int(self.xPos-self.vision):int(self.xPos+self.vision)]
        sadXSlice = []
        for boidlet in xSortedSnapshot:
            if self.xPos - self.vision < boidlet.xPos and self.xPos + self.vision > boidlet.xPos:
                sadXSlice.append(boidlet) 
        sadXYSlice = []
        for boidlet in sadXSlice:
            if self.yPos - self.vision < boidlet.yPos and self.yPos + self.vision > boidlet.yPos:
                sadXYSlice.append(boidlet)

############################################################################################
############################################################################################
############################################################################################


        #CHECK ALL THE OTHER BOIDS & GATHER RELEVANT INFO
        for boidlet in sadXYSlice:
            #set some variables from the other boid to compare from
            otherXPos = boidlet.xPos
            otherYPos = boidlet.yPos
            otherCoords = (otherXPos, otherYPos)
            #otherCoords = [otherXPos, otherYPos]
            otherVector = (boidlet.xVelocity, boidlet.yVelocity)
            xDistance = otherXPos - self.xPos
            yDistance = otherYPos - self.yPos
            trueDistance = math.sqrt((xDistance * xDistance)+(yDistance * yDistance))
            #COLLECT DIRECTIONS OF LOCAL FLOCK
            #COLLECT POSITIONS OF LOCAL FLOCK
            #print("CHECKING LOCAL")
            if trueDistance <= self.vision and boidlet != self:
                localVectors.append(otherVector)
            #    print("FRIEND FOUND!")
                localColours.append(boidlet.colour)
                #Little check to see if they're all going @ the proper speed
                #localSpeeds.append(math.sqrt((otherVector[0]*otherVector[0])+(otherVector[1]*otherVector[1])))
                if trueDistance > self.dispersal:
                    localPositions.append(otherCoords)
                #USE THIS TO HAVE THE BOIDS GET COLOUR OF WHAT THEY SEE
                #localColours.append(boidlet.colour)
                #COLLECT POSITIONS OF THOSE TOO CLOSE
                if trueDistance <= self.dispersal:
                    tooClosePositions.append(otherCoords)



        finalPressures = []
        #desiredVector = ()

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
            vectorsAway = []
            for tooClose in tooClosePositions:
                #The vectors away from each boid too close is calculated
                vectorXComp = self.xPos - tooClose[0]
                vectorYComp = self.yPos - tooClose[1]
                vectorAwayFromTooClose = (vectorXComp, vectorYComp)
                #These are each appended to pressures, so that moving away from each boids matters
                finalPressures.append(vectorAwayFromTooClose)


        #SET NEW VECTOR
        #go thru averagedPressures to set final desiredVector
        #find average between desiredVector & currentVector, then set currentVector to that
        #1, Calc desired vector
        if len(finalPressures) > 0:
            #print(finalPressures)
            #i, average pressures are averaged out into the desired vector
            desiredVector = self.averageVector(finalPressures)

            #ii, desired vector is turned into a unit vector
            unitDesiredVector = self.unitizedVector(desiredVector)
            #✔✔ unitDesiredVector works correctly

            #iii, current vector is turned into a unit vector
            unitCurrentVector = self.unitizedVector(currentVector)
            #✔✔ unitCurrentVector works correctly

            #2, Average of Desired & Current is found & newVector is set to that
            newXComp = (unitDesiredVector[0] + unitCurrentVector[0])/2
            newYComp = (unitDesiredVector[1] + unitCurrentVector[1])/2
            newVector = (newXComp, newYComp)

            #i, New Vector is set to a unit vector
            unitNewVector = self.unitizedVector(newVector)
            #✔✔ unitNewVector works correctly

            #Remember to multiply it back so that they move @ th right speed
            speededNewVector = (unitNewVector[0]*self.speed, unitNewVector[1]*self.speed)

            #By making a unit vector, we set the ratio of x:y to move the correct amount to go z distance
            #Then unitVector*speed scales those movements so that they move @ the boids proper speed
        else:
            speededNewVector = (currentVector[0],currentVector[1])
            #print (math.sqrt((speededNewVector[0]**2)+(speededNewVector[1]**2)))

        #Current Vector set to the new vector, scaled to the speed limit
        currentVector = speededNewVector
        #currentSpeed = math.hypot(*currentVector)
        #print(currentSpeed)


        #I dont know why, but TK moves the boid circles by +1,+1 (ie if xVel = 0, it will still move +1)
        #This throws off all the velocities, so these counter that
        xMove = currentVector[0] - 1
        yMove = currentVector[1] - 1
        

        #This moves the boid, "by adding x amount to the x axis & y amount...", THIS is why xVelocity & yVel... are needed 
        ## FROM THE DOCUMENTATION vv
        ##pathName move tagOrId xAmount yAmount
        ##Move each of the items given by tagOrId in the canvas coordinate space by adding xAmount to the x-coordinate of each point associated with the item and yAmount to the y-coordinate of each point associated with the item. This command returns an empty string.
        self.canvas.move(self.image, xMove, yMove)

        #Sets the x & y Pos based off of boids new position, otherwise they just jiggle around one spot
        ##This is because the next time it moves it checks its position (which was never reset), sp moves from there again
        ##The new info is taken from self.image, taking the first two itelf from the list as defined in ___init___ > image = canvas.create_oval(xPos,yPos,xPos+8,yPos+8,fill=colour) 
        ##The : 'slice' defines the start and end points to look at, here start at 0, then end at the last entry before 2, ie, self.image[0,1], which are xPos & yPos respectively
        self.xPos, self.yPos = self.canvas.coords(self.image)[0:2]

        ##CHANGE COLOUR TO DOMINANT COLOUR OF BOIDS IN SIGHT
        if len(localColours) > 0:
            #local colours counted up and ordered according to occurance
            colourCounter = Counter(localColours)
            #dominant colour set to the most common colour, done by organising the list of counted colours
            dominantColour = colourCounter.most_common()[0][0]
            self.colour = dominantColour
            #Change the colour of a drawn item after drawing
            self.canvas.itemconfig(self.image,fill=self.colour)

