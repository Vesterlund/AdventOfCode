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
    
    width = len(data[0])
    height = len(data)
    
    matrix = np.zeros((height, width))
    
    for i in range(height):
        for j in range(width):
            v = -1
            
            match data[i][j]:
                case 'X':
                    v = 1
                case 'M':
                    v = 2
                case 'A':
                    v = 3
                case 'S':
                    v = 4
                case _:
                    break
            
            
            matrix[i][j] = v
    
    return matrix


    
def part1(data):
    def checkXMAS(pos, max_w, max_h):
        b_left_check = (pos[1] - 3 >= 0)
        b_right_check = (pos[1] + 3 <= max_w-1)
        b_up_check = (pos[0] - 3 >= 0)
        b_down_check = (pos[0] + 3 <= max_h-1)
        
        origin = pos[0] + pos[1]*1j
        
        xmas_count = 0
        
        c_set = []
        
        if b_left_check:
            c_set.append([origin - i*1j for i in range(4)])
            
            if b_up_check:
                c_set.append([origin - i*(1+1j) for i in range(4)])
            
            if b_down_check:
                c_set.append([origin + i*(1-1j) for i in range(4)])
        
        if b_right_check:
            c_set.append([origin + i*1j for i in range(4)])
            
            if b_up_check:
                c_set.append([origin - i*(1-1j) for i in range(4)])
            
            if b_down_check:
                c_set.append([origin + i*(1+1j) for i in range(4)])
        
        if b_up_check:
            c_set.append([origin - i for i in range(4)])
            
        if b_down_check:
            c_set.append([origin + i for i in range(4)])
        
        
        for c in c_set:
            s = ""
            
            for p in c:
                x,y = int(np.real(p)), int(np.imag(p))
      
                s += str(int(data[x][y]))
            
            if s=="1234":
                xmas_count += 1
        
        return xmas_count
        
    total_xmas = 0
    
    max_w = len(data[0])
    max_h = len(data)
    
    for i in range(max_h):
        for j in range(max_w):
            
            if data[i][j] == 1:
                total_xmas += checkXMAS((i,j), max_w, max_h)
    
    
    return total_xmas


def part2(data):
    def checkX_MAS(pos, max_w, max_h):
        
        b_box_check = (pos[1] - 1 >= 0) and (pos[1] + 1 <= max_w-1) and (pos[0] - 1 >= 0) and (pos[0] + 1 <= max_h-1)
        
        origin = pos[0] + pos[1]*1j
        
        xmas_count = 0
        
        c_set = []
        
        if b_box_check:
            c_set.append([origin + i*(1+1j) for i in range(-1,2)])
            c_set.append([origin - i*(1-1j) for i in range(-1,2)])
        
        
        for c in c_set:
            s = ""
            
            for p in c:
                x,y = int(np.real(p)), int(np.imag(p))
      
                s += str(int(data[x][y]))
            
            if s=="234" or s=="432":
                xmas_count += 1
        
        if xmas_count == 2:
            return 1
        
        return 0
    
    
    total_xmas = 0
    
    max_w = len(data[0])
    max_h = len(data)
    for i in range(max_h):
        for j in range(max_w):
            
            if data[i][j] == 3:
                # print(f"A: {i},{j}")
                total_xmas += checkX_MAS((i,j), max_w, max_h)
  
    
    
    return total_xmas

    

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