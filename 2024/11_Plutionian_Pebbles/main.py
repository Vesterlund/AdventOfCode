import sys, getopt
import numpy as np
import math
import re
from enum import Enum
import copy
import queue
from collections import defaultdict
import time

np.set_printoptions(threshold=sys.maxsize, linewidth=sys.maxsize)

def readFile(filepath:str):
    f = open(filepath)

    fileContent = f.read()
    f.close()

    return fileContent

def parseInput(filePath:str):
    fileContent = readFile(filePath)
    
    return list(map(int,fileContent.split(" ")))


    
def part1(data):
    stones = data
    
    def blink(stone, n_blinks):
         
        if not n_blinks:
            return [stone]
        
        new_stone = [2024*stone]
        s_stone = str(stone)
        l_stone = len(s_stone)
        
        if stone == 0:
            new_stone = [1]
        elif l_stone % 2 == 0:
            
            new_stone = [int(s_stone[:int(l_stone/2)]), int(s_stone[int(l_stone/2):])]

        res_stones = []

        for s in new_stone:
            r  = blink(s, n_blinks-1)

            res_stones += r
            
        return res_stones
        
    stone_length = 0
 
    for s in stones:
        r = blink(s, 25)
        stone_length += len(r)
    
    return stone_length


from functools import cache

def part2(data):
    stones = data
    
    sd = {}
    
    @cache
    def blink(stone, n_times):
        
        if stone in sd:
            l = sd[stone]["steps"]
            
            if l > n_times:
                return 1

            if l == n_times:
                return 2
            
            n = 0
            for s in sd[stone]["children"]:
                n += blink(s, n_times-l)
            
            return n
        
        steps = 1
        
        c_stone = stone
        while(len(str(c_stone)) % 2):
            new_stone = 2024*c_stone
            
            if c_stone == 0:
                new_stone = 1
            
            c_stone = new_stone
            
            steps += 1

        s_stone = str(c_stone)
        l_stone = len(s_stone)
        sd[stone] = {"steps": steps, "children": [int(s_stone[:int(l_stone/2)]), int(s_stone[int(l_stone/2):])]}

        if steps < n_times:
            n = 0

            for s in sd[stone]["children"]:
                
                t = blink(s, n_times-steps)
                n+= t
            
            return n

        if steps == n_times:
            return 2
        
    
        return 1
    
    stone_length = 0
    
    for s in stones:
        stone_length += blink(s, 75)

    return stone_length

    

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