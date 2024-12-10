import sys, getopt
import numpy as np
import math
import re
from enum import Enum
import copy
import queue
from collections import defaultdict
np.set_printoptions(threshold=sys.maxsize, linewidth=sys.maxsize)

def readFile(filepath:str):
    f = open(filepath)

    fileContent = f.read()
    f.close()

    return fileContent

def parseInput(filePath:str):
    fileContent = readFile(filePath)
    data = fileContent.split("\n")
    
    grid = []
    grid.append([-1] * (len(data[0])+2))
    
    trailhead_pos = []
    
    for i, row in enumerate(data):
        
        t = [-1]
        for j, c in enumerate(row):
            if c == ".":
                c = -1
            t.append(int(c))
            
            if c == "0":
                trailhead_pos.append((1+i)+(1+j)*1j)
        
        t.append(-1)
        
        grid.append(t)
    
    
    grid.append([-1] * (len(data[0])+2))
    
    return grid, trailhead_pos


    
def part1(data):
    grid, trailhead_pos = data
    
    def walkTrail(pos, level, prev_pos= None, rlevel=0, walked=set()):
        if level == 9:
            #print("Complete!")
            return 1, walked
        
        if grid[int(pos.real)][int(pos.imag)] == -1:
            return 0, walked
        
        u = pos - 1
        d = pos + 1
        l = pos - 1j
        r = pos + 1j
        
        dirs = set([u,d,l,r])
        
        complete_trails = 0
        
        for p in dirs:
            #print(" "*rlevel,pos, p, grid[int(p.real)][int(p.imag)] )
            if p != prev_pos and grid[int(p.real)][int(p.imag)] == level + 1 and p not in walked:
                walked.add(p)
                
                c, w = walkTrail(p, level + 1, pos, rlevel= rlevel+1, walked=walked)
                complete_trails += c
                walked = walked.union(w)
                
        return complete_trails, walked
    
    

    # t = trailhead_pos[8]
    
    # c, w = walkTrail(t, 0)
    # s = ""
    # for i,r in enumerate(grid):
    #     for j,ch in enumerate(r):
    #         if(i+j*1j) in w or (i+j*1j) == t:
    #             s+=f" {str(ch)} "
    #         else:
    #             s += " . "
    #     s +="\n"
        
    # print(s,c)
    
    topo_score = 0  
    
    for t in trailhead_pos:
        c,w = walkTrail(t,0, walked=set())
        
        topo_score += c
    
 
    return topo_score


def part2(data):
    grid, trailhead_pos = data
    
    def walkTrail(pos, level, prev_pos= None, rlevel=0):
        if level == 9:
            return 1
        
        if grid[int(pos.real)][int(pos.imag)] == -1:
            return 0
        
        u = pos - 1
        d = pos + 1
        l = pos - 1j
        r = pos + 1j
        
        dirs = set([u,d,l,r])
        
        complete_trails = 0
        
        for p in dirs:
            #print(" "*rlevel,pos, p, grid[int(p.real)][int(p.imag)] )
            if p != prev_pos and grid[int(p.real)][int(p.imag)] == level + 1:
                complete_trails +=  walkTrail(p, level + 1, pos, rlevel= rlevel+1)
                
        return complete_trails
    
    scenic_score = 0  
    
    for t in trailhead_pos:
        c = walkTrail(t,0)
        
        scenic_score += c

    return scenic_score

    

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