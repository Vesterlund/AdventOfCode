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
    data = fileContent.split("\n")
    
    sizes = []
    
    for d in data:
        sizes.append(list(map(int, re.findall(r"\d+", d))))
    
    return sizes


    
def part1(data):
    
    totalWrapping = 0
    
    for s in data:
        l,w,h = s
        totalWrapping += 2*(l*w + w*h + h*l) + min(l*w,w*h,h*l)
    
    return totalWrapping


def part2(data):
    totalRibbon = 0
    
    for s in data:
        s.sort()
        a,b,c = s
        totalRibbon += 2*(a+b) + a*b*c
    
    return totalRibbon

    

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
            print("{} - Part 1: {} square feet of wrapping".format(file, result))
        
        if not noPartTwo:
            result = part2(copy.deepcopy(data))
            print("{} - Part 2: {} feet of ribbon".format(file, result))

if __name__ == "__main__":
    main(sys.argv[1:])