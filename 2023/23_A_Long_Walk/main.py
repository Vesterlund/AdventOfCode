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
    
    return data
    
    

class Junction():
    
    def __init__(self,p) -> None:
        self.x,self.y = p

    def getPos(self):
        return (self.x, self.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def __eq__(self, __value) -> bool:
        return self.x == __value.x and self.y == __value.y
    
    def __str__(self) -> str:
        return "J: ({},{})".format(self.x,self.y)
    
class Edge():
    
    def __init__(self, fJunc : Junction, tJunc : Junction, dist, nodes : list) -> None:
        self.fJunc = fJunc
        self.tJunc = tJunc
        self.dist = dist
        self.nodes = nodes

    def __str__(self) -> str:
        return "{} - {} -> {}".format(self.fJunc, self.dist, self.tJunc)
    
def traverseDirection(snowMap, startPos, dir):
    nodes = []
    
    sp = complex(startPos[0], startPos[1])
    
    np = sp + dir
    pp = sp
    
    checkDirs = [1+0j, -1+0j, 0+1j, 0-1j]
    
    nChar = snowMap[int(np.real)][int(np.imag)]
    
    nodes = [sp,np]
    
    while nChar not in ["^", ">", "v", "<"]:
        dir = pp - np
        
        #print("{}  {}-> {} ({})".format(pp,-1*dir,np, nChar))
        pp = np

        for d in checkDirs:
            tp = np + d
            
            x,y = int(tp.real), int(tp.imag)
            
            #If we find end node
            if x == len(snowMap):
                nodes.remove(np)
                return len(nodes)+1, np, nodes 
            
            if d == dir or snowMap[x][y] == "#":
                continue
            
            
            np = tp
            
            nodes.append(np)
            break
            
        nChar = snowMap[int(np.real)][int(np.imag)]
 
    
    for d in [(1+0j,"v"), (-1+0j,"^"), (0+1j,">"), (0-1j,"<")]:
        if nChar == d[1]:
            np = np + d[0]
            break
    
    
    return len(nodes)+1, np, nodes
    
    

def findNextJunctions(snowMap, j : Junction):
    x,y = j.getPos()
    
    junctions = []
    edges = []
     
    if j.getPos() == (0,1):
        dist, nextPos, nodes = traverseDirection(snowMap, (x+1,y), 0+1j)
        nj = Junction((int(nextPos.real), int(nextPos.imag)))
        e = Edge(j,nj,dist, nodes)
        
        junctions.append(nj)
        edges.append(e)
        
        return junctions, edges
    
   
    pDirs = [(1+0j,"v"), (-1+0j,"^"), (0+1j,">"), (0-1j,"<")]
    
    for dirs in pDirs:   
        p = complex(x,y)
        np = p + dirs[0]
        nx = int(np.real)
        ny = int(np.imag)
        
        if nx >= len(snowMap):
            continue
        
        if snowMap[nx][ny] == dirs[1]:
            dist, np, nodes = traverseDirection(snowMap, (nx,ny), dirs[0])
            nj = Junction((int(np.real), int(np.imag)))
            e = Edge(j,nj,dist, nodes)
            
            junctions.append(nj)
            edges.append(e)
            
    return junctions, edges

from queue import Queue

def distToGoal(j, end, edgeDict, stepsToHere):
    if j == end:
        return [stepsToHere]

    t = []
    
    for e in edgeDict[j]:
        d = distToGoal(e.tJunc, end, edgeDict, stepsToHere + e.dist)    
        t += d
        
    return t

def buildEdgeGraph(data, startJunction):

    
    q = Queue()
    q.put(startJunction)
    
    hasVisited = set()
    edgeDict = {}
    
    while not q.empty():
        j : Junction = q.get()
        
        if j in hasVisited:
            continue
        
        hasVisited.add(j)
        fj = findNextJunctions(data,j)

        edgeDict[j] = []
        
        for edge in fj[1]:
            edgeDict[j].append(edge)
        
        for junk in fj[0]:
            if junk not in hasVisited:
                q.put(junk)
    
    return edgeDict

def part1(data):
    startJunction = Junction((0,1))
    endJunction = Junction((len(data)-1, len(data[0])-2))
    
    edgeDict = buildEdgeGraph(data, startJunction)
    
    dist = distToGoal(startJunction, endJunction, edgeDict, 0)
    
    return max(dist)

def undirectEdgeGraph(edgeDict):
    temp = copy.deepcopy(edgeDict)

    
    for key in temp:
        if not temp[key]:
            continue
        for e in temp[key]:
            
            if e.tJunc not in edgeDict:
                edgeDict[e.tJunc] = [Edge(e.tJunc, e.fJunc, e.dist, e.nodes)]
            else:
                edgeDict[e.tJunc].append(Edge(e.tJunc, e.fJunc, e.dist, e.nodes))



maxSteps = 0

def longPath(j, end, edgeDict, stepsToHere, visited):
    global maxSteps
    if j == end:
        maxSteps = max(maxSteps, stepsToHere)
        return 
    
    for e in edgeDict[j]:
        if e.tJunc not in visited:
            visited.add(e.tJunc)
            longPath(e.tJunc, end, edgeDict, stepsToHere + e.dist, visited)

            visited.remove(e.tJunc)
        
    return maxSteps



def part2(data):
    startJunction = Junction((0,1))
    endJunction = Junction((len(data)-1, len(data[0])-2))
    
    edgeDict = buildEdgeGraph(data, startJunction)
    undirectEdgeGraph(edgeDict)
  
    return longPath(startJunction, endJunction, edgeDict, 0, {startJunction})
    

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
            print("{} - Part 1: {} Steps are in the longest hike".format(file, result))
        
        if not noPartTwo:
            result = part2(copy.deepcopy(data))
            print("{} - Part 2: {} Sum of other bricks that fall ".format(file, result))

if __name__ == "__main__":
    main(sys.argv[1:])