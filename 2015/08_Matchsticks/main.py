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
    
    return data


    
def part1(data):
    
    sll = 0 # String literar length
    ml = 0 # Memory length
    
    for row in data:
        sll += len(row)
        
        escaped = len(re.findall(r"\\[^x]",row[1:-1]))
        ascii = len(re.findall(r"(?<!\\)(?:\\\\)*\\x..", row[1:-1]))
        
        t = len(row[1:-1]) - escaped - 3*ascii
        ml += t

    return sll - ml


def part2(data):
    sll = 0 # String literar length
    nel = 0 # New encoding length
    
    for row in data:
        
        
        escaped = len(re.findall(r"\\[^x]",row[1:-1]))
        ascii = len(re.findall(r"(?<!\\)(?:\\\\)*\\x..", row[1:-1]))
        
        t = len(row)+ 2+2 + 2*escaped + ascii
        
        sll += len(row)
        nel += t

    return nel - sll

    

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
            print("{} - Part 1: {}".format(file, result))
        
        if not noPartTwo:
            result = part2(copy.deepcopy(data))
            print("{} - Part 2: {}".format(file, result))

if __name__ == "__main__":
    main(sys.argv[1:])