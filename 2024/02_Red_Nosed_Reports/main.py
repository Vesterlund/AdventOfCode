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

    reports = fileContent.split("\n")

    def helper(r):
        return list(map(int, r.split(" ")))

    reports = list(map(helper, reports))
      
      
    return reports



    
def part1(data):

    validReports = 0
    
    for r in data:
        sign = np.sign(r[0] - r[1])
        prevVal = r[0]
        
        valid = True
        
        
        
        for value in r[1:]:
            #print(prevVal, value)
            if 1 <= abs(prevVal - value) and abs(prevVal - value) <= 3 and np.sign(prevVal - value) == sign:
                prevVal = value
            else:
                valid = False
                break
        
        if valid:
            validReports += 1
        
   

    return validReports


def part2(data):
    validReports = 0
    
    for r in data:
        diffs = []

        prevVal = None
       
        
        for value in r:
            
            if prevVal == None:
                prevVal = value
                continue
            
        
            diffs.append(value-prevVal)
            
            prevVal = value
        
        # Find index of unsafe entry
        # Recompute diffs
        # Find if any breaks again
        
       
        from collections import Counter
    
    
        count = Counter(np.sign(diffs))
        
        major_sign = max(count, key=count.get)
        
        b_sign = True
        i_sign = -1
        
        if len(count.keys()) > 2:
            b_sign = False
        
        if len(count.keys()) == 2:
            temp = count.keys()
            
            for k in temp:
                if k == major_sign:
                    continue
                
                if count[k] > 1:
                    b_sign = False
                    

        
        b_range = sum(1 for d in diffs if (d<-3 or d > 3)) <= 1
        
        

        if b_sign and b_range:
            validReports += 1

    return validReports

    

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
            print("{} - Part 1: Valid reports: {} ".format(file, result))
        
        if not noPartTwo:
            result = part2(copy.deepcopy(data))
            print("{} - Part 2: Safe reports: {} ".format(file, result))

if __name__ == "__main__":
    main(sys.argv[1:])