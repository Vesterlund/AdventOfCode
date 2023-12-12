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


def combinationCounter(springStr, springSizes):
    
    # Loop through the spring sizes trying to place them
    # Offset the starting ? (or # in some measure) by one after each loop
    # If some spring cannot be placed, the sequence is invalid
    
    springCombinations = []
    
    for i, c in enumerate(springStr):
        if c not in ["?"]:
            continue
        tempString = springStr[:i].replace("?",".") + springStr[i:]
        
        placedString = True
        lastPlacedIndex = 0
        
        for spring in springSizes:
            index = canPlaceSpring(tempString, spring, lastPlacedIndex)
            
            if index == -1: # If one spring cannot be placed, dont try the rest
                placedString = False
                break
            
            tempString = placeSpring(tempString, spring, index)
            lastPlacedIndex = index + spring
            
        
        if placedString:
            springCombinations.append(tempString)
        
    
    return springCombinations

def springPlacementCombinations(substring, springSizes, level=0):
    # See where we can place current spring
    # If there are more springs left, recursive
    # Place current spring, concat with recursive calls
    
    if not springSizes:
        return [substring]
    
    springCombinations = []
    prevChar = ""
    lastSubsetIndex = 0
    for i, c in enumerate(substring):
        if c not in ["?", "#"] or prevChar == "#":
            prevChar = c
            continue
        prevChar = c
        
        tempString = substring[:i] + substring[i:]
        placedString = True
        currentSpring = springSizes[0]
        
        index = canPlaceSpring(tempString, currentSpring, i)

        if index == -1: # If one spring cannot be placed, dont try the rest
            placedString = False
            break
        
        tempString =  placeSpring(tempString, currentSpring, index)
        
        if placedString:
            recursiveIndex = i +  currentSpring + 1
            lastSubsetIndex = i + index +  currentSpring
            
            recString = tempString[recursiveIndex:]
            affix = tempString[:recursiveIndex]
            
            if level > -1:
                print("{}{}: index: {}".format("  "*level,level, i), springSizes[1:])
                print("{} string: ".format("  "*level), tempString)
                print("{} Affix: ".format("  "*level), affix)
                print("{} Suffixes: ".format("  "*level), recString)
        
            if not springSizes[1:]:
                springCombinations.append(tempString)
                continue
        
            suffixes = springPlacementCombinations(recString, springSizes[1:], level+1)
            
            
            
            for suffix in suffixes:
                
                if False and level == 0 :
                    print("{} {} suffixes:".format(level,i), suffixes)
                    print("{} {} added:".format(level,i), tempString[:recursiveIndex] + suffix)
                
                springCombinations.append(affix + suffix)
        
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
    for i, c in enumerate(springStr[offset:]):
        iOff = i + offset
        #print(i, iOff, c)
        if c in ["?", "#"]:
            springSubset = springStr[iOff:iOff+springSize]
            if "." in springSubset:
                continue
            
            afterChar = springStr[iOff+springSize]
            #print(springSubset, afterChar)
            if afterChar in ["?", "."]:
                return iOff
            else:
                continue
                
            
    
    return -1


def part1(data):
    
    numComb = 0
    
    for s in data:
        
        paddedString = "."+s[0]+"."
        #springCombinations = combinationCounter(paddedString, s[1])
        print("====",paddedString, s[1])
        comb = springPlacementCombinations(paddedString, s[1])
        print("====",paddedString, s[1], len(comb))
        
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
            print("{} - Part 2: Sum of shortest distances {}".format(file, result))

if __name__ == "__main__":
    main(sys.argv[1:])