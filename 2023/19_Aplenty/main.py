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
        l = list(map(int,l))
        self.x = l[0]
        self.m = l[1]
        self.a = l[2]
        self.s = l[3]
        
    def __str__(self) -> str:
        return "x={}, m={}, a={}, s={}".format(self.x,self.m,self.a,self.s)
    
    def sum(self) -> int:
        return self.x + self.m + self.a + self.s

class Instruction():
    
    def __init__(self, var, val, op, trueRes) -> None:
        self.var = var
        self.val = int(val)
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
    
    def modifyRange(self, r):
        pos = 0 if self.op == ">" else 1
        i = 0
        match self.var:
            case "x": i = 0
            case "m": i = 1
            case "a": i = 2
            case "s": i = 3

        trueRange = copy.deepcopy(r)
        falseRange = copy.deepcopy(r)

        trueRange[self.var][pos] = self.val + (-1 if pos else 1)
        falseRange[self.var][(pos + 1) % 2] = self.val

        return trueRange, falseRange

    def __hash__(self) -> int:
        return hash((self.var,self.val, self.op, self.trueRes))

    def __str__(self) -> str:
        return "{} {} {} -> {}".format(self.var, self.op, self.val, self.trueRes)
import copy 

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
    
    def createRanges(self, r):
        cR = copy.deepcopy(r)
        outRanges = []
        for ins in self.instructions:
            a, cR = ins.modifyRange(cR)
            outRanges.append((ins.trueRes,a))
        outRanges.append((self.finalDest,cR))
        return outRanges

    def __str__(self) -> str:
        rString = ""
        for ins in self.instructions:
            rString += str(ins) + "\n"
        
        return rString + "finally: {}".format(self.finalDest)
        
def parseInput(filePath:str):
    fileContent = readFile(filePath)


    data = fileContent.split("\n\n")
    
    instructions = data[0].split("\n")
    partList = data[1].split("\n")
    
    workDict = dict()
    
    for ins in instructions:
        a = ins.split("{")
        
        i = a[1].split(",")
        
        temp = []
        for ti in i[:-1]:
            op = "<" if "<" in ti else ">"
            c = ti.split(op)
            v = c[1].split(":")
            temp.append(Instruction(c[0], v[0],op,v[1]))
        
        work = WorkFlow(temp, i[-1][:-1])
        workDict[a[0]] = work
    
    parts = []
    for sPart in partList:
        t = [int(x) for x in re.findall(r"(\d+)", sPart)]
        parts.append(Part(t))

    return workDict, parts


def part1(data):
    workDict, parts = data

    totalSum = 0
    
    for p in parts:
        startIns = "in"
        currIns = startIns

        while currIns not in ["A", "R"]:
            currFlow : WorkFlow = workDict[currIns]
            currIns = currFlow.findResult(p)

        if currIns == "A":
            totalSum += p.sum()

    return totalSum

def part2(data):
    workDict, _ = data
    ranges = {
        "x": [1,4000],
        "m": [1,4000],
        "a": [1,4000],
        "s": [1,4000]
    }
    currKey = "in"

    ranges = workDict[currKey].createRanges(ranges)

    finalRanges = []
    tempRanges = ranges
    while tempRanges:
        tempRanges = []
        for k, r in ranges:
            if k == "A":
                finalRanges.append(r)
                continue
            elif k== "R":
                continue
            
            t = workDict[k].createRanges(r)
            tempRanges += t

        ranges = tempRanges

    totalComb = 0
    for fr in finalRanges:
        m = 1
        for key in fr:
            m *= fr[key][1] - fr[key][0]+1
        totalComb += m
    return totalComb
    

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
            print("{} - Part 1: {} Total ratings for all parts  ".format(file, result))
        
        if not noPartTwo:
            result = part2(data)
            print("{} - Part 2: {} Total different part combinations ".format(file, result))

if __name__ == "__main__":
    main(sys.argv[1:])