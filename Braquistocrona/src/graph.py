from xturtle import *
from realCurve import *

width = 800
height = 600

turtle = Pen()
turtle.winsize(width+50, height+50, -10, 10) 
turtle.tracer(False)

def maxMax(array):
    max=-2
    
    for i in xrange(1,len(array),2):
        if array[i]>max:
            max = array[i]
            
    return max

def plotGraph(array, turtle, color):
    turtle.color(color)
    turtle.goto(array[0],array[1])
    turtle.pensize(2)
    turtle.pendown()
    for i in xrange(2,len(array),2):
        turtle.goto(array[i],array[i+1])
    turtle.penup()

def scalePoints(x,y,realX,realY,oldPoints,n):

    points = [j for j in oldPoints]
    
    for i in range(0,n,2):
        if points[i] != 0:
            points[i] = ((realX*points[i]/x))
        points[i]-=realX/2

        if points[i+1] != 0:
            points[i+1] = ((realY*points[i+1]/y))
        points[i+1]-=realY/2
        
    return points

def drawGraph(curveFinder):
    ''' plot '''
    turtle.clearscreen()

    turtle.pensize(3)
    turtle.speed(10)
    turtle.penup()
    turtle.hideturtle()
    
    ''' draw axes '''
    turtle.goto(-width/2,height/2)
    turtle.pendown()
    turtle.goto(-width/2,0)
    turtle.goto(width/2,0)
    turtle.goto(-width/2,0)
    turtle.goto(-width/2,-height/2)
    turtle.goto(width/2,-height/2)
    turtle.penup()
    
    _, L2 = brachistochroneReal(curveFinder.hBegin[0], curveFinder.hBegin[1], curveFinder.hEnd[0], curveFinder.hEnd[1], curveFinder.noPoints+1) 
    
    ''' scale all points '''
    points = scalePoints(curveFinder.hEnd[0],curveFinder.hBegin[1],width,height/2,curveFinder.population[0].points,curveFinder.noPoints*2+4)
    L2 = scalePoints(curveFinder.hEnd[0],curveFinder.hBegin[1],width,height/2,L2,len(L2))
    
    
    if curveFinder.currentGeneration>curveFinder.plotOn:
        maxH = maxMax(curveFinder.plotMax)
        medPoints = scalePoints(curveFinder.numberGenerations,maxH,width,height/2,curveFinder.plotMed,len(curveFinder.plotMed))
        minPoints = scalePoints(curveFinder.numberGenerations,maxH,width,height/2,curveFinder.plotMin,len(curveFinder.plotMin))
        maxPoints = scalePoints(curveFinder.numberGenerations,maxH,width,height/2,curveFinder.plotMax,len(curveFinder.plotMax))
        
    #draw in the top graph
    for i in xrange(1,len(points),2):
        points[i]+=height/4
        L2[i]+=height/4
    
    if curveFinder.currentGeneration>curveFinder.plotOn:
        #draw in the bottom graph
        for i in xrange(1,len(medPoints),2):
            medPoints[i]-=height/4
            minPoints[i]-=height/4
            maxPoints[i]-=height/4
        
    ''' draw curve '''
    plotGraph(points,turtle, 'red')
    
    ''' draw real curve '''
    plotGraph(L2,turtle, 'blue')
        
    ''' draw Min Med Max '''
    if curveFinder.currentGeneration>curveFinder.plotOn:
        plotGraph(medPoints,turtle,'red')
        plotGraph(minPoints,turtle, 'green')
        plotGraph(maxPoints,turtle, 'green')
        
    turtle.color('black')
    turtle.penup()
    turtle.goto(width/2-80,height/2-20)
    turtle.write("gen: "+str(curveFinder.currentGeneration+10),font=('Arial', 12, 'bold'))
    
    turtle.update()

