import sys, getopt
import numpy as np
import math

def readFile(filepath:str):
    f = open(filepath)

    fileContent = f.read()
    f.close()

    return fileContent

def parseInput(filePath:str):
    fileContent = readFile(filePath)


    data = fileContent.split("\n")
    
    xBound = 0
    yBound = 0
    
    instructions = []
    
    for instruction in data:
        direction, nSteps, col = instruction.split(" ")
        
        nSteps = int(nSteps)
        
        match direction:
            case "R":
                yBound += nSteps
            case "D":
                xBound += nSteps
        
        instructions.append((direction, nSteps, col))
        
    return instructions, xBound, yBound

from operator import add

def diffCoordCalc(dir, step):
    
    c = [0,0]
    
    match dir:
        case "R":
            c[1] = step
        case "L":
            c[1] = -step
        case "U":
            c[0] = -step
        case "D":
            c[0] = step
    
    
    return c

def cornerType(pDir, dir):
    match pDir:
        case "R":
            return -1 if dir == "D" else -2
        case "D":
            return -2 if dir == "L" else -4
        case "L":
            return -3 if dir == "D" else -4
        case "U":
            return -1 if dir == "L" else -3

import sys

def constructGrid(instructions, xBound, yBound):
    grid = np.zeros((xBound*2+1, yBound*2+1))
    
    startPoint = (xBound, yBound)

    grid[startPoint] = 1
    
    currPoint = list(startPoint)
    
    prevDir = None
    
    minX, maxX = startPoint[0],startPoint[0]
    minY, maxY = startPoint[1],startPoint[1]
    
    for ins in instructions:
        dir, step, col = ins
        nextPoint = tuple(map(add, currPoint, diffCoordCalc(dir, step)))
        
        xC = [currPoint[0], nextPoint[0]]
        xC.sort()
        yC = [currPoint[1], nextPoint[1]]
        yC.sort()
        
        grid[xC[0]:xC[1]+1, yC[0]:yC[1]+1] = 1
        
        if prevDir:
            a = xC[1] if dir == "U" else xC[0]
            b = yC[1] if dir == "L" else yC[0]
            grid[a,b] = cornerType(prevDir, dir)
        
        currPoint = list(nextPoint)
        prevDir = dir
        minX = min(minX, currPoint[0])
        minY = min(minY, currPoint[1])
        maxX = max(maxX, currPoint[0])
        maxY = max(maxY, currPoint[1])
    
    grid[startPoint] = cornerType(prevDir, instructions[0][0])
    
    grid = grid[minX:maxX+1, minY:maxY+1]
    
    return grid


def fillGrid(grid):
    
    filledGrid = np.copy(grid)
    
    for i,row in enumerate(grid):
        isInside  = False
        isInWall = False
        lastCorner = 0
        
        for j,element in enumerate(row):
            
            if element < 0:
                isInWall = not isInWall
                
                if lastCorner == 0:
                    lastCorner = element
                else:
                    if lastCorner == -3:
                        isInside = not isInside if element == -2 else isInside
                    elif lastCorner == -4:
                        isInside = not isInside if element == -1 else isInside
                    lastCorner = 0
                    isInWall = False
                    continue
            
            if element == 1 and not isInWall:
                isInside = not isInside
            
            
            if isInside:
                filledGrid[i,j] = 1
        
    
    return filledGrid

def intToDir(x):
    match x:
        case 0: return "R"
        case 1: return "D"
        case 2: return "L"
        case 3: return "U"

def part1(data):
    
    grid = constructGrid(*data)
    filledGrid = fillGrid(grid)

    return np.count_nonzero(filledGrid)

def part2(data):
    
    # Need to be clever, cannot allocate 69.6 TiB
    
    ins,_,_ = data
    print(ins)
    xBound = 0
    yBound = 0
    instructions = []
    for i in ins:
        _, _, c = i
        
        direction = intToDir(int(c[-2]))
        nSteps = int(c[2:-2],16)
        instructions.append((direction, nSteps))
        
        match direction:
            case "R":
                yBound += nSteps
            case "D":
                xBound += nSteps

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
            result = part1(data)
            print("{} - Part 1: {} cubic meters".format(file, result))
        
        if not noPartTwo:
            result = part2(data)
            print("{} - Part 2: Maximum energized tiles {}".format(file, result))

if __name__ == "__main__":
    main(sys.argv[1:])