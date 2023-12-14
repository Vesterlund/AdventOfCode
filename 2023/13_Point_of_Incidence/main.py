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
    mirrorIndex = []
    for mirrorPos in range(1, rowLength):
        mirroredElements = min(mirrorPos, rowLength - mirrorPos)
        
        frontElements = row[mirrorPos-mirroredElements:mirrorPos]
        backElements = row[mirrorPos:mirrorPos + mirroredElements]
        
        frontElements.reverse()
        
        if all(f == b for f,b in zip(frontElements, backElements)):
            mirrorIndex.append(mirrorPos)
    
    if not mirrorIndex:
        return [-1]
    
    return mirrorIndex

def findValidMirror(pattern):
    rowIndex = findMirror(cHashRow(pattern))
    colIndex = findMirror(cHashRow(np.transpose(pattern)))
    
    return rowIndex, colIndex

def cHashRow(pattern):
    return [hashRow(row) for row in pattern]

def fixSmudge(pattern, originalReflectation):
    
    for i in range(0,len(pattern)):
        for j in range(0, len(pattern[0])):
            diff = np.copy(pattern)
            diff[i][j] = 1 - diff[i][j]
                        
            vRow, vCol = findValidMirror(diff)

            for row in vRow:
                if (row not in [-1, originalReflectation[0]]):
                    return np.copy(diff), True
            
            for col in vCol:
                if col not in [-1, originalReflectation[1]]:
                    return np.copy(diff), True
    
    return pattern, False
    
# Find mirror
def part1(data):
    mirrorScore = 0
    
    for pattern in data:
       
        rowMirrorIndex, colMirrorIndex = findValidMirror(pattern)

        if -1 not in rowMirrorIndex:
            mirrorScore += 100*rowMirrorIndex[0]
            
        if -1 not in colMirrorIndex:
            mirrorScore += colMirrorIndex[0]
    
    return mirrorScore

def part2(data):
    mirrorScore = 0
    
    for pattern in data:
        oRowIndex, oColIndex = findValidMirror(pattern)
        oRowIndex, oColIndex = oRowIndex[0],oColIndex[0]
        
        pattern, hasReflection = fixSmudge(pattern, (oRowIndex, oColIndex))
        
        if not hasReflection:
            continue
        
        nRowIndex, nColIndex = findValidMirror(pattern)
        
        for ri in nRowIndex:
            if ri not in [-1, oRowIndex]:
                mirrorScore += 100*ri
            
        for ci in nColIndex:
            if ci not in [-1, oColIndex]:
                mirrorScore += ci
        
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