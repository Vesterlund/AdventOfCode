import sys, getopt
import numpy as np
import math
import re
from enum import Enum
import copy
np.set_printoptions(threshold=sys.maxsize, linewidth=sys.maxsize)

def readFile(filepath:str):
    f = open(filepath)

    fileContent = f.read()
    f.close()

    return fileContent

def parseInput(filePath:str):
    fileContent = readFile(filePath)


    data = fileContent.split("\n")
    
    bricks = {}
    
    for i, row in enumerate(data):
        b = row.split("~")
        sp = tuple(map(int,b[0].split(",")))
        ep = tuple(map(int,b[1].split(",")))
        
        id = chr(ord('@')+i+1)
        bricks[id] = Brick(sp,ep,id)
    
    return bricks

class Point():
    
    def __init__(self,p) -> None:
        self.x, self.y, self.z = p
    
    def __str__(self) -> str:
        return "({},{},{})".format(self.x,self.y,self.z)
    
    def __hash__(self) -> int:
        return hash(self.x,self.y,self.z)


class Brick():
    
    def __init__(self, s, e,i) -> None:
        self.supportedBy = set()
        self.supports = set()
        self.start = Point(s)
        self.end = Point(e)
        self.id = i

    def __hash__(self) -> int:
        return hash(self.id)
    
    def __str__(self) -> str:
        return "{}: {} -> {}".format(self.id, self.start, self.end)
    
    def getRange(self):
        t = []
        for x in range(self.start.x, self.end.x+1):
            for y in range(self.start.y, self.end.y+1):
                t.append((x,y))
        return t

    def __lt__(self, other):
        return self.id < other.id

class Space():
    
    
    
    def __init__(self) -> None:
        self.floor = 1
        self.maxVals = [0,0,0]
        self.occupiedCoordinates = {}
    
    def rangeIsUnoccupied(self, r, z):
        
        for p in r:
            if (*p, z) in self.occupiedCoordinates:
                return False
            
        return True
    
    def placeBrick(self, brick):
        #while all space (x,y,z-1) below brick is empty
        startZ = brick.start.z
        bRange = brick.getRange()
        
        currZ = startZ
        
        while self.rangeIsUnoccupied(bRange, currZ-1) and currZ > self.floor:
            currZ -= 1
        
        for p in bRange:
            if (*p, currZ-1) in self.occupiedCoordinates:
                brick.supportedBy.add(self.occupiedCoordinates[(*p,currZ-1)])
        
        
        self.maxVals[2] = max(currZ, self.maxVals[2])
        for p in bRange:
            if startZ != brick.end.z:
                for i in range(0, brick.end.z - brick.start.z + 1):
                    self.occupiedCoordinates[(*p, currZ+i)] = brick.id
                    self.maxVals[2] = max(currZ+i, self.maxVals[2])
            else:
                self.occupiedCoordinates[(*p, currZ)] = brick.id
                self.maxVals[0] = max(p[0], self.maxVals[0])
                self.maxVals[1] = max(p[1], self.maxVals[1])
    
        
    def findAllAt(self,xR,yR,zR):
        
        t = []
        
        for x in range(xR[0],xR[-1]+1):
            for y in range(yR[0], yR[-1]+1):
                for z in range(zR[0], zR[-1]+1):
                    if (x,y,z) in self.occupiedCoordinates:
                        t.append(self.occupiedCoordinates[(x,y,z)])

        return t

    
    def printSpace(self, dim):
        if dim == 1: self.printXZ()
        if dim == 2: self.printYZ()
    
    def printYZ(self):
        temp = "-"*(self.maxVals[0]+1)
        
        
        for z in range(1, self.maxVals[2]+1):
            tRow = ""
            
            for y in range(0, self.maxVals[1]+1):
               
               row = self.findAllAt([0, self.maxVals[0]+1], [y], [z])
               t = str(row[0]) if len(row) >= 1 else "."
               
               tRow += t
               
            temp = tRow + "\n"+ temp

        print(temp)
    
    def printXZ(self):
        temp = "-"*(self.maxVals[0]+1)
        
        
        for z in range(1, self.maxVals[2]+1):
            tRow = ""
            
            for x in range(0, self.maxVals[0]+1):
               
               row = self.findAllAt([x], [0, self.maxVals[1]+1], [z])
               t = str(row[0]) if len(row) >= 1 else "."
               
               tRow += t
               
            temp = tRow + "\n"+ temp
        print(temp)

from queue import PriorityQueue
from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class PItem:
    priority: int
    item: Any=field(compare=False)

def calculateSupports(bricks):
    
    for k in bricks:
        b = bricks[k]
        
        for s in b.supportedBy:
            bricks[s].supports.add(k)

def simulateBricks(bricks):
    pq = PriorityQueue()
    for k in bricks:
        b = bricks[k]
        pq.put((b.start.z, b))
    
    space = Space()
    
    # In order of z-level
    while not pq.empty():
        b = pq.get()[1]
        space.placeBrick(b)
    
    #space.printSpace(1)
    #space.printSpace(2)
    
    calculateSupports(bricks)
    
    return bricks
def part1(data):
    bricks = data

    simulateBricks(bricks)
    
    removableBricks = set()
    
    for k in bricks:
        b = bricks[k]
        removable = all([1 if len(bricks[s].supportedBy) > 1 else 0 for s in b.supports])
        
        if removable:
            removableBricks.add(k)

    return len(removableBricks)


from functools import cache
from queue import Queue

def willFall(bricks, k):
    b = bricks[k]
    hasFallen : set = {k}
    hasChecked = set()
    q = Queue()

    for s in b.supports:
        q.put(s)
        
    while not q.empty():
        b = bricks[q.get()]
        
        if all(x in hasFallen for x in b.supportedBy): # If all bricks that supports this brick has falleen, this one falls as well
            hasFallen.update(b.id)
            for s in b.supports:
                q.put(s)
        
    hasFallen.remove(k)
    
    return hasFallen   

def part2(data):
    bricks = data

    simulateBricks(bricks)
    
    totalFall = 0
    
    for k in bricks:
        
        totalFall += len(willFall(bricks, k))

    return totalFall

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
            print("{} - Part 1: {} Bricks can be disintegrated".format(file, result))
        
        if not noPartTwo:
            result = part2(copy.deepcopy(data))
            print("{} - Part 2: {} Sum of other bricks that fall ".format(file, result))

if __name__ == "__main__":
    main(sys.argv[1:])