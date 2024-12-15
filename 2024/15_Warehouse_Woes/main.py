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
    
    warehouse, instructions = fileContent.split("\n\n")
    
    warehouse = warehouse.split("\n")
    
    
    
    return warehouse, instructions


    
def part1(data):
    
    def parse(data):
        warehouse, instructions = data
        
        grid = []
        start_pos = 0 
        
        for i, row in enumerate(warehouse):
            grid.append(list(row))
            
            if "@" in row:
                start_pos = i + row.index("@") * 1j
                
        
        grid = np.asarray(grid)
        
        return grid, instructions, start_pos
        
    
    start_grid, instructions, start_pos = parse(data)    
    
    grid = np.copy(start_grid)

    def gridEntry(p):    
        return grid[int(p.real), int(p.imag)]

    def editGrid(p, c):
        grid[int(p.real), int(p.imag)] = c

    def canPush(pos, direction):
        
        pushable_objects = 0
        
        while gridEntry(pos + direction*(pushable_objects+1)) == "O":
            pushable_objects += 1

        if gridEntry(pos + direction*(pushable_objects+1)) == ".":
            return pushable_objects

        return 0
    
    pos = start_pos
    
    for ins in list(instructions):
        direction = 0
        match ins:
            case "^":
                direction = -1
            case "v":
                direction = 1
            case "<":
                direction = -1j
            case ">":
                direction = 1j
                
        next_tile = gridEntry(pos + direction)
        
        if next_tile == "#":
            continue
        
        if next_tile == ".":
            editGrid(pos, ".")
            pos += direction
            editGrid(pos, "@")
            continue
        
        n_boxes = canPush(pos, direction)
        
        if not n_boxes:
            continue
        
        p1 = pos
        p2 = pos + direction*n_boxes
        source_s_r = min(p1.real,p2.real)
        source_e_r = max(p1.real,p2.real)
        source_s_i = min(p1.imag,p2.imag)
        source_e_i = max(p1.imag,p2.imag)

        p1 += direction
        p2 += direction
        
        dest_s_r = min(p1.real,p2.real)
        dest_e_r = max(p1.real,p2.real)
        dest_s_i = min(p1.imag,p2.imag)
        dest_e_i = max(p1.imag,p2.imag)

        grid[int(dest_s_r):int(dest_e_r+1), int(dest_s_i):int(dest_e_i+1)] = grid[int(source_s_r):int(source_e_r+1), int(source_s_i):int(source_e_i+1)]
        
        editGrid(pos, ".")
        pos += direction
        editGrid(pos, "@")
        
    
    GPS_sum = 0
    
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c == "O":
                GPS_sum += 100*i + j
            
    return GPS_sum


def part2(data):
    
    def parse(data):
        warehouse, instructions = data
        
        grid = {}
        start_pos = 0
        i = 0
        for row in warehouse:
            j = 0
            for c in row:
                match c:
                    case "#":
                        grid[i+j*1j] = "#"
                        grid[i+j*1j + 1j] = "#"
                    case "O":
                        grid[i+j*1j] = "["
                        grid[i+j*1j + 1j] = "]"
                    case ".":
                        j += 2
                        continue
                    case "@":
                        grid[i+j*1j] = "@"
                        start_pos = i + j*1j
                
                j += 2

            i+= 1
            
        shape = (i,j)
        
        return grid, instructions, start_pos, shape
    
    grid, instructions, start_pos, shape = parse(data)
    
    def printGrid(grid):
        
        h,w = shape
        for i in range(h):
            
            rString = ""
            for j in range(w):
                
                p = i+j*1j
               
                if p in grid:
                    rString += grid[p]
                else:
                    rString += "."
            
            print(rString)

    
    def canMove(p, direction):
        if (p+direction) not in grid:
            return True
        
        if grid[p+direction] == "#":
            return False
        
        if grid[p+direction] == "[":
            if direction == 1j:
                return canMove(p+direction +1j, direction)
            
            return canMove(p+direction, direction) and canMove(p+direction +1j, direction)
    
        if grid[p+direction] == "]":
            if direction == -1j:
                return canMove(p+direction -1j, direction)
            return canMove(p+direction, direction) and canMove(p+direction - 1j, direction)
    
    new_grid = {}
    
    def move(pos,dir, prev=""):
        changed = set()
        if not (pos + dir) in grid:
            
            new_grid[pos+dir] = grid[pos]
            changed.add(pos)

            return changed
        
        if grid[pos+dir] == "[" and (prev != "]" or dir != -1j):
            c1 = move(pos+dir+1j, dir,prev="[")
            c2 = move(pos+dir, dir,prev="[")
            
            changed = changed.union(c1).union(c2)
        if grid[pos+dir] == "]"and (prev != "[" or dir != 1j):
            c1 = move(pos+dir-1j, dir, prev="]")
            c2 = move(pos+dir, dir, prev="]")
            
            changed = changed.union(c1).union(c2)
            
        
        new_grid[pos+dir] = grid[pos]
        
        changed.add(pos)
        
        return changed
    
    pos = start_pos
    for ins in instructions:
        
        direction = 0
        match ins:
            case "^":
                direction = -1
            case "v":
                direction = 1
            case "<":
                direction = -1j
            case ">":
                direction = 1j
        
        if not canMove(pos, direction):
            continue
        
        
        new_grid = {}
        changed = move(pos, direction)
        
        if changed:
            pos += direction
            
            for k in grid.keys():
                if k in changed:
                    continue
                
                new_grid[k] = grid[k]

            grid = new_grid.copy()

    GPS_sum = 0
    
    h,w = shape
    
    for i in range(h):
        for j in range(w):
            p = i+j*1j
            
            if p in grid and grid[p] == "[":
                GPS_sum += 100*i +j 
            
    return GPS_sum    
        
    


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