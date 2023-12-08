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

    directions = fileContent[0]
    nodes = []
    leftNodes = []
    rightNodes = []

    for row in fileContent[2:]:
        rootNode = row[0:3]
        leftNode = row[7:10]
        rightNode = row[12:15]
        
        nodes.append(rootNode)
        leftNodes.append(leftNode)
        rightNodes.append(rightNode)

    return (directions, nodes, leftNodes, rightNodes)

def createStepMatrix(data):
    directions = data[0]
    nodes : list = data[1]
    leftNodes : list = data[2]
    rightNodes : list = data[3]


    leftMatrix = np.zeros((len(nodes), len(nodes)))
    rightMatrix = np.zeros_like(leftMatrix)

    for i in range(len(nodes)):
        l = nodes.index(leftNodes[i])
        r = nodes.index(rightNodes[i])

        leftMatrix[i][l] = 1
        rightMatrix[i][r] = 1

    stepMatrix = np.zeros_like(leftMatrix)

    stepMatrix = leftMatrix if directions[0]=="L" else rightMatrix

    for direction in directions[1:]:
        stepMatrix = np.matmul(stepMatrix, leftMatrix) if direction=="L" else np.matmul(stepMatrix, rightMatrix)


    return stepMatrix

def findStartEnd(data):
    nodes = data[1]

    start = -1
    end = -1

    for i in range(len(nodes)):
        
        node = nodes[i]

        if node == "AAA":
            start = i
        
        if node == "ZZZ":
            end = i

        if end > -1 and start > -1:
            break

    
    return start, end

def part1(data):
    directions = data[0]

    stepMatrix = createStepMatrix(data)
    start, end =  findStartEnd(data)
    print("Searcing {} -> {}".format(start, end))

    currentNode = start
    currentSteps = 0
    stepSize = len(directions)

    while currentNode != end:
        nextNode = np.where(stepMatrix[currentNode] == 1)[0][0]

        currentNode = nextNode
        currentSteps += stepSize
    

    return currentSteps

def findAllStartEnd(data):
    starts = []
    ends = []

    for i, node in enumerate(data[1]):
        if node[-1] == "A":
            starts.append(i)
        elif node[-1] == "Z":
            ends.append(i)


    return starts, ends

def part2(data):
    directions = data[0]

    stepMatrix = createStepMatrix(data)
    starts, ends = findAllStartEnd(data)
    currentNodes = starts

    stepSize = len(directions)


    nodeCycles = []
    foundNodes = []
    for node in starts:
        foundNodes.append([node])

    # Find all the repeating cycles
    while True:
        nextNodes = []

        for i in range(len(currentNodes)):
            currentNode = currentNodes[i]

            if (currentNode < 0):
                nextNodes.append(-1)
                continue

            nextNode = np.where(stepMatrix[currentNode] == 1)[0][0]

            if nextNode in foundNodes[i]:
                cycleStart = foundNodes[i].index(nextNode)
                nodeCycles.append(foundNodes[i][cycleStart:])
                nextNodes.append(-1)
            else:
                nextNodes.append(nextNode)
                foundNodes[i].append(nextNode)
        
        currentNodes = nextNodes

        if sum(currentNodes) == -1*len(currentNodes):
            break


    cycleLengths = [len(x) for x in nodeCycles]

    return math.lcm(*cycleLengths)*stepSize


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
    
    exampleFiles = []
    problemFiles = ["input.txt"]

    problemFiles = problemFiles + exampleFiles if not onlyExample else exampleFiles

    for file in problemFiles:
        data = parseInput(file)

        if not noPartOne:
            result = part1(data)
            print("{} - Part 1: Number of steps {}".format(file, result))
        
        if not noPartTwo:
            result = part2(data)
            print("{} - Part 2: Number of steps {}".format(file, result))






if __name__ == "__main__":
    main(sys.argv[1:])