import sys, getopt
import numpy as np
import math

def readFile(filepath:str):
    f = open(filepath)

    fileContent = f.read()
    f.close()

    return fileContent

def parseInput(filePath:str):
    fileContent = readFile(filePath).split("\n")

    spaceMatrix = np.zeros((len(fileContent), len(fileContent[0])))
    pointList = []

    for i,row in enumerate(fileContent):
        for j, el in enumerate(row):
            if el == "#":
                spaceMatrix[i][j] = 1 
                pointList.append((i,j))

    return spaceMatrix, pointList

def getExpandingParts(spaceMatrix):
    cols = []
    rows = []

    for i, row in enumerate(spaceMatrix):
        if np.count_nonzero(row) == 0:
            rows.append(i)
    
    for i, col in enumerate(np.transpose(spaceMatrix)):
        if np.count_nonzero(col) == 0:
            cols.append(i)

    return rows, cols

def countDistance(p1, p2, expandingSpace, expandBy):


    xDist = abs(p1[0] - p2[0])
    yDist = abs(p1[1] - p2[1])

    xRange = range(min(p1[0],p2[0]), max(p1[0],p2[0]))
    yRange = range(min(p1[1],p2[1]), max(p1[1],p2[1]))

    xSpace = 0
    ySpace = 0

    for row in expandingSpace[0]:
        if row in xRange:
            xSpace += expandBy
    
    for col in expandingSpace[1]:
        if col in yRange:
            ySpace += expandBy

    dist = xDist + xSpace + yDist + ySpace

    return dist

def part1(data):

    totalDist = 0
    size = len(data[1])
    expandingSpace = getExpandingParts(data[0])

    for i in range(size):
        for j in range(i, size):
            p1 = data[1][i]
            p2 = data[1][j]
            totalDist += countDistance(p1,p2,expandingSpace, 1)


    return totalDist

def part2(data):
    
    totalDist = 0
    size = len(data[1])
    expandingSpace = getExpandingParts(data[0])

    for i in range(size):
        for j in range(i, size):
            p1 = data[1][i]
            p2 = data[1][j]
            totalDist += countDistance(p1,p2,expandingSpace, 1000000-1)


    return totalDist


def main(argv):
    noPartOne = False
    noPartTwo = False
    onlyExample = False

    opts, args = getopt.getopt(argv,"od",["no-part-1","no-part-2", "only-example"])
    for opt, arg in opts:
        if opt in ("-o", "--only-example"):
            onlyExample = True
        elif opt == "--no-part-1":
            noPartOne = True
        elif opt == "--no-part-2":
            noPartTwo = True
    
    exampleFiles = ["example.txt"]
    problemFiles = ["input.txt"]

    problemFiles = exampleFiles + problemFiles if not onlyExample else exampleFiles

    for file in problemFiles:
        data = parseInput(file)

        if not noPartOne:
            result = part1(data)
            print("{} - Part 1: Sum of shortest distances {}".format(file, result))
        
        if not noPartTwo:
            result = part2(data)
            print("{} - Part 2: Sum of shortest distances {}".format(file, result))

if __name__ == "__main__":
    main(sys.argv[1:])