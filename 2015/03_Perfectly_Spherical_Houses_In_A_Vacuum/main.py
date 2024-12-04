import sys, getopt
import numpy as np
import math
import re
from enum import Enum
import copy
import queue
np.set_printoptions(threshold=sys.maxsize, linewidth=sys.maxsize)

def readFile(filepath:str):
    f = open(filepath)

    fileContent = f.read()
    f.close()

    return fileContent

def parseInput(filePath:str):
    fileContent = readFile(filePath)
    
    return fileContent

def charToComp(c):
    match c:
        case "^": return -1+0j
        case "v": return  1+0j
        case ">": return  0+1j
        case "<": return  0-1j
    
def part1(data):
    
    visitedHouses = set()
    start = 0+0j
    
    visitedHouses.add(start)
    
    for c in data:
        start += charToComp(c)
        visitedHouses.add(start)
    
    return len(visitedHouses)


def part2(data):
    
    visitedHouses = set()
    start = 0+0j
    
    visitedHouses.add(start)
    
    roboPos = start
    santaPos = start
    
    for i, c in enumerate(data):
        if i % 2 == 0:
            santaPos += charToComp(c)
            visitedHouses.add(santaPos)
        else:
            roboPos += charToComp(c)
            visitedHouses.add(roboPos)
        
        
    return len(visitedHouses)
    

    

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
            print("{} - Part 1: {} Houses gets presents!".format(file, result))
        
        if not noPartTwo:
            result = part2(copy.deepcopy(data))
            print("{} - Part 2: {} Houses gets presents!".format(file, result))

if __name__ == "__main__":
    main(sys.argv[1:])