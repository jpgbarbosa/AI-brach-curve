'''
Created on 17 de Mai de 2011

@author: Barbosa
'''

from curva import BrachistochroneCurve
from Gui import *

if __name__ == '__main__':
    
    curveFinder = BrachistochroneCurve([0,3], [1,2])
    curveFinder.setNoPoints(10)
    curveFinder.setSizePopulation(200)
    curveFinder.setSizeTournament(5)
    curveFinder.setNumberGenerations(500)
    
    curveFinder.setMutationProb(10)
    curveFinder.setCrossOverProb(50)

    curveFinder.setCrossOverSizePerc(50)
    curveFinder.setParentsElitismPerc(5)
    
    curveFinder.useCrossover = True
    curveFinder.useCrossOverPercentage = True
    curveFinder.useMutation = True
    curveFinder.useSelectionParents = 1 #0- n usar 1- tournament 2- roulette
    curveFinder.useElitism = True
    curveFinder.printPopulation = True

      
    app = BrackGui(curveFinder)
    app.resizable(0,0)
    app.geometry("550x550+100+100")
    app.mainloop()
