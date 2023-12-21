import sys, getopt
import numpy as np
import math
import re
from enum import Enum
import copy
np.set_printoptions(threshold=sys.maxsize, linewidth=sys.maxsize)

def readFile(filepath:str):
    f = open(filepath)

    fileContent = f.read()
    f.close()

    return fileContent

def parseInput(filePath:str):
    fileContent = readFile(filePath)


    data = fileContent.split("\n")
    
    numberOfPlots= len(data) * len(data[0])

    paddedGrid = np.zeros((len(data)+2, len(data[0])+2))
    connectivityMatrix = np.zeros((numberOfPlots,numberOfPlots))
    
    paddedGrid[0,:] = -1
    paddedGrid[-1,:] = -1
    paddedGrid[:,0] = -1
    paddedGrid[:,-1] = -1

    startPoint = (0,0)

    for iRow, row in enumerate(data):
        for jCol, el in enumerate(row):
            if el == "S":
                startPoint = (iRow, jCol)
                paddedGrid[iRow+1, jCol+1] = 1
            elif el == "#":
                paddedGrid[iRow+1, jCol+1] = -1
            else:
                paddedGrid[iRow+1, jCol+1] = 0

    height = len(data)
    width = len(data[0])

    for iRow in range(0, height):
        for iCol in range(0, width):
            currentNodeNumber = iRow*width + iCol

            paddedIndex = (iRow +1, iCol + 1)
            if paddedGrid[paddedIndex] == -1:
                continue

            adjacentNodes = [(iRow, iCol+1), (iRow + 2, iCol + 1), (iRow+1, iCol), (iRow+1,iCol+2)]

            for nodeIndex in adjacentNodes:
                if paddedGrid[nodeIndex] != -1:
                    #print(currentNodeNumber,(nodeIndex[0]-1)*width + nodeIndex[1]-1)
                    connectivityMatrix[currentNodeNumber, ((nodeIndex[0]-1)*width + nodeIndex[1]-1)] = 1

    return  connectivityMatrix, startPoint[0]*width + startPoint[1]

from queue import Queue

def part1(data):
    connectivityMatrix, startPlot = data

    visitedSet = set()
    stepsToFirstReach = {}

    nodeQ = Queue()

    adjacentPlots = np.nonzero(connectivityMatrix[startPlot,:])[0]

    for plot in adjacentPlots:
        stepsToFirstReach[plot] = 1
        nodeQ.put(plot)

    while not nodeQ.empty():
        currPlot = nodeQ.get()

        if currPlot not in visitedSet:
            
            visitedSet.add(currPlot)
            
            adjacentPlots = np.nonzero(connectivityMatrix[currPlot,:])[0]

            for plot in adjacentPlots:
                if plot not in visitedSet:
                    stepsToFirstReach[plot] = stepsToFirstReach[currPlot] + 1
                    nodeQ.put(plot)

    
    exactSteps = 64

    plotCount = 0

    for k in stepsToFirstReach:
        steps = stepsToFirstReach[k]

        if steps <= exactSteps and (exactSteps - steps) % 2 == 0:
            plotCount += 1


    return plotCount

def part2(data):
   return

def main(argv):
    noPartOne = False
    noPartTwo = False
    onlyExample = False
    argFile = ""

    opts, args = getopt.getopt(argv,"odf:",["no-part-1","no-part-2", "only-example"])
    for opt, arg in opts:
        if opt in ("-o", "--only-example"):
            onlyExample = True
        elif opt == "--no-part-1":
            noPartOne = True
        elif opt == "--no-part-2":
            noPartTwo = True
        elif opt in ['-f']:
            argFile = arg
    
    exampleFiles = ["example.txt"]
    problemFiles = ["input.txt"]

    problemFiles = exampleFiles + problemFiles if not onlyExample else exampleFiles

    if argFile:
        problemFiles = [argFile]

    for file in problemFiles:
        data = parseInput(file)

        if not noPartOne:
            result = part1(copy.deepcopy(data))
            print("{} - Part 1: {} Plots can be reached".format(file, result))
        
        if not noPartTwo:
            result = part2(copy.deepcopy(data))
            print("{} - Part 2: {} Button presses ".format(file, result))

if __name__ == "__main__":
    main(sys.argv[1:])