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
        self.inputConnections = []
        self.outPulse = 0
        super().__init__(*args)

    def updateOutPulse(self,moduleDict):
        
        ifHigh = False
        ifLow = False
        print("     Updating conj:", self.name)
        for key in self.inputConnections:
            val = moduleDict[key]['lastPulse']
            print("    ", key, val)
            if val == 1:
                ifHigh = True
            elif val == 0:
                ifLow = True
        rVal = 0
        if ifHigh+ifLow == 2: rVal = 0
        else: rVal = -1 if ifHigh else 1
        print("    ", self.name, " : Updating to ", rVal)

        self.outPulse = rVal
    

    
    def transmitPulse(self, pulseSender, pulse):
        return self.outPulse

import copy

def parseInput(filePath:str):
    fileContent = readFile(filePath)


    data = fileContent.split("\n")
    
    moduleDict = {}

    for row in data:
        parts = row.split("->")

        if parts[0][0] == "%":
            moduleDict[parts[0][1:].strip()] = {'mod': FlipFlop(parts[0][1:],parts[1]), 'lastPulse':-1}
        elif parts[0][0] == "&":
            moduleDict[parts[0][1:].strip()] = {'mod': ConjunctionModule(parts[0][1:],parts[1]), 'lastPulse':-1}
        elif parts[0][0] == "b":
            moduleDict[parts[0].strip()] = {'mod': BroadCaster(parts[0],parts[1]), 'lastPulse':-1}

    # send default low pulse to set conj modules
    tempDict = copy.deepcopy(moduleDict)
    for key in tempDict:
        for out in tempDict[key]["mod"].output:
            if out not in tempDict:
                moduleDict[out] = {'mod': TestModule(out, ""), 'lastPulse':0}
            moduleDict[out]['mod'].receivePulse(key, -1)
        
    for key in moduleDict:
        for k2 in moduleDict[key]["mod"].output:
            if not k2:
                continue
            if isinstance(moduleDict[k2]['mod'], ConjunctionModule):
                moduleDict[k2]['mod'].inputConnections.append(key)

    
    return moduleDict

def pushButton(moduleDict):

    lowPulses = 1 # initial pulse
    highPulses = 0

    start = "broadcaster"
    startPulse = -1
    sendQueue = [(start, [(startPulse, r) for r in moduleDict[start]['mod']])]
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

           
            
            
            if isinstance(moduleDict[sender]['mod'], ConjunctionModule):
                print("cnojmod: ", sender)
                moduleDict[sender]['mod'].updateOutPulse(moduleDict)
                pulse = moduleDict[sender]['mod'].outPulse
            
            temp = moduleDict[rec]['mod'].transmitPulse(sender, pulse)
            print(sender, pulse, " -> ", rec, " ({})".format(temp))
            moduleDict[rec]['lastPulse'] = temp
            #print("  {} sends pulse {} to {}".format(rec, temp, [x for x in moduleDict[rec]['mod']]))
            if temp == 0:
                continue

            
            sendQueue += [(rec,[(temp, r) for r in moduleDict[rec]['mod']])]

        if isinstance(moduleDict[sender]['mod'], FlipFlop):
            moduleDict[sender]['mod'].flip()

    return lowPulses, highPulses

def part1(data):
    moduleDict = data
    print(moduleDict)

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