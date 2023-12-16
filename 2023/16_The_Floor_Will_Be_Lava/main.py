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
    

    mirrorMatrix = np.zeros((len(data)+2, len(data[0])+2))

    mirrorMatrix[:,0] = -1
    mirrorMatrix[0] = -1
    mirrorMatrix[-1] = -1
    mirrorMatrix[:,-1] = -1

    for i, row in enumerate(data):
        for j, char in enumerate(row):

            val = 0

            match char:
                case "|":
                    val = 1
                case "-":
                    val = 2
                case "\\":
                    val = 3
                case "/":
                    val = 4

            mirrorMatrix[i+1,j+1] = val

    return mirrorMatrix

class Beam:
    cPos = 0+1j
    direction = 1+0j

    def __init__(self, cPos = 0+1j, direction = 1+0j) -> None:
        self.cPos = cPos
        self.direction = direction

    def mirror(self, mType):

        if mType == 1: # /
            self.direction = -(self.direction.imag) - 1j*(self.direction.real)
        else: # \
            self.direction = (self.direction.imag) + 1j*(self.direction.real)

    def split(self):
        self.mirror(1)
        return Beam(cPos=self.cPos, direction=self.direction*-1)

    def nextPos(self):
        return self.cPos + self.direction

    def step(self):
        self.cPos = self.cPos + self.direction

    def id(self):
        return (self.cPos, self.direction)

    def __str__(self) -> str:
        return "{},{}".format(self.cPos, self.direction)

def printSpace(matrix, traversalSet):
    def instToChar(inst):
        match inst:
            case -1:
                return "@"
            case 0: return "."
            case 1: return "|"
            case 2: return "-"
            case 3: return "\\"
            case 4: return "/"

    pointSet = set()
    print("====")
    for point, dir in traversalSet:
        pointSet.add(point)

    for iRow, row in enumerate(matrix):
        pString = ""
        mstring = ""
        for iCol, col in enumerate(row):
            p = iCol + 1j*iRow
            pString += "." if p not in pointSet else "#"
            mstring += instToChar(int(col))

        print(pString, mstring)

def energizeMatrix(mirrorMatrix, startBeam):
    b = startBeam
    activeBeams = []
    traversalSet = set()

    activeBeams.append(b)
    while activeBeams:
        tempBeams = activeBeams.copy()

        for b in tempBeams:
            nPos = b.nextPos()
            instruction = mirrorMatrix[int(nPos.imag),int(nPos.real)]

            if instruction == -1 or (nPos, b.direction) in traversalSet:
                activeBeams.pop(activeBeams.index(b))
                continue
            
            b.step()
            traversalSet.add(b.id())
            
            match instruction:
                case 1:
                    d = b.direction.real
                    if d:
                        activeBeams.append(b.split())
                case 2:
                    d = b.direction.imag
                    if d:
                        activeBeams.append(b.split())
                case 3:
                    b.mirror(-1)
                case 4:
                    b.mirror(1)
        #printSpace(mirrorMatrix, traversalSet)

    pointSet = set()

    for point, dir in traversalSet:
        pointSet.add(point)

    return len(pointSet)

def part1(data):

    mirrorMatrix = data

    return energizeMatrix(mirrorMatrix, Beam())

def part2(data):

    mirrorMatrix = data
    maxEnergy = 0

    height = len(mirrorMatrix)
    width = len(mirrorMatrix[0])

    for iRow in range(1,len(mirrorMatrix)):
        maxEnergy = max(maxEnergy, energizeMatrix(mirrorMatrix, Beam(0 + iRow*1j)))
        maxEnergy = max(maxEnergy, energizeMatrix(mirrorMatrix, Beam(width-1 + iRow*1j, -1 + 0j)))
    
    for iCol in range(1,len(mirrorMatrix[0])):
        maxEnergy = max(maxEnergy, energizeMatrix(mirrorMatrix, Beam(iCol + 0j, 0 + 1j)))
        maxEnergy = max(maxEnergy, energizeMatrix(mirrorMatrix, Beam(iCol + 1j*(height-1), 0 - 1j)))

    return maxEnergy
    


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
            print("{} - Part 1: Energized tiles {}".format(file, result))
        
        if not noPartTwo:
            result = part2(data)
            print("{} - Part 2: Maximum energized tiles {}".format(file, result))

if __name__ == "__main__":
    main(sys.argv[1:])