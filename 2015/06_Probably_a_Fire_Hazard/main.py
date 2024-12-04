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
    
    instructions = []
    
    for row in data:
        ins = 0
        
        if row.startswith("turn on"):
            ins = 1
        elif row.startswith("turn off"):
            ins = -1
        
        c = list(map(int,re.findall(r"\d+", row)))
    
        instructions.append((ins,c))
    
    return instructions


    
def part1(data):
    
    lights = np.ones((1000,1000),dtype=np.int8)*-1
    
    for ins in data:
        t, c = ins
        
        if t == 0:
            lights[c[0]:c[2]+1,c[1]:c[3]+1] *= -1
        else:
            lights[c[0]:c[2]+1,c[1]:c[3]+1] = t
        
        
    return np.count_nonzero(lights == 1)

def part2(data):
    lights = np.zeros((1000,1000),dtype=np.int8)
    
    for ins in data:
        t, c = ins
        
        if t == 0:
            lights[c[0]:c[2]+1,c[1]:c[3]+1] += 2
        else:
            lights[c[0]:c[2]+1,c[1]:c[3]+1] += t
        
        lights[lights < 0] = 0
        
    return np.sum(lights)

    

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
            print("{} - Part 1: {} lights are on".format(file, result))
        
        if not noPartTwo:
            result = part2(copy.deepcopy(data))
            print("{} - Part 2: {} total brightness".format(file, result))

if __name__ == "__main__":
    main(sys.argv[1:])