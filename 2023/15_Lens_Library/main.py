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


    data = fileContent.strip().split(",")
        
    return data

def doHash(string : str):
    hashValue = 0
    
    for c in string:
        hashValue += ord(c)
        hashValue = (hashValue * 17) % 256
    
    return hashValue

class lens:
    label = ""
    focalLength = 0
    nextLens = None
    prevLens = None
    
    def __init__(self, label, focalLength) -> None:
        self.label = label
        self.focalLength = int(focalLength)
    
    def compareLabel(self, lens):
        return self.label == lens.label
    
    def addLast(self, lens):
        if self.nextLens:
            self.nextLens.addLast(lens)
        else:
            self.nextLens = lens
            self.nextLens.prevLens = self
    
    def __str__(self):
        temp = "[{}, {}]".format(self.label, self.focalLength)
        
        if self.nextLens:
            temp += " -> " + self.nextLens.__str__()
        
        return temp
    

def part1(data):
    
    sumOfHashes = 0
    for string in data:
        sumOfHashes += doHash(string)
        
    return sumOfHashes

def createHashTable(data : list[str]):
    hashTable = dict()
    
    for i in range(256):
        hashTable[i] = None
    
    def removeLens(remLens):
        hashCode = doHash(remLens.label)
        
        if hashCode in hashTable:
            head : lens = hashTable[hashCode]
            
            currentLens : lens = hashTable[hashCode] 
            
            while currentLens:
                if currentLens.compareLabel(remLens):
                    if currentLens == head: 
                        hashTable[hashCode] = head.nextLens
                        if head.nextLens:
                            head.nextLens.prevLens = None
                    else:
                        currentLens.prevLens.nextLens = currentLens.nextLens
                        
                        if currentLens.nextLens:
                            currentLens.nextLens.prevLens = currentLens.prevLens
                    
                    break
                
                currentLens = currentLens.nextLens
            
    def addLens(newLens):
        # Add/Update lens  
        hashCode = doHash(newLens.label)
        
        
        if not hashTable[hashCode]:
            hashTable[hashCode] = newLens
        else:
            currentLens : lens = hashTable[hashCode] 
            
            updatedFocal = False
            
            while currentLens:
                if currentLens.compareLabel(newLens):
                    currentLens.focalLength = newLens.focalLength
                    updatedFocal = True
                    break
                
                currentLens = currentLens.nextLens
            
            if not updatedFocal:
                hashTable[hashCode].addLast(newLens)

    
    for string in data:
        
        if "-" in string:
            label = string.replace("-","")
            remLens = lens(label, -1)
            
            removeLens(remLens)
        else:
            label = string.split("=")[0]
            focalLength = string.split("=")[1]
            newLens = lens(label, focalLength)
            
            addLens(newLens)

  
    return hashTable

def calculateFocusingPower(hashTable):
    focusingPower = 0
    
    for key in hashTable:
        if hashTable[key]:
            currentLens = hashTable[key]
            
            index = (int(key) + 1)
            slot = 1

            temp = slot * currentLens.focalLength
            
            while currentLens.nextLens:
                slot += 1
                currentLens = currentLens.nextLens
                
                temp += slot * currentLens.focalLength
            
            focusingPower += temp * index
            
    return focusingPower

def part2(data):
    
    hashTable = createHashTable(data)
    
    for key in hashTable:
        if hashTable[key]:
            
            currentLens = hashTable[key]
            
            index = (int(key) + 1)
            slot = 1

            temp = index * slot * currentLens.focalLength
            
            while currentLens.nextLens:
                slot += 1
                currentLens = currentLens.nextLens
                
                temp += index * slot * currentLens.focalLength
    
    focusingPower = calculateFocusingPower(hashTable)
    
    return focusingPower
    


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
            print("{} - Part 1: Sum of hashes {}".format(file, result))
        
        if not noPartTwo:
            result = part2(data)
            print("{} - Part 2: Focusing power {}".format(file, result))

if __name__ == "__main__":
    main(sys.argv[1:])