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


    springInfo = []

    for row in fileContent:
        info = row.split(" ")
        springInfo.append((info[0] , list(map(int, info[1].split(","))) ))
        

    return springInfo

def recursivePlaceSpring(string, springSizeList, level = 0):

    springCombinations = []

    stringLength = len(string)
    springSum = sum(springSizeList)

    iChar = 0

    while iChar < stringLength :
        tempString = string
        c = tempString[iChar]
        #print(tempString)
        if c == ".":
            iChar += 1
            continue
        

        nextSpring = springSizeList[0]
        nextSpringIndex = canPlaceSpring(tempString, nextSpring, iChar)

        if nextSpringIndex == -1:
            iChar += 1
            continue
        
        tempString = placeSpring(tempString, nextSpring, nextSpringIndex)

        if springSizeList[1:]:
            splitIndex = nextSpringIndex + nextSpring + 1

            affix = tempString[:splitIndex]

            suffixes = recursivePlaceSpring(tempString[splitIndex:], springSizeList[1:], level=level+1)
            
            #if level==0: print(iChar,affix,tempString[splitIndex:],suffixes,  springSizeList[1:])
            #if level==1: print("  ",iChar,affix,tempString[splitIndex:],suffixes,  springSizeList[1:])
            
            for suffix in suffixes:
                if (affix + suffix).count("#") <= springSum:
                    springCombinations.append(affix + suffix)

        else:
            if tempString.count("#") <= springSum:
                springCombinations.append(tempString)

        iChar += 1
    
    return springCombinations

def placeSpring(springStr, springSize, index):
    return springStr[0:index] + "#"*springSize + "." + springStr[index+springSize+1:]

def canPlaceSpring(springStr, springSize, offset):
    if len(springStr) < springSize:
        return -1
    # Find first ? or #
    # Check that all chars in the range of springSize is either ? or #
    # Check that the char after springSize is ? or .
    # Return true/false and index/-1 of where it can be placed
     
    #print("s:",springStr, springSize)
    
    iOff = offset
    c = springStr[iOff]
    #print(i, iOff, c)
    if c in ["?", "#"]:
        springSubset = springStr[iOff:iOff+springSize]
        if "." in springSubset:
            return -1
        
        afterChar = springStr[iOff+springSize]
        beforeChar = springStr[iOff - 1]
        #print(beforeChar, springSubset, afterChar)
        if afterChar in ["?", "."] and beforeChar != "#":
            return iOff
            
    return -1


def part1(data):
    
    numComb = 0
    
    for s in data:
        
        paddedString = "."+s[0]+"."
        #springCombinations = combinationCounter(paddedString, s[1])
        #print("====",paddedString, s[1])
        comb = recursivePlaceSpring(paddedString, tuple(s[1]))

        numComb += len(comb)
        
    return numComb

def part2(data):
    return
    


def main(argv):
    noPartOne = False
    noPartTwo = False
    onlyExample = False

    opts, args = getopt.getopt(argv,"od",["no-part-1","no-part-2", "only-example"])
    for opt, arg in opts:
        if opt in ("-o", "--only-example"):
            onlyExample = True
        elif opt == "--no-part-1":
            noPartOne = True
        elif opt == "--no-part-2":
            noPartTwo = True
    
    exampleFiles = ["example.txt"]
    problemFiles = ["input.txt"]

    problemFiles = exampleFiles + problemFiles if not onlyExample else exampleFiles

    for file in problemFiles:
        data = parseInput(file)

        if not noPartOne:
            result = part1(data)
            print("{} - Part 1: {} combinations that meet the criteria".format(file, result))
        
        if not noPartTwo:
            result = part2(data)
            print("{} - Part 2: {} combinations that meet the criteria".format(file, result))

if __name__ == "__main__":
    main(sys.argv[1:])