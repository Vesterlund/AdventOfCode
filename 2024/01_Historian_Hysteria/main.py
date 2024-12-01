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

   

    digits = list(map(int, re.findall(r"\d+", fileContent)))
      
    leftList = digits[::2]
    rightList = digits[1::2]
      
      
    return leftList, rightList



    
def part1(data):

    left = data[0]
    right = data[1]
    
    left.sort()
    right.sort()
    
    dist = 0

    for l, r in zip(left,right):
        dist += abs(l-r)

    return dist


def part2(data):
    
    left = data[0]
    right = data[1]
    
    from collections import Counter
    
    count = Counter(right)
    
    similarity = 0
    
    for l in left:
        similarity += count[l] * l
        
    
    return similarity

    

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
            print("{} - Part 1: Total distance: {} ".format(file, result))
        
        if not noPartTwo:
            result = part2(copy.deepcopy(data))
            print("{} - Part 2: Similarity score: {} ".format(file, result))

if __name__ == "__main__":
    main(sys.argv[1:])