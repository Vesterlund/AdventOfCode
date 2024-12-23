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
    data = fileContent.split("\n\n")
    
    registers, program = data
    
    registers = list(map(int, re.findall(r"\d+", registers)))
    program = list(map(int,re.findall(r"\d+", program)))
    
        
    return registers, program


def runProgram(registers, program):
    
    ptr = 0
    
    def combo(o):
        if o in {0,1,2,3}:
            return o

        if o == 4:
            return registers[0]
        if o == 5:
            return registers[1]
        if o == 6:
            return registers[2]
        
        if o == 7:
            raise ValueError("Invalid operand")
    
    output = []
    
    while ptr < len(program):
        opcode, operand = program[ptr], program[ptr+1]
        
        ptr += 2
        
        match opcode:
            case 0:
                registers[0] = int(registers[0] / (2**combo(operand)))
                
            case 1:
                registers[1] = registers[1] ^ operand
            
            case 2:
                registers[1] = combo(operand) % 8
                
            case 3:
                if registers[0] == 0:
                    continue
                
                ptr = operand  
            
            case 4:
                registers[1] = registers[1] ^ registers[2]
            
            case 5:
                output.append(combo(operand) % 8)

            case 6:
                registers[1] = int(registers[0] / (2**combo(operand)))

            case 7:
                registers[2] = int(registers[0] / (2**combo(operand)))
    res = ",".join(list(map(str,output)))
    
    return res
    
def part1(data):
    registers, program = data
    
    return runProgram(registers, program)


def part2(data):
    registers, program = data
    
    l = len(program)

    pstring=",".join(list(map(str,program)))
    from colorama import Fore, Back, Style
    
    def trueStr(res):
        r = ""
        
        for i in range(len(res)):
            if res[i] == pstring[i] and res[i] != ",":
                r+= Fore.GREEN
            
            r+= res[i] + Fore.WHITE
            
        return r
    
    def checkProgram(res, n_ins):
        for i in range(1,2*n_ins + 1):
            if res[-i] == ",":
                continue
            if res[-i] != pstring[-i]:
                return False
            
        
        return True
    

    prev_digits = [(6,1), (6,5)]
    
    for _ in range(13):
        new_digits = []
        for pd  in prev_digits:
            
            start_a = sum([d *(8**(l-1-i)) for i,d in enumerate(pd)])
            
            e = l - 1 - len(pd)

            
            for i in range(8):
                for j in range(8):
                    A = start_a + i*8**e + j*8**(e-1)
                    res = runProgram([A, 0,0], program)
                    #print(trueStr(res), i,j)
                    
                    if checkProgram(res, len(pd)+1):
                        new_digits.append(tuple(list(pd) + [i]))
                        
                        if res == pstring:
                            return A

        prev_digits = list(set(new_digits.copy()))
    

    

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