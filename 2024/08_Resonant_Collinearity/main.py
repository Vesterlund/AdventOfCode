import sys, getopt
import numpy as np
import math
import re
from enum import Enum
import copy
import queue
from collections import defaultdict
np.set_printoptions(threshold=sys.maxsize, linewidth=sys.maxsize)

def readFile(filepath:str):
    f = open(filepath)

    fileContent = f.read()
    f.close()

    return fileContent

def parseInput(filePath:str):
    fileContent = readFile(filePath)
    data = fileContent.split("\n")
    
    antenna_positions = defaultdict(list)
    
    i = 0
    for row in data:
        j = 0
        for c in row:
            if c != ".":
                antenna_positions[c].append(i+j*1j)
            j+= 1
        i+= 1

    grid_size = (len(data), len(data[0]))

    return antenna_positions, grid_size


    
def part1(data):
    antenna_positions, grid_size = data
    
    def inGrid(pos):
        return (0 <= pos.real) and (pos.real < grid_size[0]) and (0 <= pos.imag) and (pos.imag < grid_size[1]) 
        
    antinodes = set()

    for k in antenna_positions.keys():
        positions = antenna_positions[k]
        
        for i in range(len(positions)):
            for j in range(i+1, len(positions)):
                a,b = positions[i], positions[j]
                
                a1 = 2*a - b
                a2 = 2*b - a
                if(inGrid(a1)):
                    antinodes.add(a1)
                    
                if(inGrid(a2)):
                    antinodes.add(a2)
                
    
    return len(antinodes)


def part2(data): 
    antenna_positions, grid_size = data
    
    def inGrid(pos):
        return (0 <= pos.real) and (pos.real < grid_size[0]) and (0 <= pos.imag) and (pos.imag < grid_size[1]) 
        
    antinodes = set()

    for k in antenna_positions.keys():
        positions = antenna_positions[k]
        
        for i in range(len(positions)):
            for j in range(i+1, len(positions)):
                a,b = positions[i], positions[j]

                diff = b - a 
                
                pos = a
                while inGrid(pos):
                    antinodes.add(pos)
                    
                    pos += diff
                
                pos = a
                while inGrid(pos):
                    antinodes.add(pos)
                    
                    pos -= diff
                    
                
                
    return len(antinodes)

    

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