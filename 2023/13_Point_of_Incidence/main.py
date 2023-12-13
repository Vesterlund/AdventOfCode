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

    patterns = fileContent.split("\n\n")
    npPatterns = []
    
    for pattern in patterns:
        data = pattern.replace(".","0").replace("#","1").split("\n")
        data = [[int(c) for c in s] for s in data]
        
        npPatterns.append(np.squeeze(np.array(data)))
        

    return npPatterns

def hashRow(row):
    
    return sum([x*2**i for i,x in enumerate(row)])

def findMirror(row):
    rowLength = len(row)
    for mirrorPos in range(1, rowLength):
        mirroredElements = min(mirrorPos, rowLength - mirrorPos)
        
        frontElements = row[mirrorPos-mirroredElements:mirrorPos]
        backElements = row[mirrorPos:mirrorPos + mirroredElements]
        
        frontElements.reverse()
        
        if all(f == b for f,b in zip(frontElements, backElements)):
            return mirrorPos
    
    return -1

def findValidMirror(pattern):
    rowIndex = findMirror(cHashRow(pattern))
    colIndex = findMirror(cHashRow(np.transpose(pattern)))
    
    return rowIndex, colIndex

def cHashRow(pattern):
    return [hashRow(row) for row in pattern]

def fixSmudge(pattern, originalReflectation):
    # What smudges can be changed to produce a different reflection line?
    #print(pattern)
    
    validMirrors = []
    earliestMirrorIndex = np.Inf

    for i in range(0,len(pattern)):
        for j in range(0, len(pattern[0])):
            diff = np.copy(pattern)
            diff[i][j] = 1 - diff[i][j]
            
            vRow, vCol = findValidMirror(diff)
            
            if (vRow not in [-1, originalReflectation[0]]) or (vCol not in [-1, originalReflectation[1]]):
                return np.copy(diff)

# Find mirror
def part1(data):
    mirrorScore = 0
    
    for pattern in data:
       
        rowMirrorIndex, colMirrorIndex = findValidMirror(pattern)
    
        if rowMirrorIndex != -1:
            mirrorScore += 100*rowMirrorIndex
            
        if colMirrorIndex != -1:
            mirrorScore += colMirrorIndex
    
    return mirrorScore

def part2(data):
    mirrorScore = 0
    
    for i,pattern in enumerate(data):
        print(i,pattern)
        oRowIndex, oColIndex = findValidMirror(pattern)
        pattern = fixSmudge(pattern, (oRowIndex, oColIndex))
        
        nRowIndex, nColIndex = findValidMirror(pattern)
        
        if nRowIndex not in [-1, oRowIndex]:
            mirrorScore += 100*nRowIndex
            
        if nColIndex not in [-1, oColIndex]:
            mirrorScore += nColIndex
            
        
        
    return mirrorScore
    


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
            print("{} - Part 1: Mirror score {}".format(file, result))
        
        if not noPartTwo:
            result = part2(data)
            print("{} - Part 2: Mirror score {}".format(file, result))

if __name__ == "__main__":
    main(sys.argv[1:])