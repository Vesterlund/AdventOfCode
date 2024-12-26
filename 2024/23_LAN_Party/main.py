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
    
    connections_dict = defaultdict(set)
    
    
    for r in data:
        c1,c2 = r.split("-")
        
        connections_dict[c1].add(c2)
        connections_dict[c2].add(c1)
    
    return data, connections_dict


    
def part1(data):
    return


def part2(data):
    
    connections, connections_dict = data
    
    
    handled_connections = set()
    clusters = []
    
    
    for con in connections:
        if con in handled_connections:
            continue
        
        c1,c2 = con.split("-")
        
        c1_set = connections_dict[c1].union({c1})
        c2_set = connections_dict[c2].union({c2})
        
        temp_cluster = c1_set & c2_set
        iter_cluster = temp_cluster.copy()
        

        for c in iter_cluster:
            temp_cluster = temp_cluster & connections_dict[c].union({c})
        
        
        for a in temp_cluster:
            for b in temp_cluster:
                handled_connections.add(f"{a}-{b}")
        
        
        clusters.append(temp_cluster)

        
    res = ",".join(sorted(clusters[np.argmax([len(c) for c in clusters])]))  
    
    
    return res

    

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