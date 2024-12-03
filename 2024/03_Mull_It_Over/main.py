import sys, getopt
import numpy as np
import math
import re

import copy
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
    
    mul_instructions = re.findall(r"mul\(\d+,\d+\)", data)
    
    
    result = 0

    for m in mul_instructions:
        numbers = list(map(int,re.findall(r"\d+", m)))

        result += numbers[0] * numbers[1]

    return result


def part2(data):
    
    instructions = re.findall(r"mul\(\d+,\d+\)|do\(\)|don't\(\)", data)
    
    result = 0
    b_mult = True 
    
    for i in instructions:
        
        if i == "do()":
            b_mult = True
        elif i == "don't()":
            b_mult = False
        else:
            if b_mult:
                numbers = list(map(int,re.findall(r"\d+", i)))

                result += numbers[0] * numbers[1]
    
    
    return result

    

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
            print("{} - Part 1: Memory Results: {} ".format(file, result))
        
        if not noPartTwo:
            result = part2(copy.deepcopy(data))
            print("{} - Part 2: Memory Results: {} ".format(file, result))

if __name__ == "__main__":
    main(sys.argv[1:])