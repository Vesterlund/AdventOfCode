import sys, getopt
import numpy as np
import math

def readFile(filepath:str):
    f = open(filepath)

    fileContent = f.read()
    f.close()

    return fileContent

def parseInput(filePath:str):

    # Pipe is = [A B] = [B A]
    # 1 north
    # 2 east
    # 3 south
    # 4 west
    
    fileContent = readFile(filePath).split("\n")

    stepMatrix = [[[-1,-1]]*(len(fileContent[0])+2)]
    startIndex = []

    
    for i,row in enumerate(fileContent):
        stepMatrix.append([[-1,-1]])
        j = 1
        for char in row:
            
            pipe = []
            
            match char:
                case "|":
                    pipe = [1,3]
                    
                case "-":
                    pipe = [2,4]
                    
                case "L":
                    pipe = [1,2]
                    
                case "J":
                    pipe = [1,4]
                    
                case "7":
                    pipe = [3,4]
                    
                case "F":
                    pipe = [2,3]
                    
                case "S":
                    pipe = [0,0] # Starting pipe of unknown shape
                    startIndex = [i+1,j]
                    
                case _:
                    pipe = [-1, -1]
                    
                    
            stepMatrix[i+1].append(pipe)
            j += 1
        stepMatrix[i+1].append([[-1,-1]])
            
    stepMatrix.append([[-1,-1]]*(len(fileContent[0])+2))
    
    return stepMatrix, startIndex, (len(fileContent),len(fileContent[0]))

def directionToCoords(direction):
    iNext = 0
    jNext = 0
    
    match direction:
        case 1:
            iNext = -1
        case 2:
            jNext = 1
        case 3:
            iNext = 1
        case 4:
            jNext = -1
            
    return [iNext, jNext]

def flipDir(direction):
    recDiv = 0
    
    match direction:
        
        case 1:
            recDiv = 3
        case 2: 
            recDiv = 4
        case 3:
            recDiv = 1
        case 4:
            recDiv = 2
    
    return recDiv

def canTakeStep(matrix, pos, direction): 
    dir = directionToCoords(direction)
    
    i = pos[0] + dir[0]
    j = pos[1] + dir[1]
    
    if(all(x==0 for x in matrix[i][j])):
        return True
    
    recDiv = flipDir(direction)
            
    
    return recDiv in matrix[i][j]

def searchForLoop(matrix,startIndex,direction):
    
    
    

    currentIndex = startIndex
    currentStep = 0
    
    loop = [(startIndex, 0)]
    
    while canTakeStep(matrix, currentIndex, direction):
        dir = directionToCoords(direction)
        currentIndex = [currentIndex[0] + dir[0], currentIndex[1] + dir[1]] 
        currentValues = matrix[currentIndex[0]][currentIndex[1]]
        
        if all(x==0 for x in currentValues):
            return loop
        
        currentStep += 1
       
        #print(currentValues,currentIndex, flipDir(direction))
        direction = currentValues[currentValues.index(flipDir(direction)) - 1]
        #print("dir: {}".format(direction))
        loop.append((currentIndex, currentStep))

            
        
         
    return -1

def part1(data):
    startingIndex = data[1]
    
    for i in range(1,5):
        loopSteps = searchForLoop(data[0], startingIndex, i)
        
        if loopSteps != -1:
            return len(loopSteps) // 2
    
    return -1

def part2(data):
    startingIndex = data[1]
    loopSteps = []
    for i in range(1,5):
        loopSteps = searchForLoop(data[0], startingIndex, i)
        
        if loopSteps != -1:
            break
    
    
    edges = np.zeros((data[2][0]+2, data[2][1]+2))
    
    for step in loopSteps:
        point = step[0]
        
        edges[point[0]][point[1]] = 1

    print(edges)
    

    return -1


def main(argv):
    noPartOne = False
    noPartTwo = False
    onlyExample = False
    debugMode = False

    opts, args = getopt.getopt(argv,"od",["no-part-1","no-part-2", "only-example"])
    for opt, arg in opts:
        if opt in ("-o", "--only-example"):
            onlyExample = True
        elif opt == "--no-part-1":
            noPartOne = True
        elif opt == "--no-part-2":
            noPartTwo = True
        elif opt == "-d":
            debugMode = True
    
    exampleFiles = ["example.txt", "example2.txt"]
    problemFiles = ["input.txt"]

    problemFiles = problemFiles + exampleFiles if not onlyExample else exampleFiles

    for file in problemFiles:
        data = parseInput(file)

        if not noPartOne:
            result = part1(data)
            print("{} - Part 1: Steps to farthest point {}".format(file, result))
        
        if not noPartTwo:
            result = part2(data)
            print("{} - Part 2: Inside area {}".format(file, result))






if __name__ == "__main__":
    main(sys.argv[1:])