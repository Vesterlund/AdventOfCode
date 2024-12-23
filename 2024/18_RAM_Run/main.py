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
    data = fileContent.split("\n")
    
    byte_positions = []
    
    for r in data:
        b = list(map(int,re.findall(r"\d+",r)))
        
        byte_positions.append((b[1], b[0]))
    
    
    return byte_positions

def createWalls(shape):
    
    walls =  {}
    
    
    walls_coord = [-1 + i*1j for i in range(-1,shape+1)] + [shape + i*1j for i in range(-1,shape+1)] + [i -1j for i in range(-1,shape+1)]  + [i + shape*1j for i in range(-1,shape+1)] 
    
    for w in walls_coord:
        walls[w] = "#"
    
    return walls

def printGrid(shape, walls, visited={}):
    r = ""
    for i in range(-1, shape+1):
        
        for j in range(-1, shape+1):
            p =  i+j*1j
            if p in walls:
                r+= "#"
                continue
            
            if p in visited:
                r+="O"
                continue
            
            r+= "."
            
            
        r += "\n"

    print(r)

def findPath(walls, start_pos, end_pos):
    
    pq = queue.PriorityQueue()
   
    pq.put((0, 0, start_pos, [start_pos]))
    
    visited = {}
    
    
    extra_order = 1

    shortest_cost = -1
    shortest_tail = []
    
    while not pq.empty():
        cost,_, pos, tail = pq.get()
        
        if pos in visited:
            continue
        
        visited[pos] = cost
        
        if pos == end_pos:
            shortest_cost = cost
            shortest_tail = tail
            break
        
        directions = [1j**i for i in range(4)]
        
        for d in directions:
            if pos + d in walls:
                continue
            
            pq.put((cost + 1,extra_order, pos + d, tail + [pos+d]))
            extra_order += 1

    return shortest_cost, visited, shortest_tail
    
def part1(data):
    byte_positions = data
    
    # =============
    shape = 71
    read_bytes = 12 if shape == 7 else 1024
    # =============
    
    boundry_walls = createWalls(shape)
    
    walls = boundry_walls.copy()
    
    #printGrid(shape, boundry_walls)
    for i in range(read_bytes):
        bp = byte_positions[i]
        p = bp[0] + bp[1]*1j
        
        walls[p] = "#"
    
    start_pos = 0
    end_pos = (shape-1)*(1+1j)
    
    #printGrid(shape, walls)
    
    cost, v, tail = findPath(shape, walls, start_pos, end_pos)
    printGrid(shape, walls, tail)
    
    
    return cost

def part2(data):
    
    byte_positions = data
    
    # =============
    shape = 71
    p_comp = 12 if shape==7 else 1024
    read_bytes = len(byte_positions)
    # =============
    
    boundry_walls = createWalls(shape)
    
    walls = boundry_walls.copy()
    
    start_pos = 0
    end_pos = (shape-1)*(1+1j)
    
    for i in range(p_comp):
        bp = byte_positions[i]
        p = bp[0] + bp[1]*1j
        
        walls[p] = "#"
    
    tail = []
    
    for i in range(p_comp, read_bytes):
        print(f"Fallen bytes: {i}/{read_bytes}")
        
        bp = byte_positions[i]
        p = bp[0] + bp[1]*1j
        
        walls[p] = "#"
        
        if tail and p not in tail:
            continue
        
        cost, _, tail = findPath(shape, walls, start_pos, end_pos)
        
        if cost == -1:
            print(f"Byte: {i}, at: {str(bp[1])},{str(bp[0])}")
            return f"{str(bp[1])},{str(bp[0])}"
        
        
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