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
    
    return data

numpad = {
    0: 7,
    1j: 8,
    2j: 9,
    1:4,
    1+1j:5,
    1+2j:6,
    2: 1,
    2+1j: 2,
    2+2j: 3,
    3+1j: 0,
    3+2j: "A"
}

keypadmap = {
    "7":  0,
    "8": 1j,
    "9": 2j,
    "4":1,
    "5": 1+1j,
    "6":1+2j,
    "1": 2,
    "2": 2+1j,
    "3": 2+2j,
    "0": 3+1j,
    "A": 3+2j
}

dirpad = {
    1j: "^",
    2j: "A",
    1: "<",
    1+1j: "v",
    1+2j: ">"
}

dirmap = {
    "^": -1 ,
    "v": 1,
    "<":-1j,
    ">":1j
}

buttonmap = {
    "^": 1j,
    "A": 2j,
    "<": 1,
    "v": 1+1j,
    ">": 1+2j
}

@cache
def moveKeypad(start_id, end_id):
    p_start = keypadmap[start_id]
    p_end = keypadmap[end_id]

    path = p_end - p_start
    
    r = int(path.real)
    i = int(path.imag)
    
    h_part = "<" * (-i) if i < 0 else ">"*i
    v_part = "^"*(-r) if r <0 else "v"*r
    
    # Om vi kan gå vänster först gör det
    
    if r < 0 and i < 0 and (int(p_end.imag) > 0  or (int(p_end.real) < 3 and int(p_start.real) < 3)):
        return h_part+v_part
    
    # Om vi kan gå nedåt först gör det
    # om r > 0
    if r > 0 and ((int(p_end.imag) > 0 and int(p_start.imag) > 0) or (int(p_end.real) < 3 and int(p_start.real) < 3)):
        return v_part+h_part
    
    final_path = h_part + v_part if r > 0 else v_part+ h_part
    
    return final_path
    
@cache
def moveDirpad(start_id, end_id):
    p_start = buttonmap[start_id]
    p_end = buttonmap[end_id]

    path = p_end - p_start
    
    r = int(path.real)
    i = int(path.imag)
    
    h_part = "<" * (-i) if i < 0 else ">"*i
    v_part = "^"*(-r) if r <0 else "v"*r
    
    final_path = h_part + v_part if r < 0 else v_part+ h_part
    
    return final_path


def codePath(code):
    
    path = ""
    
    for i in range(len(code)-1):
        c_pos = code[i]
        n_pos = code[i+1]
        path += moveKeypad(c_pos, n_pos) + "A"
        

    return path

def dirPath(directions):
    path = ""
    
    for i in range(len(directions)-1):
        c_pos = directions[i]
        n_pos = directions[i+1]
        
        #print(c_pos, n_pos, moveDirpad(c_pos, n_pos), "A")
        path += moveDirpad(c_pos, n_pos) + "A"
    

    return path

def decodeDir(dirpath):
    p = 2j
    
    out =""
    for d in dirpath:
       
        if d != "A":
            p += dirmap[d]
            continue
        
        out += dirpad[p]
    
    return out            

def part1(data):
    codes = data
    
    # ====
    keypad_robots = 2 
    # ====

    total_complexity = 0
    for code in codes:
        seq = codePath("A" + code)
        
        for _ in range(keypad_robots):
            seq = dirPath("A" + seq)
        
        comp = len(seq)*int(code[:-1])

        #print(len(seq), int(code[:-1]), comp)

       
        total_complexity += comp

    return total_complexity


def part2(data):
    codes = data
    
    # ====
    keypad_robots = 25
    # ====
    numpad_map = defaultdict(lambda: defaultdict(list))
    dirpad_map = defaultdict(lambda: defaultdict(list))

    def numpadPaths(start,end):
        p_start = keypadmap[start]
        p_end = keypadmap[end]

        path = p_end - p_start
        
        r = int(path.real)
        i = int(path.imag)
        
        h_part = "<" * (-i) if i < 0 else ">"*i
        v_part = "^"*(-r) if r <0 else "v"*r

        
        # Om vi kan gå vertikalt först (upp ja, nej beror på)
        if r < 0 or ((int(p_end.imag) > 0 and int(p_start.imag) > 0) or (int(p_end.real) < 3 and int(p_start.real) < 3)):
            if r:
                numpad_map[start][end].append(v_part + h_part)
        
        # Om vi kan gå horisontellt först (höger ja, vänster beror på)
        if  i > 0 or ((int(p_end.imag) > 0 and int(p_start.imag) > 0) or (int(p_end.real) < 3 and int(p_start.real) < 3)):
            if i :
                numpad_map[start][end].append(h_part + v_part)
      
      
    p = "0123456789A"
    
    for s in p:
        for e in p:
            numpadPaths(s,e) 

    def dirpadPaths(s,e):
        p_start = buttonmap[s]
        p_end = buttonmap[e]

        path = p_end - p_start
        
        r = int(path.real)
        i = int(path.imag)
        
        h_part = "<" * (-i) if i < 0 else ">"*i
        v_part = "^"*(-r) if r <0 else "v"*r
        
        b_insquare = int(p_end.imag) > 0 and int(p_start.imag) > 0
        
        if i>= 0 or b_insquare:
            if r:
                dirpad_map[s][e].append(h_part + v_part)
    
        if r >= 0 or b_insquare:
            if i:
                dirpad_map[s][e].append(v_part + h_part)

        if not path:
            dirpad_map[s][e].append("")

    p = "<^v>A"
    
    for s in p:
        for e in p:
            dirpadPaths(s,e)
    

    def buildSeq(keys,index,prevKey,currPath,res):
        if index == len(keys):
            res.append(currPath)
            return
        for path in dirpad_map[prevKey][keys[index]]:
            buildSeq(keys, index+1, keys[index], currPath + path + "A", res)

    @cache
    def shortestSeq(keys,depth):
        if not depth:
            return len(keys)
        
        sub_keys = [e + "A" if e else "A" for e in keys.split("A") ]
        sub_keys = sub_keys[:-1]
        total_seq_length = 0
        
        for sk in sub_keys:
            seq_ins = []
            buildSeq(sk, 0, "A", "", seq_ins)

            l = []
            for s in seq_ins:
                length = shortestSeq(s, depth-1)

                l.append(length)
            
            total_seq_length += min(l)
        
        return total_seq_length 
    
    def buildNumSeq(keys,index,prevKey,currPath,res):
        
        if index == len(keys):
            res.append(currPath)
            return

        for path in numpad_map[prevKey][keys[index]]:
            buildNumSeq(keys, index+1, keys[index], currPath + path + "A", res)
    
    def solve(code, maxDepth):
        
        seq = []
        buildNumSeq(code,0,"A","", seq)
        
        score = []
        
        for s in seq:
            score.append(shortestSeq(s, maxDepth))
        
        return min(score)
    
    total_complexity = 0
    
    for code in codes:
        total_complexity += int(code[:-1]) * solve(code, keypad_robots)
    
    
    # Low:
    # 448592681972
    
    return total_complexity

    

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