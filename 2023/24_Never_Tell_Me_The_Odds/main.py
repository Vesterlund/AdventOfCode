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
    
    lineList = []
    
    for i,row in enumerate(data):
        l = list(map(int,re.findall(r"-?\d+", row)))
        id = chr(ord('@')+i+1)
        lineList.append(Line(l[0:3], l[3:],id))    

    
    return lineList

class Line():
    
    def __init__(self,p:list, v, id) -> None:
        self.p = np.array(p)
        self.v = np.array(v)
        self.id = id
        
        self.x, self.y, self.z = p
        self.vx, self.vy, self.vz = v
    
    def __str__(self) -> str:
        return "{}, {}, {} @ {}, {}, {}".format(self.x,self.y,self.z,self.vx,self.vy,self.vz)
    
    def isParallelTo(self, other):
        
        return not all((a % b == 0) for a,b in zip(self.v, other.v))
    
    def isPointInPast(self,point):
        return (point[0] - self.x) / self.vx < 0  
    
    def intersect2d(self, other) -> (bool, float, float):
        pDiff = self.p[:2] - other.p[:2]
        
        vCross = np.cross(self.v[:2], other.v[:2])
        
        if vCross == 0:
            return False, -1, -1
        
        t = np.cross(pDiff, other.v[:2]) / vCross
        u = np.cross(pDiff, self.v[:2]) / vCross
        
        return True, self.x - self.vx*t, self.y-self.vy*t
      
        
def checkInBound(bMin, bMax, point):
    
    return all(bMin <= c and c <= bMax for c in point)
        
def part1(data):
    lineList = data

    bMin = 200000000000000
    bMax = 400000000000000
    
    insideBounds = 0
 
    for i, line1 in enumerate(lineList[:-1]):
        for line2 in lineList[i+1:]:
            intersects, x, y = line1.intersect2d(line2)
            
            if intersects:
                if not line1.isPointInPast((x,y)) and not line2.isPointInPast((x,y)):
                    if checkInBound(bMin, bMax, (x,y)):
                        insideBounds += 1
    
    return insideBounds


def part2(data):
    
    import sympy as sp
    from sympy.solvers import solve
    
    equationList = []
    x,y,z,vx,vy,vz = sp.symbols("x,y,z,vx,vy,vz")
    
    for i,line in enumerate(data[:3]): 
        t = sp.symbols("t{}".format(i))
        equationList.append(sp.Eq(x+t*vx-line.x-t*line.vx,0))
        equationList.append(sp.Eq(y+t*vy-line.y-t*line.vy,0))
        equationList.append(sp.Eq(z+t*vz-line.z-t*line.vz,0))
     
    output = solve(equationList)

    return output[0][x] + output[0][y] + output[0][z]

    

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
            print("{} - Part 1: {} Future points are within the bound".format(file, result))
        
        if not noPartTwo:
            result = part2(copy.deepcopy(data))
            print("{} - Part 2: {} Sum of starting position coordinates ".format(file, result))

if __name__ == "__main__":
    main(sys.argv[1:])