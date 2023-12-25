import sys, getopt
import numpy as np
import math
import re
from enum import Enum
import copy
np.set_printoptions(threshold=sys.maxsize, linewidth=sys.maxsize)

def readFile(filepath:str):
    f = open(filepath)

    fileContent = f.read()
    f.close()

    return fileContent

def parseInput(filePath:str):
    fileContent = readFile(filePath)

    wiresDict = {}

    data = fileContent.split("\n")
    
    for d in data:
        wires = re.findall(r"\w+", d)
        
        fromWire, toWires = wires[0], wires[1:]
        
        wiresDict[fromWire] = set(toWires)
    
    temp = copy.deepcopy(wiresDict)
    
    for k in temp:
        for e in temp[k]:
            
            if e not in wiresDict:
                wiresDict[e] = {k}
            else:
                wiresDict[e].add(k)
    
    return wiresDict

import queue

def findNodesInGroup(startNode, wires):
    
    q = queue.Queue()
    visited = set()
    
    q.put(startNode)
    
    while not q.empty():
        n = q.get()
        
        if n not in visited:
            visited.add(n)
            
            for e in wires[n]:
                if e not in visited:
                    q.put(e)
    

    return visited
    
def generateGraph(wires):    
    import graphviz
    
    dot = graphviz.Graph('connections')
    dot.engine = "neato"
    for k in wires:
        dot.node(k)
        for e in wires[k]:
            dot.edge(k, e)

    dot.render(view=True,)  
    
def part1(data):
    
    # generateGraph(data)  
    
    # Cut between
    # nct : _kdk_
    # _cvx_ : tvj
    # _spx_ : fsv
    wiresDict = data
    
    wiresDict["kdk"].remove("nct")
    wiresDict["cvx"].remove("tvj")
    wiresDict["spx"].remove("fsv")
    
    wiresDict["nct"].remove("kdk")
    wiresDict["tvj"].remove("cvx")
    wiresDict["fsv"].remove("spx")
    
    n1 = findNodesInGroup("nct", wiresDict)
    n2 = findNodesInGroup("kdk", wiresDict)


    return len(n1)*len(n2)


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
            result = part1(copy.deepcopy(data))
            print("{} - Part 1: size1 * size2 = {} ".format(file, result))
        
        if not noPartTwo:
            result = part2(copy.deepcopy(data))
            print("{} - Part 2: {} Sum of starting position coordinates ".format(file, result))

if __name__ == "__main__":
    main(sys.argv[1:])