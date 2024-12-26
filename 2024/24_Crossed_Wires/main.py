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
    registers, operations = fileContent.split("\n\n")
    
    registers = registers.split("\n")
    
    registers = [r.split(": ") for r in registers]
    registers = {r:int(v) for r,v in registers}
    
    
    operations = operations.split("\n")

    op_list = []

    for o in operations:
        op, out = o.split("-> ")
        
        temp = op.split(" ")
        
        op_list.append((temp[1], temp[0],temp[2], out))
    
    return registers, op_list


def doOp(op, v1, v2):
    
    match op:
        case "AND":
            return v1 and v2
        case "OR":
            return v1 or v2
        case "XOR":
            return v1 ^ v2

    
def part1(data):
    
    registers, op_list = data
    
    op_iter : list = op_list.copy()
    
    ptr = 0
    
    z_list = []
    
    while op_iter:
        instr = op_iter[ptr]
        
        op, v1, v2, res = instr
        
        if v1 not in registers or v2 not in registers: 
            ptr += 1
            ptr = ptr % len(op_iter)
            continue
        
        v1,v2 = registers[v1], registers[v2]
        
        registers[res] = doOp(op,v1,v2)
        
        if res[0] == "z":
            z_list.append(res)
        
        op_iter.pop(ptr)
        if op_iter:
            ptr = ptr % len(op_iter)
        
        
    binary_string = "" 
    for z in sorted(z_list,reverse=True):
        binary_string += str(registers[z])
        

    return int(binary_string,2)


def part2(data):
    
    registers, op_list = data
    
    from enum import Enum
    
    class OpColor(Enum):
        AND = "green"
        OR = "red"
        XOR = "yellow"
    
    
    import graphviz
    whole = graphviz.Digraph()

    for ins in op_list:
        op, x1,x2, y = ins
        
        with whole.subgraph(name="xy") as xy:
            xy.node_attr['style'] = "filled"
            xy.attr(rank='same')
            if x1[0] in "xy":
                xy.node(x1,x1)
            else:
                whole.node(x1,x1)
            
            if x2[0] in "xy":
                xy.node(x2,x2)
            else:
                whole.node(x2,x2)
        
        if y[0]=="z":
            with whole.subgraph(name="z") as z:
                c = OpColor[op]
                z.node_attr['style'] = "filled"
                z.attr(rank='same')
                z.node(y,y, color=c.value)
        else:
        
            with whole.subgraph(name="ops") as ops:
                c = OpColor[op]
                xy.node_attr['style'] = ""
                ops.node(y,y, color=c.value)
        
        whole.edge(x1,y)
        whole.edge(x2,y) 
    
    whole.subgraph(xy)
    
    whole.render('test.gv', view=True)
   
    # Loopa tills alla instruktioner är förburkade
    # Om inte kan beräkna skippa
    
    op_iter : list = op_list.copy()
    
    ptr = 0
    
    z_list = []
    
    while op_iter:
        instr = op_iter[ptr]
        
        op, v1, v2, res = instr
        
        if v1 not in registers or v2 not in registers: 
            ptr += 1
            ptr = ptr % len(op_iter)
            continue
        
        v1,v2 = registers[v1], registers[v2]
        
        registers[res] = doOp(op,v1,v2)
        
        if res[0] == "z":
            z_list.append(res)
        
        op_iter.pop(ptr)
        if op_iter:
            ptr = ptr % len(op_iter)
        
        
    binary_string = "" 
    for z in sorted(z_list,reverse=True):
        binary_string += str(registers[z])
        
    
    x_list = []
    y_list = []
    
    for k in registers:
        if k[0] == "x":
            x_list.append(k)
        if k[0] == "y":
            y_list.append(k)

    x_string = "" 
    for x in sorted(x_list,reverse=True):
        x_string += str(registers[x])  
    
    y_string = "" 
    for y in sorted(y_list,reverse=True):
        y_string += str(registers[y])   
        
        
    out = int(x_string,2) + int(y_string,2)
    print(bin(out))
    print("0b"+ binary_string)
    
     
    # hdt <=> z05
    # gbf <=> z09
    # mht <=> jgt
    # nbf <=> z30
    
    swaps = ["hdt","gbf","mht","nbf","z05","z09","jgt","z30"]
    
    return ",".join(sorted(swaps))
    
    
    
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