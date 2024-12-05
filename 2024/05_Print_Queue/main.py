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
    data = fileContent.split("\n\n")
    
    order = re.findall(r"\d+\|\d+", data[0])
    lists = re.findall(r"\d+(?:,\d+)*", data[1])

    
    return order, lists


    
def part1(data):
    order, updates = data
    
    order_set = set()
    
    for o in order:
        o = list(map(int, o.split("|")))
        
        order_set.add((o[0], o[1]))
    
    
    def checkInvalidUpdate(u):
        l = len(u)
        
        for i in range(l):
            
            f_e = u[i]
            
            for j in range(i+1,l):
                s_e = u[j]
                
                if (s_e, f_e) in order_set:
                    return True

        
        return False

    middleSum = 0
    
    for u in updates:
        u = list(map(int, u.split(",")))
        
        b_invalid_update = checkInvalidUpdate(u)

        if not b_invalid_update:
            middleSum += u[math.ceil(len(u)/2)-1]
                
    return middleSum


def part2(data):
    order, updates = data
    
    order_set = set()
    
    for o in order:
        o = list(map(int, o.split("|")))
        
        order_set.add((o[0], o[1]))
    
    def checkInvalidUpdate(u):
        l = len(u)
        
        for i in range(l):
            
            f_e = u[i]
            
            for j in range(i+1,l):
                s_e = u[j]
                
                if (s_e, f_e) in order_set:
                    return True

        
        return False

    def reorderUpdate(u):
        l = len(u)
        
        i = 0
        
        while i < l:
            
            
            f_e = u[i]
            
            for j in range(i+1,l):
                s_e = u[j]
                
                if (s_e, f_e) in order_set:
                    u[i], u[j] = u[j], u[i]
                    i = 0
                    
                    break

            i += 1
        return u

    middleSum = 0
    
    for u in updates:
        u_i = list(map(int, u.split(",")))
        
        b_invalid_update = checkInvalidUpdate(u_i)

        if b_invalid_update:
  
            while checkInvalidUpdate(u_i):
                u_i = reorderUpdate(np.copy(u_i))
            
            middleSum+= u_i[math.ceil(len(u_i)/2)-1]
            
    
 
    return middleSum

    

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