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
    
    robot_list = []
    
    for r in data:
        x1,x2,v1,v2 = list(map(int,re.findall(r"-?\d+", r)))
        
        robot_list.append((x1+x2*1j, v1+v2*1j))
    
    return robot_list


    
def part1(data):
    robot_list = data
    
    width = 101
    height = 103
    steps = 100
    
    matrix = np.zeros((height,width))
    
    for robot in robot_list:
        #print(robot)
        
        pos, vel = robot
        
        new_pos = pos + vel*steps
        proj_pos = (int(new_pos.real) % width) + (int(new_pos.imag) % height)*1j 
        #print(new_pos, proj_pos)
        
        matrix[int(proj_pos.imag)][int(proj_pos.real)] += 1
    
    
    w_half = int((width-1   )/2)
    h_half = int((height-1)/2)
    
    q2 = matrix[0:h_half, 0:w_half]
    q3 = matrix[(h_half+1):, 0:w_half]
    q1 = matrix[0:h_half, (w_half+1):]
    q4 = matrix[(h_half+1):, (w_half+1):]
    
    
    safety_factor = np.sum(q1) * np.sum(q2) *np.sum(q3) *np.sum(q4)
    
    
    # low: 
    # 87476760
    
    return safety_factor

def part2(data):
    robot_list = data
    
    width = 101
    height = 103
    
    from PIL import Image as im 
    
    def saveMatrix(m, step):
        m = (m>0).astype(int) * 255
        
        i = im.fromarray(m)
        i = i.convert("L")
        i.save(f"img/m-{step}.png")
        
    for steps in range(1,10000):
        matrix = np.zeros((height,width))
        
        for robot in robot_list:
            
            pos, vel = robot
            
            new_pos = pos + vel*steps
            proj_pos = (int(new_pos.real) % width) + (int(new_pos.imag) % height)*1j 

 
            matrix[int(proj_pos.imag)][int(proj_pos.real)] += 1
        
        saveMatrix(matrix, steps)
    
    # Lite manuellt arbete
    return 6512

    

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