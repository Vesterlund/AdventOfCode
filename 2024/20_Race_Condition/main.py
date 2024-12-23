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
    
    
    walls = set()
    
    start_pos = 0
    end_pos = 0
    
    for i,r in enumerate(data):
        for j,c in enumerate(r):
            p = i+j*1j
            
            if c == "#":
                walls.add(p)
            
            if c == "S":
                start_pos = p
            
            if c == "E":
                end_pos = p
    
    
    
    return walls, start_pos, end_pos

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
    
    walls, start_pos, end_pos = data
    
    
    path = findPath(walls, start_pos, end_pos)
    
    cost, visited, path = path
    
    
    directions = [-1, 1j, 1, -1j]
    cuts = [2, 1+1j, 1-1j]
    
    timesave = defaultdict(int)
    
    def findCuts(point):
        for d in directions:
            if point + d in walls:
                
                for c in cuts:
                    if point + c*d in visited:
                        saved = visited[point+c*d] - visited[point] - 2
                        
                        if saved > 0:
                            timesave[saved] += 1
    

    for point in path:
        findCuts(point)
    
    fast_cuts = 0
    
    for k in timesave:
        if k >= 100:
            fast_cuts += timesave[k]
    
    return fast_cuts


def part2(data):
    
    
    walls, start_pos, end_pos = data
    
    
    path = findPath(walls, start_pos, end_pos)
    
    cost, visited, path = path
    
    # ====
    
    cheating_lvl = 20
    save_threshold = 100
    
    # ====
    
    timesave = defaultdict(int)
    
    for i, p1 in enumerate(path):
        for p2 in path[i+1:]:
            dist = abs(p1.real - p2.real) + abs(p1.imag - p2.imag)
            
            if dist <= cheating_lvl:
                saved = visited[p2] - visited[p1] - dist
                
                if saved >= save_threshold:
                    timesave[saved] += 1

    return sum(timesave.values())


    

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