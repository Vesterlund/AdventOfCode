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

import networkx as nx

def parseInput(filePath:str):
    fileContent = readFile(filePath)
    data = fileContent.split("\n")
    
    
    walls = set()
    start_pos = 0
    end_pos = 0
    
    
    for i, row in enumerate(data):
        for j, c in enumerate(row):
            p = i+j*1j
            
            if c=="#":
                walls.add(p)
                continue
            
            
            if c=="S":
                start_pos = p
                continue
            if c =="E":
                end_pos = p

            
    def makeGraph(graph):
        R = len(graph)
        C = len(graph[0])
        G = nx.DiGraph()
        for r in range(R):
            nx.add_path(G, [(r, c, 0) for c in range(C)], weight=1)
            nx.add_path(G, [(r, c, 2) for c in range(C - 1, -1, -1)], weight=1)
        for c in range(C):
            nx.add_path(G, [(r, c, 1) for r in range(R)], weight=1)
            nx.add_path(G, [(r, c, 3) for r in range(R - 1, -1, -1)], weight=1)
            
        for r in range(R):
            for c in range(C):
                if graph[r][c] in ".ES":
                    nx.add_cycle(G, [(r, c, x) for x in range(4)], weight=1000)
                    nx.add_cycle(G, [(r, c, x) for x in range(3, -1, -1)], weight=1000)
                if graph[r][c] == "#":
                    G.remove_nodes_from([(r, c, x) for x in range(4)])
                if graph[r][c] == "S":
                    start = r, c, 0
                if graph[r][c] == "E":
                    end = r, c
                    for x in range(4):
                        G.add_edge((r, c, x), (r, c), weight=0)
        return G, start, end

    
    
    return walls, start_pos, end_pos, (len(data), len(data[0])), makeGraph(data)


    
def part1(data):
    walls, start_pos, end_pos, shape,_ = data
    
    def printgraph(reached=set()):
        
        for i in range(shape[0]):
            r = ""
            for j in range(shape[1]):
                p = i+j*1j
                
                if p not in walls:
                    if p == start_pos:
                        r+= "S"
                    elif p == end_pos:
                        r+= "E"
                    elif p in reached:
                        r+="x"
                    else:
                        r+="."
                    continue
    
                if p in walls:
                    r+= "#"
                    continue
                
                r+="?"

            print(r)
    
    #(priority, (poslist, dir))
    pq = queue.PriorityQueue()
    
    reached = set()
    
    score = 0
    
    if not start_pos + -1 in walls:
        pq.put((1000,1, ([start_pos], -1)))
    
    if not start_pos + 1j in walls:
        pq.put((0,2, ([start_pos], 1j)))
    
    if not start_pos + 1 in walls:
        pq.put((1000,2, ([start_pos], 1)))
    
    
    extra_order = 3
    
    while not pq.empty():
        
        #printgraph(reached)
        
        item = pq.get()
        
        cost,_, path = item
        pathlist, direction = path
        
        c_node = pathlist[-1]
        
        if c_node in reached:
            continue
        
        reached.add(c_node)
        
        if c_node == end_pos:
            score = cost
            break
        
        
        #print(score, cost)
        
        n_fw = c_node + direction
        n_r = c_node + direction*(-1j)
        n_l = c_node + direction*(1j)
        
        if not n_fw in walls:            
            pq.put((cost + 1, extra_order, (pathlist + [n_fw], direction)))
            extra_order += 1
        
        if not n_r in walls:
            pq.put((cost + 1000+ 1, extra_order, (pathlist+[n_r], direction*(-1j))))
            extra_order += 1
            
        if not n_l in walls:
            pq.put((cost + 1000+ 1, extra_order, (pathlist+[n_l], direction*1j)))
            extra_order += 1

    #print(reached)

    return score


def part2(data):
    walls, start_pos, end_pos, shape, graph = data
    from colorama import Fore, Back, Style
    
    def printgraph(pset=set()):
        for i in range(shape[0]):
            r = ""
            for j in range(shape[1]):
                p = i+j*1j
                
                if p not in walls:
                    if p == start_pos:
                        r+= "S"
                    elif p == end_pos:
                        r+= "E"
                    elif p in pset:
                        r+= Fore.GREEN + "x" + Fore.WHITE
                    else:
                        r+="."
                    continue
    
                if p in walls:
                    r+= "#"
                    continue
                
                r+="?"

            print(r)
    def printgraphCol(l=[]):
        
        pset, col = l
        
        for i in range(shape[0]):
            r = ""
            for j in range(shape[1]):
                p = i+j*1j
                
                if p not in walls:
                    if p == start_pos:
                        r+= "S"
                    elif p == end_pos:
                        r+= "E"
                    elif p in pset:
                        r+= col[p] + "x" + Fore.WHITE
                    else:
                        r+="."
                    continue
    
                if p in walls:
                    r+= "#"
                    continue
                
                r+="?"

            print(r)
    
    
        
    graph,s,e = graph
    
    paths = nx.all_shortest_paths(graph, s,e,weight="weight")
    
    seats = set()
    
    for path in paths:
        for point in path:
            p = point[0] + point[1]*1j
            seats.add(p)
    
    
    return len(seats)
    
    
    
    
    printgraphCol((reached_set, set_col))
    # High:
    # 625
    # 624
    # 571
    
    # 461 Wrong
    return  len(reached_set)

    

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