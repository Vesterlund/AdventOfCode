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


    
def part1(data):
    
    numbers = list(map(int,re.findall(r"-?\d+", data)))

    return sum(numbers)


def part2(data):
    
    iterator = re.finditer(r"-?\d+|{|}|:\"red\"", data)
    
    def redBuffer(iterator):
        
        buffer = 0
        b_red_buffer = False
        
        for instruction in iterator:
            
            ins = instruction.group()
            
            if ins == "}":
                break
            
            if ins == "{":
                buffer += redBuffer(iterator)
                continue
            
            if ins == ":\"red\"":
                b_red_buffer = True
                continue
            
            buffer += int(ins)
        
        if b_red_buffer:
            buffer = 0
        
        return buffer
    
    
    return redBuffer(iterator)

    

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