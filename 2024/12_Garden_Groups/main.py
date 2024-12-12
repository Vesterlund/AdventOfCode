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
    
    matrix = []
    matrix.append(["."]*(len(data[0]) + 2))
    
    for row in data:
        matrix.append(["."] + list(row)+["."])
    
    matrix.append(["."]*(len(data[0]) + 2))
    
    def findPlot(pos):
        x,y = int(pos.real), int(pos.imag)
        
        c = matrix[x][y]
        
        plot_points = set()
        
        explore_points = [pos]
        
        while explore_points:
            p = explore_points.pop(0)
            
            if matrix[int(p.real)][int(p.imag)] != c or p in plot_points:
                continue
            
            plot_points.add(p)
            
            u = p - 1
            d = p + 1
            l = p - 1j
            r = p + 1j
            
            explore_points += [u,d,l,r]
                        

        return plot_points
    
    w,h  = len(matrix[0]), len(matrix)
    explored_points = set()
    
    plots_list = []
    
    for i in range(w):
        for j in range(h):
            c = matrix[i][j]
            
            p = i+j*1j
            
            if p not in explored_points and c != ".":
                pts = findPlot(i+j*1j)
                
                explored_points = explored_points.union(pts)
                plots_list.append(CropPlot(pts, w+h*1j, c))
    

    return plots_list

class CropPlot():
    
    def __init__(self, points, bounds, c):
        self.points = points
        self.area = len(points)
        self.bounds = bounds
        self.id = c
    
    def perimiter(self):
        perimiter = 0
        
        w = int(self.bounds.imag)
        h = int(self.bounds.real)
        inside = [False] * h

        for i in range(w):
            p = i
            
            for j in range(h):
                p += 1j
                
                if (p in self.points) != inside[j]:
                    perimiter += 1
                    inside[j] = not inside[j]
           
        inside = [False] * w
        for i in range(h):
            p = i*1j
            
            for j in range(w):
                p += 1
                
                if (p in self.points) != inside[j]:
                    perimiter += 1
                    inside[j] = not inside[j]
                    

        return perimiter
    
    
    def price(self):
        return self.area * self.perimiter()
    
    def edgePrice(self):
        return self.area * self.edges()
    
    def __repr__(self):
        return str(self.points)
    
    
def part1(data):
    plots : list[CropPlot] =  data
    
    plot_price = 0
    
    for p in plots:
        plot_price += p.price()
    
    return plot_price


def part2(data):
    
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