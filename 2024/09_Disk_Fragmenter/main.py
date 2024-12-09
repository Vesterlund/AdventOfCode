import sys, getopt
import numpy as np
import math
import re
from enum import Enum
import copy
import queue
from collections import defaultdict
np.set_printoptions(threshold=sys.maxsize, linewidth=sys.maxsize)

def readFile(filepath:str):
    f = open(filepath)

    fileContent = f.read()
    f.close()

    return fileContent

def parseInput(filePath:str):
    fileContent = readFile(filePath)
    
    return fileContent


class File:  
    def __init__(self, value, end=False):
        self.end = end
        self.value=value
    
    def isLast(self):
        return self.end
    
    def __str__(self):
        return str(self.value) + ("T" if self.end else "")
    
    def __repr__(self):
        return str(self)
   
def part1(data):
    disk = data
    
    file_data = disk[::2]
    empty_space = list(disk[1::2])
    
    
    file_list = []
    
    for i, f in enumerate(file_data):
        file_list += [File(i) for _ in range(int(f)-1)] + [File(i, end=True)]

    b_is_in_empty_space = False

    pos = 0
    chksum = 0
    while file_list:
        if not b_is_in_empty_space:
            f:File = file_list.pop(0)
            
            chksum += pos * f.value
            pos += 1
            while not f.isLast() and file_list:
                f:File = file_list.pop(0)
                chksum += pos * f.value
                pos += 1
           
            b_is_in_empty_space = True
            
            continue
        
        e_counter = int(empty_space.pop(0))
        
        while e_counter > 0:
            f:File = file_list.pop(-1)
            chksum += f.value * pos
            pos += 1
            e_counter -= 1
            
        
        b_is_in_empty_space = False
    
    return chksum


 
class Filev2:  
    def __init__(self, value, size):
        self.value=value
        self.size = size
        self.touched = False
    
    def isEmpty(self):
        return (self.value < 0)
    
    def __str__(self):
        return f"{self.value}"*self.size if self.value >= 0 else f"."*self.size
    
    def __repr__(self):
        return str(self)


def part2(data):
    disk = data
    

    file_list = []
    b_empty=False
    i = 0
    for f in disk:
        if b_empty:
            b_empty=False
            file_list.append(Filev2(-1, int(f)))
            continue
        file_list.append(Filev2(i, int(f)))
        b_empty=True
        i+=1
    
    end_ptr = len(file_list)-1
    
    while end_ptr >= 0:
        end_file:Filev2 = file_list[end_ptr]
        
        if end_file.isEmpty():
            end_ptr -= 1
            continue
        
        
        for j in range(end_ptr):
            f:Filev2 = file_list[j]
            
            if f.isEmpty() and f.size >= end_file.size:
                f.size -= end_file.size
                
                new_file = Filev2(end_file.value, end_file.size)
                end_file.value = -1
                
                file_list = file_list[:j] + [new_file] + file_list[j:]
                
                end_ptr += 1
                
                break
        
        end_ptr -= 1
    

    chksum = 0  
    pos = 0
    for f in file_list:
        
        if f.isEmpty():
            pos += f.size
            continue
        
        chksum += f.value * sum(range(pos, pos+f.size))
        pos += f.size

    return chksum

    

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