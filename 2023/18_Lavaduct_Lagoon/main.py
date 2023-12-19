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


def intToDir(x):
    match x:
        case 0: return "R"
        case 1: return "D"
        case 2: return "L"
        case 3: return "U"

def calcEndPoint(curr : list, dir, steps):
    ep = curr.copy()
    match dir:
        case "U": ep[1] -= steps
        case "R": ep[0] += steps
        case "D": ep[1] += steps
        case "L": ep[0] -= steps

    return ep

def constructCornerGraph(instructions):
    startPoint = [0,0]
    pCurr = startPoint
    pointList = []
    pointList.append(startPoint)

    for ins in instructions:
        dir, steps,_ = ins

        pEnd = calcEndPoint(pCurr, dir, steps)
        pointList.append(pEnd)

        pCurr = pEnd

    return pointList

def perimiterLength(instructions):
    length = 0

    for ins in instructions:
        _, steps, _ = ins
        length += steps

    return length

def shoelace(x_y):
    x_y = np.array(x_y, dtype=np.int64)
    x_y = x_y.reshape(-1,2)

    x = x_y[:,0]
    y = x_y[:,1]

    S1 = np.sum(x*np.roll(y,-1))
    S2 = np.sum(y*np.roll(x,-1))

    area = .5*np.absolute(S1 - S2)

    return area

def solve(ins):
    cornerGraph = constructCornerGraph(ins)
    cornerGraph.reverse()
    # Compensate for shoelace algorithm working with "center" of our squares
    return int(shoelace(cornerGraph) + perimiterLength(ins) / 2 + 1)

def part1(data):
    ins,_,_ = data

    
    return solve(ins)

def part2(data):
    ins,_,_ = data
    instructions = []
    for i in ins:
        _, _, c = i
        
        direction = intToDir(int(c[-2]))
        nSteps = int(c[2:-2],16)
        instructions.append((direction, nSteps, ""))

    return solve(instructions)
    

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
            print("{} - Part 2: {} cubic meters".format(file, result))

if __name__ == "__main__":
    main(sys.argv[1:])