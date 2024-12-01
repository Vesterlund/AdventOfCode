import sys, getopt
import numpy as np
import math

def readFile(filepath:str):
    f = open(filepath)

    fileContent = f.read()
    f.close()

    return fileContent

def parseInput(filePath:str):
    fileContent = readFile(filePath)


    data = fileContent.split("\n")
    
    costMap = np.zeros((len(data), len(data[0])))

    for i, row in enumerate(data):
        for j, char in enumerate(row):
            costMap[i,j] = int(char)

    return costMap

from functools import total_ordering
UP, DOWN, RIGHT, LEFT = (-1 + 0j), (1 + 0j),  (0 + 1j), (0 + -1j)

@total_ordering
class Node:
    def __init__(self, pos = 1+1j, direction = RIGHT, costTohere=0, prevNode = None, straightSteps = 0) -> None:
        self.pos = pos
        self.direction = direction
        self.costTohere = costTohere
        self.prevNode = prevNode
        self.straightSteps = straightSteps
    
    def getPos(self):
        return int(self.pos.real), int(self.pos.imag)

    def isEqual(self, __value):
        return self.pos == __value.pos

    def data(self):

        return self.pos, self.straightSteps, self.costTohere, self.direction

    def step(self, costMap, rotation=1):
        nextPos = self.pos + self.direction*rotation
        nextDir = self.direction*rotation
        nextCost = self.costTohere + costMap[int(nextPos.real), int(nextPos.imag)]
        nextStraight = self.straightSteps + 1 if rotation == 1 else 0
        nextPrev = self

        return Node(nextPos,nextDir, nextCost, nextPrev, nextStraight)


    def __str__(self) -> str:
        return "({} cost: {})".format(self.pos, self.costTohere)

    def __hash__(self) -> int:
        return hash(self.pos, self.straightSteps, self.direction)

    def __eq__(self, __value) -> bool:
        return self.costTohere == __value.costTohere
    def __lt__(self, __value) -> bool:
        return self.costTohere < __value.costTohere 

import queue
from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class PQItem:
    cost: int
    data: Any=field(compare=False)

def directionToInt(dir : complex):
   if dir == UP: return 0
   if dir == RIGHT: return 1
   if dir == DOWN: return 2
   return 3

def doNodeDjikstra(minstep, maxstep, costMatrix):

    endNode = Node(pos=complex(len(costMatrix)-1, len(costMatrix[0]) - 1))

    pq = queue.PriorityQueue()
    pq.put(Node(direction=RIGHT))
    pq.put(Node(direction=DOWN))


    distances = np.ones((len(costMatrix), len(costMatrix[0]),4, 4)) * -1

    def isBestFound(pos, steps, dir, cost):
        cReal = int(pos.real)
        cImag = int(pos.imag)
        currBest = distances[cReal,cImag,directionToInt(dir), steps-1]

        if cost < currBest or currBest == -1:
            distances[cReal,cImag,directionToInt(dir), steps-1] = cost
            return True
        return False

    while pq:
        curr = pq.get()
        pos, steps, cost, dir = curr.data()

        if curr.isEqual(endNode) and steps >= minstep:
            return cost

        if steps >= minstep:
            for newDir in (dir*1j, dir*-1j):
                newPos = pos + newDir
                if nextCost :=  costMatrix[int(newPos.real), int(newPos.imag)]:
                    if isBestFound(newPos, 1, newDir, cost + nextCost):
                        pq.put(Node(newPos, newDir, cost + nextCost,None, 1))
        
        if steps < maxstep:
            newPos = pos + dir
            if nextCost := costMatrix[int(newPos.real), int(newPos.imag)]:
                if isBestFound(newPos, steps + 1, dir, cost + nextCost):
                    pq.put(Node(newPos, dir, cost + nextCost, None, steps + 1))

    return
    
def doDjikstra(minStep, maxStep, costMatrix):
    pq = queue.PriorityQueue()
    pq.put(PQItem(0, (complex(0,0),0,RIGHT)))
    pq.put(PQItem(0, (complex(0,0),0,DOWN)))

    # Save visited
    tiles = {complex(row, column): val for row, line in enumerate(costMatrix) for column, val in enumerate(line)}
    distances = {key: [[-1] * maxStep, [-1] * maxStep, [-1] * maxStep, [-1] * maxStep] for key in tiles.keys()}
    
    # Check if best
    def isBestFound(pos, steps, dir, cost):
        currBest = distances[pos][directionToInt(dir)][steps-1]
        if cost < currBest or currBest == -1:
            distances[pos][directionToInt(dir)][steps-1] = cost
            return True
        return False

    endPos = complex(len(costMatrix)-1, len(costMatrix[0]) - 1)

    while pq:
        curr = pq.get()
        cost, data = curr.cost, curr.data
        pos, steps, dir = data

        #print(curr)

        if pos == endPos and steps >= minStep:
            return cost
        
        if steps >= minStep:
            for newDir in (dir*1j, dir*-1j):
                if nextCost := tiles.get(pos + newDir):
                    if isBestFound(pos + newDir, 1, newDir, cost + nextCost):
                        pq.put(PQItem(cost + nextCost, (pos + newDir, 1, newDir)))

        if steps < maxStep:
            if nextCost := tiles.get(pos + dir):
                if isBestFound(pos + dir, steps+1, dir, cost + nextCost):
                    pq.put(PQItem(cost+nextCost, (pos+dir, steps + 1, dir)))
        

    return

def get_best_heat(min_step, max_step,costMatrix):
    dijkstra_imposter = queue.PriorityQueue()
    dijkstra_imposter.put(PQItem(0, (complex(0, 0), 0, DOWN))) #position, number of straight steps, direction
    dijkstra_imposter.put(PQItem(0, (complex(0, 0), 0, RIGHT)))
    
    tiles = {complex(row, column): val for row, line in enumerate(costMatrix) for column, val in enumerate(line)}
    
    bests_heats = {key: [[-1] * max_step, [-1] * max_step, [-1] * max_step, [-1] * max_step] for key in tiles.keys()}

    def is_best_heat(steps, position, cost, direction):
        cur_best = bests_heats[position][directionToInt(direction)][steps - 1]
        if cost < cur_best or cur_best == -1:
            bests_heats[position][directionToInt(direction)][steps - 1] = cost
            return True

        return False
    endPos = complex(len(costMatrix)-1, len(costMatrix[0]) - 1)

    while dijkstra_imposter:
        
        item = dijkstra_imposter.get()
        cost, data = item.cost, item.data
        position, steps, direction = data

        if position == endPos and steps >= min_step:
            return cost

        if steps >= min_step:
            for new_dir in (direction * 1j, direction * -1j):
                if next_cost := tiles.get(position + new_dir):
                    if is_best_heat(1, position + new_dir, cost + next_cost, new_dir):
                        dijkstra_imposter.put(PQItem(cost + next_cost, (position +new_dir, 1, new_dir)))

        if steps < max_step:
            if next_cost := tiles.get(position + direction):
                if is_best_heat(steps + 1, position + direction, cost + next_cost, direction):
                    dijkstra_imposter.put(PQItem(cost + next_cost, (position + direction, steps + 1, direction)))


def part1(data):
    return doNodeDjikstra(1,3,data)


def part2(data):
    return doDjikstra(4,10,data)
    


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
            result = part1(data)
            print("{} - Part 1: Least heat loss {}".format(file, result))
        
        if not noPartTwo:
            result = part2(data)
            print("{} - Part 2: Least heat loss {}".format(file, result))

if __name__ == "__main__":
    main(sys.argv[1:])