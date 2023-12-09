import sys, getopt
import numpy as np
import math

def readFile(filepath:str):
    f = open(filepath)

    fileContent = f.read()
    f.close()

    return fileContent

def parseInput(filePath:str):

    fileContent = readFile(filePath).split("\n")

    numberSequence = []

    for row in fileContent:
        numberSequence.append(list(map(int,row.split(" "))))

    return numberSequence


def traverse(sequence):
    levels = [sequence]

    while not all(i == 0 for i in levels[-1]):
        levels.append([y-x for x,y in zip(levels[-1][:-1],levels[-1][1:])])
    
    
    return levels

def construct(levels, reverse):
    i = len(levels)-1

    zeroPos = -1 if not reverse else 0

    d = levels[i][zeroPos]
    p = levels[i-1][zeroPos]
    n = p + d if not reverse else p - d

    i -= 1
    while i > 0:
        d = n
        p = levels[i-1][zeroPos]

        n = p + d if not reverse else p - d
        i -= 1

    return n

    

def part1(data):

    histSum = 0

    for sequence in data:
        levels = traverse(sequence)
        histSum += construct(levels, False)

    return histSum

def part2(data):
    histSum = 0

    for sequence in data:
        levels = traverse(sequence)
        histSum += construct(levels, True)

    return histSum


def main(argv):
    noPartOne = False
    noPartTwo = False
    onlyExample = False
    debugMode = False

    opts, args = getopt.getopt(argv,"od",["no-part-1","no-part-2", "only-example"])
    for opt, arg in opts:
        if opt in ("-o", "--only-example"):
            onlyExample = True
        elif opt == "--no-part-1":
            noPartOne = True
        elif opt == "--no-part-2":
            noPartTwo = True
        elif opt == "-d":
            debugMode = True
    
    exampleFiles = ["example.txt"]
    problemFiles = ["input.txt"]

    problemFiles = problemFiles + exampleFiles if not onlyExample else exampleFiles

    for file in problemFiles:
        data = parseInput(file)

        if not noPartOne:
            result = part1(data)
            print("{} - Part 1: Sum of extrapolated values {}".format(file, result))
        
        if not noPartTwo:
            result = part2(data)
            print("{} - Part 2: Sum of extrapolated values {}".format(file, result))






if __name__ == "__main__":
    main(sys.argv[1:])