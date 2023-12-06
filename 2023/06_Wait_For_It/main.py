from sympy import Eq, solve, floor, ceiling
from sympy.abc import x

def readFile(filepath:str):
    f = open(filepath)

    fileContent = f.read()
    f.close()

    return fileContent

def strArrToNum(arr):
    return list(map(int, arr))

def parseInput(fileContent):

    rows = fileContent.split("\n")
    times = rows[0].split(":")[1].strip().split(" ")
    times = strArrToNum(list(filter(None, times)))
    distances = rows[1].split(":")[1].strip().split(" ")
    distances = strArrToNum(list(filter(None, distances)))

    return times,distances

def solveEquation(time, dist):
    eq1 = Eq(0,x*(time-x) - dist)

    return solve(eq1)

def countSolutions(time, dist):
    solutions = solveEquation(time, dist)

    lowerbnd = ceiling(solutions[0])
    upperbnd = floor(solutions[1])

    numRecords = upperbnd - lowerbnd + 1

    if (lowerbnd*(time-lowerbnd) == dist):
        numRecords -= 1

    if (upperbnd*(time-upperbnd) == dist):
        numRecords -= 1
    
    return numRecords


def part1(filepath):
    times, distances = parseInput(readFile(filepath))
    
    recordsMult = 1

    for time, dist in zip(times, distances):
        recordsMult *= countSolutions(time, dist)
    
    print("{} - Part 1: Number of winning times {}".format(filepath, recordsMult))

def part2(filepath):
    times, distances = parseInput(readFile(filepath))
    
    time = int("".join([str(t) for t in times]))
    dist = int("".join([str(d) for d in distances]))

    recordsMult = countSolutions(time,dist)

    print("{} - Part 2: Number of winning times {}".format(filepath, recordsMult))



part1("example.txt")
part2("example.txt")

part1("input.txt")
part2("input.txt")