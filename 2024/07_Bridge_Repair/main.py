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
    
    equations = []
    
    for row in data:
        result, parts = row.split(":")
        parts = list(map(int, re.findall(r"\d+", parts)))

        equations.append((int(result), parts))
    
    return equations

    
def part1(data):
    equations = data
    
    
    def calc(val, parts, target):
        if not parts:
            return (val == target)
        
        temp1 = val + parts[0]
        temp2 = val * parts[0]

        
        if calc(temp1, parts[1:], target):
            return True
        
        return calc(temp2, parts[1:], target)
    
    test_sum = 0    
    
    for eq in equations:
        result, parts = eq    
        
        if calc(parts[0],parts[1:],result):
            test_sum += result

    return test_sum


def part2(data):
    equations = data
    
    
    def calc(val, parts, target):
        if not parts:
            return (val == target)
        
        temp1 = val + parts[0]
        temp2 = val * parts[0]
        temp3 = int(str(val) + str(parts[0]))

        
        if calc(temp1, parts[1:], target):
            return True
        
        if calc(temp2, parts[1:], target):
            return True    

        return calc(temp3, parts[1:], target)
    
    test_sum = 0    
    
    for eq in equations:
        result, parts = eq    
        
        if calc(parts[0],parts[1:],result):
            test_sum += result

    return test_sum

    

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