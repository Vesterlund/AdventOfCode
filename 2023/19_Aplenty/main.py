import sys, getopt
import numpy as np
import math
import re


def readFile(filepath:str):
    f = open(filepath)

    fileContent = f.read()
    f.close()

    return fileContent

class Part():
    def __init__(self, l) -> None:
        self.x = l[0]
        self.m = l[1]
        self.a = l[2]
        self.s = l[3]
        
    def __str__(self) -> str:
        return "x={}, m={}, a={}, s={}".format(self.x,self.m,self.a,self.s)

class Instruction():
    
    def __init__(self, var, val, op, trueRes) -> None:
        self.var = var
        self.val = val
        self.op = op
        self.trueRes = trueRes
        
    def isTrue(self,p):
        pVal = -1
        
        match self.var:
            case "x": pVal = p.x
            case "m": pVal = p.m
            case "a": pVal = p.a
            case "s": pVal = p.s
        
        return pVal < self.val if self.op == "<" else pVal > self.val
             

class WorkFlow():
    instructions= []
    
    
    def __init__(self, ins, finalDest) -> None:
        self.instructions : list(Instruction) = ins
        self.finalDest = finalDest # If no instruction is true 
    
    
    def findResult(self, p : Part):
        
        for ins in self.instructions:
            if ins.isTrue(p):
                return ins.trueRes

        return self.finalDest
        
def parseInput(filePath:str):
    fileContent = readFile(filePath)


    data = fileContent.split("\n\n")
    
    instructions = data[0].split("\n")
    partList = data[1].split("\n")
    
    workDict = {}
    
    for ins in instructions:
        a = ins.split("{")
        
        i = a[1].split(",")
        
        temp = []
        for ti in i[:-1]:
            temp.append(Instruction()
        
        print(a)
    
    parts = []
    for sPart in partList:
        t = [int(x) for x in re.findall(r"(\d+)", sPart)]
        parts.append(Part(t))
    
    for p in parts:
        print(p)
    
    return 


def part1(data):
    return
def part2(data):
    return
    

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
            result = part1(data)
            print("{} - Part 1: {} cubic meters".format(file, result))
        
        if not noPartTwo:
            result = part2(data)
            print("{} - Part 2: {} cubic meters".format(file, result))

if __name__ == "__main__":
    main(sys.argv[1:])