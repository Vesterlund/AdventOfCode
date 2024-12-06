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
    
    matrix = []
    
    matrix.append(["o"]* (len(data[0]) + 2))
    
    row = 1
    start_dir = [-1]*4
    
    start_pos = (-1,-1)
    
    for r in data:
        temp = ["o"] + list(r) + ["o"]
        matrix.append(temp)
        
        for c in r:
            if c in ["^",">","v","<"]:
                start_dir = [r.find("^"), r.find(">"), r.find("v"),r.find("<")]
                
                start_pos = (row, 1+ [start_dir[i] for i in range(len(start_dir)) if start_dir[i] != -1][0])
        row += 1
    
    matrix.append(["o"]* (len(data[0]) + 2))
    
    start_dir = -1 if (start_dir[0]!= -1) else (1 if (start_dir[2]!= -1) else 0) +  -1*1j if (start_dir[3]!= -1) else (1*1j if (start_dir[1]!= -1) else 0)
    
    start_pos = start_pos[0] + start_pos[1]*1j
    
    return matrix, start_pos, start_dir


    
def part1(data):
    matrix, start_pos, start_dir = data
    
    
    visited_set = set()
    visited_set.add(start_pos)
    
    next_tile = matrix[int(start_pos.real + start_dir)][int(start_pos.imag + start_dir)]
    
    current_pos = start_pos
    current_dir = start_dir
    
    while next_tile != "o":
        #print(current_pos, current_dir, int(current_pos.real + current_dir.real),int(current_pos.imag + current_dir.imag),next_tile)
        
        if next_tile == "#":
            current_dir *= -1j
        else:
            current_pos += current_dir
            visited_set.add(current_pos)
            
        next_tile = matrix[int(current_pos.real + current_dir.real)][int(current_pos.imag + current_dir.imag)]
    
    return len(visited_set)



def part2(data):
    
    matrix, start_pos, start_dir = data
    
    def simulateLoops(matrix):
        visited_set = set()
        visited_set.add((start_pos, start_dir))
        
        next_tile = matrix[int(start_pos.real + start_dir)][int(start_pos.imag + start_dir)]
        
        current_pos = start_pos
        current_dir = start_dir
        
        while next_tile != "o":
            #print(current_pos, current_dir, int(current_pos.real + current_dir.real),int(current_pos.imag + current_dir.imag),next_tile)
            
            if next_tile == "#":
                current_dir *= -1j
            else:
                current_pos += current_dir
                visited_set.add((current_pos, current_dir))
                
            next_tile = matrix[int(current_pos.real + current_dir.real)][int(current_pos.imag + current_dir.imag)]
            
            if((current_pos+current_dir, current_dir * (-1j if next_tile=="#" else 1)) in visited_set):
                return 1
            
        return 0

    original_path = []
    original_path.append((start_pos, start_dir))
    
    next_tile = matrix[int(start_pos.real + start_dir)][int(start_pos.imag + start_dir)]
    
    current_pos = start_pos
    current_dir = start_dir
    
    while next_tile != "o":
        if next_tile == "#":
            current_dir *= -1j
        else:
            current_pos += current_dir
            
        
            
        next_tile = matrix[int(current_pos.real + current_dir.real)][int(current_pos.imag + current_dir.imag)]

        if not next_tile =="#":
            original_path.append((current_pos, current_dir))
        
    rock_set = set()
    
    for step, direction in original_path:
        
        rock_pos = step + direction
        
        if rock_pos == start_pos:
            continue

        adj_matrix = np.copy(matrix)
        adj_matrix[int(rock_pos.real)][int(rock_pos.imag)] = "#"

        r = simulateLoops(adj_matrix)
        
        
        if r:
            rock_set.add(rock_pos)
            #print(f"Rock at: {rock_pos} causes loop!")
            #print(adj_matrix)

    return len(rock_set)


    

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