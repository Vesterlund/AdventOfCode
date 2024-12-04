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


def sendSingals(data:list, wires={}):
    
    if len(wires)>0:
        data.pop(3)
    
    

    handledInstructions = set()
    
    resetOnValue = False
    i = 0
    while i < len(data):
        row = data[i]
        ins, dest = row.strip().split("-> ")
        i+= 1
        if ins in handledInstructions:
            continue
        
        r = 0
        try: 
            if "AND" in ins:
                a,b = ins.replace(" ", "").split("AND")
                
                x = int(a) if a.isnumeric() else wires[a]
                y = int(b) if b.isnumeric() else wires[b]
                r = x & y
            elif "OR" in ins:
                a,b = ins.replace(" ", "").split("OR")
                x = int(a) if a.isnumeric() else wires[a]
                y = int(b) if b.isnumeric() else wires[b]
                r = x | y
            elif "LSHIFT" in ins:
                a,b = ins.replace(" ", "").split("LSHIFT")
                x = int(a) if a.isnumeric() else wires[a]
                y = int(b) if b.isnumeric() else wires[b]
                r = x << y
            elif "RSHIFT" in ins:
                a,b = ins.replace(" ", "").split("RSHIFT")
                x = int(a) if a.isnumeric() else wires[a]
                y = int(b) if b.isnumeric() else wires[b]
                r = x >> y
            elif "NOT" in ins:
                a = ins[4:-1]
                x = int(a) if a.isnumeric() else wires[a]
                r = ~x
            else:
                r = int(ins) if ins[:-1].isnumeric() else wires[ins[:-1]]
            
        except KeyError as e:
            resetOnValue = True
            continue
        
            
        if r < 0:
            r = 2**16 + r
        
        wires[dest] = r
        handledInstructions.add(ins)
        
        if resetOnValue:
            resetOnValue = False
            i = 0
        
    
    return wires["a"]


def part1(data):
    return sendSingals(data)
    


def part2(data):
    
    return sendSingals(data, {"b": 3176})
    

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