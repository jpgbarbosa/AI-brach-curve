"""
Introduction to Artifical Intelligence
Second Project
By:
  Ivo Daniel Venhuizen Correia no 2008110814
  Joao Pedro Gaioso Barbosa no 200811830

"""

# The necessary imports.
from operator import attrgetter
from random import Random
from BrachFitness import calcBrachTime
from xturtle import *
from math import sqrt
from graph import drawGraph
from numpy import *

EPSLON = 0.000000001

# A class that represents the individual.
class Individual():
    def __init__( self, points, fitness ):
        self.points = points
        self.fitness = fitness
        # Used in the roullete selection.
        self.probFitness = 0
    
    def getFitness( self ):
        return self.fitness

    def setFitness( self, v):
        self.fitness = v

    def getPoints( self ):
        return self.points

    def setPoints( self, p):
        self.points = p
    

# The main class that will hold the genetic algorithm.
class BrachistochroneCurve():

    def __init__( self , hB=[1,0], hE=[0,1]):
        self.hBegin =  hB                   # The coordinates of the starting point. 
        self.hEnd = hE                      # The coordinates of the end point.
        self.noPoints = 10                   # The number of points the list will hold
        self.pointsList = []                # The list that will hold all the points.
        self.sizePopulation = 0             # The size of the population.
        self.population = []
        self.sizeTournament = 0
        self.mutationProb = 0
        self.crossOverProb = 0
        self.sizeCrossOver = 0
        self.numberGenerations = 0
        self.parentsElitism = 0
        self.mutationPerc = 0
        self.eliType = 1
        self.plotOn = 10
        
        self.useXandY = 1
        self.useCrossOverPercentage = True

        self.useCrossover = True
        self.useMutation = True
        self.useSelectionParents = 2 #0- n usar 1- tournament 2- roulette
        self.useElitism = True
        self.printPopulation = True
        
        ''' gui vars '''
        self.currentGeneration = 0
        self.plot = True
        
        ''' Random Seeds '''
        self.rCO = Random()
        self.rTS = Random()
        self.rRWS = Random()
        self.rM = Random()
        self.rNPCO = Random()
        self.rIP = Random()
        self.rMnewPoint = Random()
        
        self.rCO.seed(1)
        self.rTS.seed(2)
        self.rRWS.seed(3)
        self.rM.seed(4)
        self.rNPCO.seed(5)
        self.rIP.seed(6)
        self.rMnewPoint.seed(7)
        
        self.useUniform = True
                
    # We could initialize all of these attributes by the __init__ method, but then
    # it gets too confusing when we want to change a single parameter.            
    def setNoPoints(self, v):
        self.noPoints = v
        
    def increaseSeeds(self,v):
        self.rCO.seed(1+v)
        self.rTS.seed(2+v)
        self.rRWS.seed(3+v)
        self.rM.seed(4+v)
        self.rNPCO.seed(5+v)
        self.rIP.seed(6+v)
        self.rMnewPoint.seed(7+v)

    def setParentsElitismPerc(self, v):
        self.parentsElitism = float(float(v)/100)

    def setSizePopulation(self, v):
        self.sizePopulation = v

    def setSizeTournament(self, v):
        self.sizeTournament = v
        
    def setEliType(self, v):
        self.eliType = v
    
    def getEliType(self):
        return self.eliType
    
    def setStartPoint(self, v):
        self.hBegin = v
    
    def setEndPoint(self, v):
        self.hEnd = v
        
    ''' Prob of suffering Mutation '''
    def setMutationProb(self, v):
        self.mutationProb = float(float(v)/100)
    def getMutationProb(self):
        return self.mutationProb

    ''' Percentage of Mutations '''
    def setMutationPerc(self, v):
        self.mutationPerc = float(float(v)/100)
    def getMutationPerc(self):
        return self.mutationPerc
    
    ''' Prob of suffering Crossover '''
    def setCrossOverProb(self, v):
        self.crossOverProb = float(float(v)/100)
    def getCrossOverProb(self):
        return self.crossOverProb

    ''' Crossover Size Percentage '''
    def setCrossOverSizePerc(self, v):
        self.crossOverSizePerc = float(float(v)/100)
    def getCrossOverSizePerc(self):
        return self.crossOverSizePerc
    def getCrossOverPoints(self):
        return int(self.crossOverSizePerc*100)
    
    ''' Number of Generations '''
    def setNumberGenerations(self, v):
        self.numberGenerations = v
    def getNumberGenerations(self):
        return self.numberGenerations
    
    ''' Given one parent, it returns a new copy of it '''
    def cloneParent (self, individual):
        points = []
        for i in individual.points:
            points.append(i)
        return Individual(points,0)


    def bestCurve(self):

        # If the starting point is at a lower point than the end point,
        # it's useless to start the algorithm because the ball won't ever
        # finish the trail.
        if self.hBegin[1] < self.hEnd[1]:
            print "The answer is obvious. The ball can't get there..."
            return;

        #print "Has started..."
        self.createPopulation()
        self.plotMin=[]#[0 for _ in xrange(self.numberGenerations)]
        self.plotMax=[]#[0 for _ in xrange(self.numberGenerations)]
        self.plotMed=[]#[0 for _ in xrange(self.numberGenerations)]
        
        self.retMin = []
        self.retMax = []
        self.retMed = []
        self.retStDev = []
        
        '''
        x=arange(self.currentGeneration)
        line=pylab.plot(x,plotMed,'r-',x,plotMin,'g-',x,plotMax,'g-')
        pylab.show()
        '''
        # Starts the algorithm itself for a given number of generations.
        for i in xrange(self.numberGenerations):
            self.currentGeneration = i
            
            # If we are using cross over, we will produce two individuals at a time.
            if self.useCrossover:
                limit = self.sizePopulation / 2
            else:
                limit = self.sizePopulation

            # Now, it's time to produce the next generation.
            newGen = []

            # We will need these values for the roulette selection.
            if (self.useSelectionParents == 2):
                #Minimization Problem: 1 / (1 + fitness)
                totalFitness = 0
                   
                # First, we find the total fitness.
                for member in self.population:
                    totalFitness += (1/(1 + member.fitness))

                # Then, we divide th fitness of each individual by the total fitness.
                for member in self.population:
                    member.probFitness = (1/(1 + member.fitness)) / totalFitness
            
                
            for _ in xrange(limit):
                # We have to select two parents to the crossover.
                parentOne = None
                parentTwo = None
                
                #useSelection = 2
                
                if(self.useSelectionParents == 1):
                    # Select parents by tournament selection.
                    parentOne = self.tournamentSelection()
                    parentTwo = self.tournamentSelection()
                elif (self.useSelectionParents == 2):
                    # Select parents by roulette selection.
                    parentOne = self.rouletteWheelSelection()
                    parentTwo = self.rouletteWheelSelection()
                    
                else:
                    pass

                sonOne = self.cloneParent(parentOne);
                sonTwo = self.cloneParent(parentTwo);
                    
                #crossover
                if( self.useCrossover ):
                    if self.rCO.random() < self.getCrossOverProb():
                        self.crossOver(sonOne , sonTwo)
                            
                if ( self.useMutation ):
                    self.mutation(sonOne)
                    self.mutation(sonTwo)

                newGen.extend([sonOne, sonTwo]);            
            
            # evaluate the newGeneration
            for i in newGen:
                i.fitness=calcBrachTime(i.points)

            newGen.sort(key = attrgetter('fitness'))
            self.population.sort(key = attrgetter('fitness'))

            # We select the individual that will survive to the next generation.
            if( self.useElitism ):
                self.elitism(self.population, newGen)
                            
            self.plotMed.append(self.currentGeneration)
            avg=self.avg()
            self.plotMed.append(avg)
            self.retMed.append(avg)
            
            min,max=self.findMinAndMaxFit()
            
            self.plotMin.append(self.currentGeneration)
            self.plotMin.append(min)
            
            self.plotMax.append(self.currentGeneration)
            self.plotMax.append(max)
            
            self.retMin.append(min)
            self.retMax.append(max)
            self.retStDev.append(self.stDev(avg))
            
            if self.plot and self.currentGeneration%self.plotOn==0:
                drawGraph(self)
            
        if (self.printPopulation):
            #self.printPopulation()
            print "\nBEST INDIVIDUAL:"
            self.printIndividual(self.population[0])        
        
        
        return [self.population[0].fitness,self.population[0].points,self.retMin,self.retMed,self.retMax,self.retStDev] 
        
                
    """ The parent selection methods. """
    def tournamentSelection( self ):
        #Gets a sample from the whole population.
        tournament = self.rTS.sample(self.population,self.sizeTournament)
        #Sorts it => minimization problem.
        tournament.sort(key = attrgetter('fitness'))
        #Returns the best individual.
        return tournament[0]

    """def rouletteWheelSelection( self ):
        totalFitness = 0
        
        for member in self.population:
            totalFitness += (1/(member.fitness))
             
        relFitness = [(1/f.fitness)/totalFitness for f in self.population]
        # Generate probability intervals for each individual
        probs = [sum(relFitness[:i+1]) for i in xrange(self.sizePopulation)]
        
        for (i, individual) in enumerate(self.population):
            if self.rRWS.random() <= probs[i]:
                return individual"""
    
    def rouletteWheelSelection( self ):
        # We have already calculated  the total fitness and the partial
        # fitness of each individual before.

        # After choosing a random number, we will sum the probabilities of each
        # individual till we get the desired probability.
        randomProb = self.rRWS.random();
        sumProbs = 0;

        for i in xrange(len(self.population)):
            sumProbs += self.population[i].probFitness
            if sumProbs >= randomProb:
                return self.population[i]


    """ Survivers selection. """
    def elitism( self, parents, newGen ):
        if self.eliType == 1:
            parentsPoints = int(self.parentsElitism*len(parents))
            newGenPoints = int((1-self.parentsElitism)*len(newGen))
            
            self.population = parents[:parentsPoints] + newGen[:newGenPoints]
            
        elif self.eliType == 2:            
            self.population = parents + newGen
            self.population.sort(key = attrgetter('fitness'))
            self.population = self.population[:(self.sizePopulation/2)]
            
        elif self.eliType == 3:
            self.population = newGen
            
        self.population.sort(key = attrgetter('fitness'))

        
    #Mutation in percentagePoints
    def mutation(self, ind):
        #TODO: gaussiana
        
        if(self.useUniform):
            for i in xrange(3,self.noPoints*2+2,2):
                if self.rM.random() < self.getMutationProb():
                    # Mutates the y coordiante.
                    #TODO: check if this is correct
                    ind.points[i] = self.rMnewPoint.uniform(self.hEnd[1]-self.hEnd[0]/2,self.hBegin[1])
                    if self.useXandY==1:
                        # Mutates the x coordinate. The minimum distance will be EPSLON.
                        ind.points[i-1] = (ind.points[i+1] - ind.points[i-3] - 2*EPSLON)*self.rMnewPoint.random() + ind.points[i-3] + EPSLON
        else:
            for i in xrange(3,self.noPoints*2+2,2):
                if self.rM.random() < self.getMutationProb():
                    x=ind.points[i]+self.rMnewPoint.gauss(0,(self.hBegin[1]-self.hEnd[1])/10)
                    while x >= self.hBegin[1]:
                        x=ind.points[i]+self.rMnewPoint.gauss(0,(self.hEnd[1]-self.hEnd[0])/10)
                    ind.points[i] = x
            pass
        '''
        npoints = int(self.getMutationPerc() * self.noPoints)
        
        for _ in xrange(npoints):
            point = randint(0,self.noPoints - 1)*2+3
            # We can only have values smaller than the initial height.                
            ind.points[point] = random()*self.hBegin[1]
        
        '''
        
        return ind
        

    #N-Point Crossover
    def crossOver(self, individuo1, individuo2):
        
        tam = self.noPoints*2

        # We have to multiply by two because each point occupies two positions
        # in the array, for x and y.
        if self.useCrossOverPercentage:
            recPoints = int(self.getCrossOverSizePerc()*self.noPoints)
        else:
            recPoints = self.getCrossOverPoints()
            if recPoints >= self.noPoints:
                print "You are trying to use more crossover points than the available! recPoints set to zero."
                recPoints = 0
    
        chosen = [-1 for i in xrange(recPoints)]
        num = 0
        
        for i in xrange(recPoints):
            while num in chosen:
                # We are only looking for even indexes, corresponding to the x
                # coordinate. randrange as an exclusive left range, so we ought
                # to use tam + 3 if you want reach the last point before the
                # final point.
                num = self.rNPCO.randrange(2, tam + 3, 2)
            chosen[i] = num
    
        chosen.sort()
    
        prev = 0
        for i in xrange(recPoints):
            # Now, as we don't have a fixed x partition, we need to verify if the cross points are compatible.
            # To do this we look at the current points and their neighbours.
            individuo1.points[prev:chosen[i]], individuo2.points[prev:chosen[i]] = individuo2.points[prev:chosen[i]], individuo1.points[prev:chosen[i]]
            prev = chosen[i]
        
        self.xCoordSelectionSortInd(individuo1)
        self.xCoordSelectionSortInd(individuo2)

        return [individuo1, individuo2]

    """ The methods to initialize the genetic algorithm. """
    # Creates a single individual.
    # This individual  has a fixed partition for its x coordinate.
    def createIndividualFixedPartition( self ):
        # This individual will have as many points as we have defined.
        points = []
        interval = (self.hEnd[0] - self.hBegin[0]) / ((self.noPoints + 1) * 1.0)

        #Appends the initial point.
        points.extend([self.hBegin[0], self.hBegin[1]])
                      
        for i in xrange(self.noPoints):
            # Each position will hold an array with the y position.
            # The x position is given by the number of the point.
            # We won't accept values lower than 0, at least, in the beginning.
            points.extend([interval * (i+1), self.rIP.random()*self.hBegin[1]])

        #Appends the final point.
        points.extend([self.hEnd[0], self.hEnd[1]])
                
        individual = Individual(points,0)
        individual.setFitness(calcBrachTime(individual.points))
        
        return individual

    # Given a size of the population, it creates that same population.
    
    def createPopulation( self ):
        self.population = [self.createIndividualFixedPartition() for _ in range(self.sizePopulation)]
                
    """ STATISTICS """
    def avg(self):
        sum = 0.0
        for i in self.population:
            sum += i.fitness
                    
        return sum/self.sizePopulation

    def stDev(self, med=None):
        if med==None:
            med = self.avg()
            
        sum=0.0
        
        for ind in self.population:
            if ind.fitness < med:
                sum += ((ind.fitness-med)**2)
    
        dev = sqrt(sum/self.sizePopulation)
    
        return dev

    def findMinAndMaxFit(self):
        min = ()
        max = -2
        
        for ind in self.population:
            if ind.fitness<min:
                min = ind.fitness
            if ind.fitness>max:
                max = ind.fitness
        
        return min,max

    #Sort the individual by the x coordinate
    
    def xCoordSelectionSortInd(self, individual):
        
        for x in range(2, (self.noPoints+2)*2,2):
            min = x
            for j in range(x + 2, (self.noPoints+2)*2,2):
                if individual.points[j] < individual.points[min]:
                    min = j
            
            individual.points[x], individual.points[min] = individual.points[min], individual.points[x] # swap
            individual.points[x+1], individual.points[min+1] = individual.points[min+1], individual.points[x+1] # swap

        # Now, we have to make sure that there are no two points with the same x value.
        previous = 0
        for x in range(2, (self.noPoints+2)*2,2):
            if (individual.points[x] == previous):
                individual.points[x] = individual.points[x] + EPSLON
            previous = individual.points[x]
        
        return individual

    """ Debugging method. """
    def printPopulation( self ):
        for i in xrange( self.sizePopulation ):
            print "%d: " % (i),
            self.printIndividual(self.population[i])
        
            
    def printIndividual( self , individual):
        for t in xrange(0, self.noPoints*2+4,2):
            print "(%.2lf, %.2lf) " % (individual.points[t], individual.points[t+1]),
        print "  Fitness: %lf" % (individual.fitness)
