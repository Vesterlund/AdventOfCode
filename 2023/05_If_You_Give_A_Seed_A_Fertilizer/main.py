import numpy as np
import sys


def parseInput(fileContent):
    fileContent = fileContent.split(":")

    seeds = list(map(np.int64,fileContent[1][:fileContent[1].find("\n\n")].strip().split(" ")))

    translations = []

    for row in fileContent[2:]:
        temp = row[:row.find("\n\n")].strip().split("\n")
        tempTranslation = []
        for item in temp:
            tempTranslation.append(list(map(np.int64, item.split(" "))))
        
        translations.append(tempTranslation)
    return (seeds, translations)

def readFile(filepath:str):
    f = open(filepath)

    fileContent = f.read()
    f.close()

    return fileContent

def part1(filePath:str):
    fileContent = readFile(filePath)

    seeds, translations = parseInput(fileContent)
    #print(seeds)
    for step in translations:
        #print("Next step:")
        newSeeds = []
        originalSeeds = seeds
        for mapping in step:
            #print(mapping, seeds)

            dest = mapping[0]
            src = mapping[1]
            length = mapping[2]

            tempSeeds = []

            for seed in originalSeeds:
                #print("Seed: ", seed)
                #If seed in mapping range
                if seed >= src and seed < src + length:
                    temp = dest + (seed - src)
                    #print("Mapping {} -> {}".format(seed, temp))
                    newSeeds.append(temp)
                else:
                    tempSeeds.append(seed)
            
            originalSeeds = tempSeeds
        
        seeds = originalSeeds + newSeeds
        #print(seeds)
    
    print("{} - Part 1: Lowest location: {}".format(filePath,np.min(seeds)))


def part2reversebrute(filePath):
    fileContent = readFile(filePath)

    seeds, translations = parseInput(fileContent)

    translations.reverse()
    i = 0
    while True:
        #print("========")

        if (i % 10000 == 0):
            print("i={}".format(i))
        currentNum = i

        for step in translations:
            #print(step)
            for mapping in step:
                dest = mapping[0]
                src = mapping[1]
                length = mapping[2]

                if currentNum >= dest and currentNum < dest + length:
                    temp = currentNum - dest + src
                    #print("{}: Mapping {} -> {}, dest: {}".format(i,currentNum, temp,dest))
                    currentNum = temp
                    break
        
        for j in range(0, len(seeds),2):
            if currentNum >= seeds[j] and currentNum < seeds[j] + seeds[j+1]:
                print("{} - Part 2: Lowest location: {}".format(filePath,i))
                return
        #print("Final: {}".format(currentNum))

        i += 1

part1("example.txt")
part1("input.txt")
part2reversebrute("example.txt")
part2reversebrute("input.txt")