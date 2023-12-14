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


    data = fileContent.replace(".","0").replace("#","1").replace("O","2").split("\n")
    data = [[int(c) for c in s] for s in data]
        
    return np.squeeze(np.array(data))

def rockNRoll(pattern):
    newPattern = np.copy(pattern)
    newPattern[newPattern == 2] = 0
    
    for i, row in enumerate(pattern):
        lastRock = 0
        roundCounter = 0
        
        for j, spot in enumerate(row):
            
            if spot == 1:
                lastRock = j+1
                roundCounter = 0
                
            
            if spot == 2:
                newPattern[i][lastRock+roundCounter] = 2
                roundCounter += 1
            
    return newPattern

def doRockNRollCycle(pattern):
    north = np.transpose(rockNRoll(np.transpose(pattern)))
    west = rockNRoll(north)
    south = np.flip(np.transpose(rockNRoll(np.transpose(np.flip(west, axis=0)))), axis=0)
    east = np.flip(rockNRoll(np.flip(south, axis=1)),axis=1)
    
    return east

def part1(data):
    
    totalLoad = 0
    numRows = len(data)
    
    for row in np.transpose(data):
        lastRock = 0
        roundCounter = 0
        rowLoad = 0
        
        for i, spot in enumerate(row):
            
            if spot == 1:
                lastRock = i+1
                roundCounter = 0
                
            if spot == 2:
                rowLoad += numRows - (lastRock + roundCounter)
                roundCounter += 1
            
        totalLoad += rowLoad
    return totalLoad

def part2(data : np.ndarray):
    bigNum = 1000000000
    pattern = data

    foundPatterns = set()
    foundPatterns.add(pattern.tobytes())
    
    firstLoopIndex = -1
    secondLoopIndex = -1
    for cycle in range(bigNum):
        pattern = doRockNRollCycle(pattern)
        
        if pattern.tobytes() in foundPatterns:
            if firstLoopIndex < 0:
                firstLoopIndex = cycle
                
                foundPatterns = set()
                foundPatterns.add(pattern.tobytes())
            else:
                secondLoopIndex = cycle
                break
        else:
            if(firstLoopIndex < 0):
                foundPatterns.add(pattern.tobytes())
        
    loopSize = secondLoopIndex - firstLoopIndex
    
    finalLoopIndex = firstLoopIndex - loopSize +  ((bigNum - firstLoopIndex -1) % loopSize)
    pattern = data
    for cycle in range(finalLoopIndex+1):
        pattern = doRockNRollCycle(pattern)
    
    mWeight = len(pattern)
    totalLoad = 0
    for i, row in enumerate(pattern):
        totalLoad += np.sum(row == 2) * (mWeight - i)
    
    return totalLoad
    


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
    
    exampleFiles = ["example.txt", "example2.txt"]
    problemFiles = ["input.txt"]

    problemFiles = exampleFiles + problemFiles if not onlyExample else exampleFiles

    if argFile:
        problemFiles = [argFile]

    for file in problemFiles:
        data = parseInput(file)

        if not noPartOne:
            result = part1(data)
            print("{} - Part 1: Total load {}".format(file, result))
        
        if not noPartTwo:
            result = part2(data)
            print("{} - Part 2: Total load {}".format(file, result))

if __name__ == "__main__":
    main(sys.argv[1:])