import sys, getopt
import numpy as np
import math
import re


def readFile(filepath:str):
    f = open(filepath)

    fileContent = f.read()
    f.close()

    return fileContent

class Module(object):

    def __init__(self, name, output) -> None:
        self.name = name
        self.output = []
        self.lastPulse = 0

        for out in output.split(","):
            self.output.append(out.strip())
    
    def __iter__(self):
        self.n = 0
        return self
    
    def __len__(self):
        return len(self.output)

    def __next__(self):
        if self.n < len(self.output):
            self.n += 1
            return self.output[self.n-1]
        else:
            raise StopIteration

    def getOutputModules(self):
        return self.output
    
    def receivePulse(self, pulseSender, pulse):
        return

    def __str__(self) -> str:
        return "{} -> {}".format(self.name, self.output)

class BroadCaster(Module): 

    def __init__(self, *args) -> None:
        super().__init__(*args)

    def transmitPulse(self, pulseSender, pulse):
        return -1

class TestModule(Module):
    def __init__(self, *args) -> None:
        super().__init__(*args)

    def transmitPulse(self,pulseSender, pulse):
        return 0

class FlipFlop(Module):
    def __init__(self, *args) -> None:
        self.isOn = False
        super().__init__(*args)

    def transmitPulse(self, pulseSender, pulse):
        if pulse == -1:
            return 1 if not self.isOn else -1

        return 0
    
    def flip(self):
        self.isOn = not self.isOn

class ConjunctionModule(Module):
    def __init__(self, *args) -> None:
        self.lastPulses = {}
        super().__init__(*args)

    def receivePulse(self, pulseSender, pulse):
        self.lastPulses[pulseSender] = pulse

    def transmitPulse(self, pulseSender, pulse):
        self.receivePulse(pulseSender, pulse)

        foundLow = False
        foundHigh = False

        for key in self.lastPulses:
            match self.lastPulses[key]:
                case 1: foundHigh = True
                case -1: foundLow = True
            
        if foundHigh + foundLow == 2:
            return 0

        return -1 if foundHigh else 1

import copy

def parseInput(filePath:str):
    fileContent = readFile(filePath)


    data = fileContent.split("\n")
    
    moduleDict = {}

    for row in data:
        parts = row.split("->")

        if parts[0][0] == "%":
            moduleDict[parts[0][1:].strip()] = FlipFlop(parts[0][1:],parts[1])
        elif parts[0][0] == "&":
            moduleDict[parts[0][1:].strip()] = ConjunctionModule(parts[0][1:],parts[1])
        elif parts[0][0] == "b":
            moduleDict[parts[0].strip()] = BroadCaster(parts[0],parts[1])

    # send default low pulse to set conj modules
    tempDict = copy.deepcopy(moduleDict)

    for key in tempDict:
        for out in tempDict[key]:
            if out not in tempDict:
                moduleDict[out] = TestModule(out, "")
            moduleDict[out].receivePulse(key, -1)

    return moduleDict

def pushButton(moduleDict):

    lowPulses = 1 # initial pulse
    highPulses = 0

    start = "broadcaster"
    startPulse = -1

    sendQueue = [(start, [(startPulse, r) for r in moduleDict[start]])]
    while sendQueue:
        #print(sendQueue)
        pulseGroup = sendQueue.pop(0)
        sender = pulseGroup[0]
        for pulsese  in pulseGroup[1]:
            pulse, rec = pulsese
            if pulse == 1:
                highPulses += 1
            else:
                lowPulses += 1

            print(sender, pulse, " -> ", rec)
            temp = moduleDict[rec].transmitPulse(sender, pulse)
            print("  {} sends pulse {} to {}".format(rec, temp, [x for x in moduleDict[rec]]))
            if temp == 0:
                continue

            
            sendQueue += [(rec,[(temp, r) for r in moduleDict[rec]])]

        if isinstance(moduleDict[sender], FlipFlop):
            moduleDict[sender].flip()

    return lowPulses, highPulses

def part1(data):
    moduleDict = data

    print(pushButton(moduleDict))


    return 0

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
            result = part1(data)
            print("{} - Part 1: {} Total ratings for all parts  ".format(file, result))
        
        if not noPartTwo:
            result = part2(data)
            print("{} - Part 2: {} Total different part combinations ".format(file, result))

if __name__ == "__main__":
    main(sys.argv[1:])