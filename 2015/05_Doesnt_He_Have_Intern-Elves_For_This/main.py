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
    
    disallowed = ["ab","cd","pq","xy"]
    vowels = "aeiou"
    
    niceStrings = 0
    
    for s in data:
        prevChar = ""
        nVowel = 0
        a = False
        
        for c in s:
            if prevChar:
                if prevChar+c in disallowed:
                    a = False
                    break
                if prevChar == c:
                    a = True
            
            if c in vowels:
                nVowel += 1

            prevChar = c
        if a and nVowel >= 3:
            niceStrings+=1
    
    return niceStrings


def part2(data):
   
    niceStrings = 0
    
    for s in data:
        prevChar = ""
        prev2Char = ""
        twice = {}
        repeat= False
        preventOverlap  = False
        
        for c in s:
            if prevChar:
                if not (prevChar == prev2Char and prevChar == c and preventOverlap):
                    preventOverlap = True
                    nstr = prevChar+c
                    if nstr in twice:
                        twice[nstr] += 1
                    else:
                        twice[nstr] = 1

                else:
                    preventOverlap = False
            if prev2Char == c:
                repeat = True
                
            prev2Char = prevChar
            prevChar = c


        if max(twice.values()) > 1 and repeat:
            niceStrings+=1
    
    return niceStrings


    

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
            print("{} - Part 1: {} Number of nice strings".format(file, result))
        
        if not noPartTwo:
            result = part2(copy.deepcopy(data))
            print("{} - Part 2: {} Number of nice strings".format(file, result))

if __name__ == "__main__":
    main(sys.argv[1:])