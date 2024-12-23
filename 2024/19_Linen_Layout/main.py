import sys, getopt
import time
import numpy as np
import math
import re
from enum import Enum
import copy
import queue
from collections import defaultdict
from functools import cache
np.set_printoptions(threshold=sys.maxsize, linewidth=sys.maxsize)

def readFile(filepath:str):
    f = open(filepath)

    fileContent = f.read()
    f.close()

    return fileContent

def parseInput(filePath:str):
    fileContent = readFile(filePath)
    patterns, designs = fileContent.split("\n\n")
    
    patterns = patterns.split(", ")
    designs = designs.split("\n")
    
    
    pattern_index = defaultdict(list)
    
    for p in patterns:
        index = p[0]
        
        pattern_index[index].append(p)
    
    
    return patterns, designs, pattern_index


    
def part1(data):
    
    patterns, designs, pattern_index = data
    
    def canBuild(design):
        
        if not design:
            return True
        
        index = design[0]
        
        patterns = pattern_index[index]
        
        for p in patterns:
            pattern_length = len(p)
            
            if design[:pattern_length] == p:
                b_can = canBuild(design[pattern_length:])

                if b_can:
                    return True
        
        
        return False

    design_counter = 0

    for d in designs:
        
        b_can = canBuild(d)

        if b_can:
            design_counter += 1

        
    return design_counter


def part2(data):
    
    
    patterns, designs, pattern_index = data
    
    @cache
    def countBuild(design):
        if not design:
            return 1
        
        u_des.add(design)
        
        index = design[0]
        
        patterns = pattern_index[index]
        
        b_can = 0
        
        for p in patterns:
            pattern_length = len(p)
            
            if design[:pattern_length] == p:
                b_can += countBuild(design[pattern_length:])

        
        
        return b_can
    
    design_counter = 0
    
    for d in designs:
        
        design_counter += countBuild(d)
    
    
    return design_counter

    

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
            s_t = time.perf_counter()
            result = part1(copy.deepcopy(data))
            e_t = time.perf_counter()
            print("{} - Part 1: {} | {:.3}s".format(file, result, e_t - s_t))
        
        if not noPartTwo:
            s_t = time.perf_counter()
            result = part2(copy.deepcopy(data))
            e_t = time.perf_counter()
            print("{} - Part 2: {} | {:.3}s".format(file, result, e_t - s_t))

if __name__ == "__main__":
    main(sys.argv[1:])