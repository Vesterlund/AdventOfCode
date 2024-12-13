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
    data = fileContent.split("\n\n")
    
    machines = []
    
    for d in data:
        digits = list(map(int,re.findall(r"\d+", d)))
        
        A = np.transpose(np.reshape(digits[:4], (2,2)))
        b = np.transpose(digits[4:])
        
        machines.append((A,b))
    
    return machines


    
def part1(data):
    
    tokens = 0
    
    for machine in data:
        A,b = machine

        x = np.linalg.solve(A,b)
        
        if sum(np.sum(np.multiply(A, np.round(x,10)), 1) == b) == 2 and x[0] <= 100 and x[1] <= 100:
            tokens += sum(np.multiply(x, [3,1]))
    
    return int(tokens)


def part2(data):
    
    tokens = 0
    
    for machine in data:
        A,b = machine
        
        b = np.int64(b)
        b += 10000000000000
        
        A_inv = np.copy(A)
        A_inv *= -1
        A_inv[0,0],A_inv[1,1] = A[1,1],A[0,0]
        
        A = np.float64(A)
        x_raw = np.matmul(A_inv, b)
        
        det = (A[0,0]*A[1,1] - A[0,1]*A[1,0])
        
        x = np.float64(x_raw/det)
        
        if(all([b==0 for b in (x_raw % det)])):
            tokens += 3*x[0] + x[1]
        

    return int(tokens)

    

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