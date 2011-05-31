'''
Created on 16 de Mai de 2011

@author: Barbosa
'''
from Tkinter import *

class BrackGui(Tk):

    def __init__(self,curveFinder,parent=None):
        Tk.__init__(self, parent)   
         
        self.parent = parent
        self.curveFinder = curveFinder

        self.initUI()


    def initUI(self):
      
        yInc=25
                
        ''' buttons '''
        self.quitButton = Button(self, text="Quit", command=self.quit)
        self.quitButton.place(x=500, y=500)
        
        self.quitButton = Button(self, text="Start", command = self.runCurve) #TODO start function
        self.quitButton.place(x=450, y=500)

        ''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ first Row ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
        self.firstLabel = Label(self, text="Parameters", font=('Arial', 10, 'bold'))
        self.firstLabel.place(x=15,y=8)
        
        ''' Spinners '''
        self.startHeightLabel = Label(self, text="Start (0, y) ")
        self.startHeightLabel.place(x=3,y=yInc+10)
        self.setHS = Spinbox(self, from_=0, to=100, width=4)
        self.setHS.place(x=70,y=yInc+10)
        for _ in xrange(3):
            self.setHS.invoke("buttonup")
        
        self.endHeightLabel = Label(self, text="End (x, y) ")
        self.endHeightLabel.place(x=3,y=yInc+40)
        self.setHEy = Spinbox(self, from_=0, to=100000,width=4)
        self.setHEy.place(x=113,y=yInc+40)
        self.setHEy.invoke("buttonup")
        self.setHEx = Spinbox(self, from_=0, to=100000,width=4)
        self.setHEx.place(x=70,y=yInc+40)
        self.setHEx.invoke("buttonup")     
        
        self.noPointsLabel = Label(self, text="No. of Points:")
        self.noPointsLabel.place(x=240,y=yInc+10)
        self.noPointsSpin = Spinbox(self, from_=0, to=100000,width=4)
        self.noPointsSpin.place(x=330,y=yInc+10)
        for _ in xrange(10):
            self.noPointsSpin.invoke("buttonup")
        
        self.printGensLabel = Label(self, text="Show Each gen:")
        self.printGensLabel.place(x=240,y=yInc+40)
        self.printGensSpin = Spinbox(self, from_=0, to=100000,width=4)
        self.printGensSpin.place(x=330,y=yInc+40)
        for _ in xrange(10):
            self.printGensSpin.invoke("buttonup")
        
        ''' radio buttons '''
        self.xyVar = IntVar()
        self.xyVar.set(0)
        self.fixedX = Radiobutton(self, text="Fixed X", variable=self.xyVar, value=0, command = self.setOnlyX)
        self.fixedX.place(x=155, y=yInc+10)
        self.fixedX.select()
        self.xAndY = Radiobutton(self, text="X & Y", variable=self.xyVar, value=1, command = self.setXandY)
        self.xAndY.place(x=155, y=yInc+40)
        
        self.selTorn = IntVar()
        self.selTorn.set(1)
        self.tournSel = Radiobutton(self, text="Tournament Selection", variable=self.selTorn, value=1, indicatoron=0, command = self.enableTournamentSize)
        self.tournSel.place(x=400, y=yInc+10)
        self.tournSel.select()
        self.RouletteSel = Radiobutton(self, width="16", text="Roulette Selection", variable=self.selTorn, value=2, indicatoron=0, command = self.disableTournamentSize)
        self.RouletteSel.place(x=400, y=yInc+40)

        ''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Second Row ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
        self.secondLabel = Label(self, text="Sizes", font=('Arial', 10, 'bold'))
        self.secondLabel.place(x=15,y=100)
        
        ''' Spinners '''
        self.popSizeLabel = Label(self, text="Population Size ")
        self.popSizeLabel.place(x=3,y=yInc+100)
        self.popSizeSpin = Spinbox(self, from_=0, to=100000, width=4)
        self.popSizeSpin.place(x=95,y=yInc+100)
        for _ in xrange(200):
            self.popSizeSpin.invoke("buttonup")
        
        self.popNoGenLabel = Label(self, text="No of generations")
        self.popNoGenLabel.place(x=180,y=yInc+100)
        self.popNoGenSpin = Spinbox(self, from_=0, to=100000, width=4)
        self.popNoGenSpin.place(x=290,y=yInc+100)
        for _ in xrange(500):
            self.popNoGenSpin.invoke("buttonup")
        
        self.popTornSizeLabel = Label(self, text="Tournament Size ")
        self.popTornSizeLabel.place(x=375,y=yInc+100)
        self.popTornSizeSpin = Spinbox(self, from_=0, to=100000, width=4)
        self.popTornSizeSpin.place(x=480,y=yInc+100)
        for _ in xrange(5):
            self.popTornSizeSpin.invoke("buttonup")
        
        
        ''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Third Row ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
        self.thirdLabel = Label(self, text="Probabilities", font=('Arial', 10, 'bold'))
        self.thirdLabel.place(x=15,y=yInc+140)
        
        ''' Scales '''
        self.mutProbLabel = Label(self, text="Mutation")
        self.mutProbLabel.place(x=3, y=yInc+175)
        self.mutProbScale = Scale(self,orient=HORIZONTAL, from_=0, to=100, length=430)
        self.mutProbScale.place(x=90, y=yInc+160)
        self.mutProbScale.set(10)
        
        self.CrosOverProbLabel = Label(self, text="CrossOver")
        self.CrosOverProbLabel.place(x=3, y=yInc+225)
        self.CrosOverProbScale = Scale(self,orient=HORIZONTAL, from_=0, to=100, length=430)
        self.CrosOverProbScale.place(x=90, y=yInc+210)
        self.CrosOverProbScale.set(50)
        
        ''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Fourth Row ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
        self.fourthLabel = Label(self, text="Percentages", font=('Arial', 10, 'bold'))
        self.fourthLabel.place(x=15,y=yInc+265)
        
        ''' Scales '''
        self.crossOverSizeLabel = Label(self, text="Size CrossOver")
        self.crossOverSizeLabel.place(x=3, y=yInc+300)
        self.crossOverSizeScale = Scale(self,orient=HORIZONTAL, from_=0, to=100, length=415)
        self.crossOverSizeScale.place(x=105, y=yInc+285)
        self.crossOverSizeScale.set(50)
        
        self.elitismLabel = Label(self, text="Elitism Parents")
        self.elitismLabel.place(x=3, y=yInc+350)
        self.elitismScale = Scale(self,orient=HORIZONTAL, from_=0, to=100, length=415)
        self.elitismScale.place(x=105, y=yInc+335)
        self.elitismScale.set(5)
        
        self.selEli = IntVar()
        self.selEli.set(1)
        self.elitismPerSel = Radiobutton(self, text="Elitism", variable=self.selEli, value=1, indicatoron=0, command = self.enablePercElitism)
        self.elitismPerSel.place(x=150, y=yInc+380)
        self.elitismPerSel.select()
        self.elitismHalfSel = Radiobutton(self, width="16", text="Half", variable=self.selEli, value=2, indicatoron=0, command = self.enableHalf)
        self.elitismHalfSel.place(x=250, y=yInc+380)
        self.elitismOffSel = Radiobutton(self, width="16", text="Only Offsprings", variable=self.selEli, value=3, indicatoron=0, command = self.enableOffspring)
        self.elitismOffSel.place(x=400, y=yInc+380)
    

    def enableHalf(self):
        self.selEli.set(2)
        self.elitismScale.configure(state=DISABLED)
        self.elitismLabel.configure(state=DISABLED)
        
    def enablePercElitism(self):
        self.selEli.set(1)
        self.elitismScale.configure(state=NORMAL)
        self.elitismLabel.configure(state=NORMAL)
    
    def enableOffspring(self):
        self.selEli.set(3)
        
    def enableTournamentSize(self):
        self.selTorn.set(1)
        self.popTornSizeSpin.configure(state=NORMAL)
        self.popTornSizeLabel.configure(state=NORMAL)
        
    def disableTournamentSize(self):
        self.selTorn.set(2)
        self.popTornSizeSpin.configure(state=DISABLED)
        self.popTornSizeLabel.configure(state=DISABLED)
    
    def setOnlyX(self):
        self.xyVar.set(0)
        
    def setXandY(self):
        self.xyVar.set(1)
    
    def runCurve(self):
        
        ''' start and end point '''
        self.curveFinder.setStartPoint([0, int(self.setHS.get())])
        self.curveFinder.setEndPoint([int(self.setHEx.get()), int(self.setHEy.get())])
        
        ''' radio buttons '''
        self.curveFinder.useXandY = self.xyVar.get()
        self.curveFinder.eliType = self.selEli.get()
        self.curveFinder.useSelectionParents = self.selTorn.get()

        '''spins'''
        self.curveFinder.noPoints = int(self.noPointsSpin.get())
        self.curveFinder.plotOn = int(self.printGensSpin.get())
        self.curveFinder.setNumberGenerations(int(self.popNoGenSpin.get()))
        self.curveFinder.setSizePopulation(int(self.popSizeSpin.get()))
        self.curveFinder.setSizeTournament(int(self.popTornSizeSpin.get()))
        
        ''' scales '''
        self.curveFinder.setMutationProb(int(self.mutProbScale.get()))
        self.curveFinder.setCrossOverProb(int(self.CrosOverProbScale.get()))
        
        self.curveFinder.setCrossOverSizePerc(int(self.crossOverSizeScale.get()))
        self.curveFinder.setParentsElitismPerc(int(self.elitismScale.get()))
        
        ''' call curve '''
        self.curveFinder.bestCurve()

    def avg(self):
        self.avgInd 
        for i in self.population:
            sum += i.fitness
                    
        return sum/self.sizePopulation
    
