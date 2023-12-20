import sys, getopt
import numpy as np
import math
import re
from enum import Enum


def readFile(filepath:str):
    f = open(filepath)

    fileContent = f.read()
    f.close()

    return fileContent

State = Enum("State", ["HIGH", "LOW"])
buttonPresses = 0

class Module(object):

    def __init__(self, name, output) -> None:
        self.name = name
        self.output = []

        if not output:
            return
        
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
    
    def receivePulse(self, pulse):
        return

    def __str__(self) -> str:
        return "{} -> {}".format(self.name, self.output)

class BroadCaster(Module): 

    def __init__(self, *args) -> None:
        super().__init__(*args)

    def transmitPulse(self, pulse):
        return State.LOW

class MachineModule(Module):
    def __init__(self, *args) -> None:
        super().__init__(*args)

    def transmitPulse(self, pulse):
        return 0

class FlipFlop(Module):
    def __init__(self, *args) -> None:
        self.isOn = False
        super().__init__(*args)

    def transmitPulse(self, pulse):
        if pulse == State.LOW:
            return State.HIGH if self.isOn else State.LOW

        return 0
    
    def flip(self):
        self.isOn = not self.isOn

class ConjunctionModule(Module):
    def __init__(self, *args) -> None:
        self.pulseMemory = {}
        self.highPulse = {}
        self.outPulse = 0
        super().__init__(*args)

    def updateMemory(self,sender, pulse):
        #print("     Updating:", self.name, "{}:{}".format(sender, pulse))
        self.pulseMemory[sender] = pulse

        if pulse == State.HIGH and self.highPulse[sender] == 0:
            self.highPulse[sender] = buttonPresses
    
    def allHaveBeenHigh(self):
        return all(self.highPulse.values())

    def transmitPulse(self, pulse):
        return State.LOW if all([self.pulseMemory[k] == State.HIGH for k in self.pulseMemory]) else State.HIGH

import copy

def parseInput(filePath:str):
    fileContent = readFile(filePath)


    data = fileContent.split("\n")
    
    moduleDict = {}

    for row in data:
        parts = row.split("->")

        if parts[0][0] == "%":
            moduleDict[parts[0][1:].strip()] = {'mod': FlipFlop(parts[0][1:],parts[1]), 'lastReceived':State.LOW, "currentPress":0}
        elif parts[0][0] == "&":
            moduleDict[parts[0][1:].strip()] = {'mod': ConjunctionModule(parts[0][1:],parts[1]), 'lastReceived':State.LOW, "currentPress":0}
        elif parts[0][0] == "b":
            moduleDict[parts[0].strip()] = {'mod': BroadCaster(parts[0],parts[1]), 'lastReceived':State.LOW, "currentPress":0}

    # send default low pulse to set conj modules
    tempDict = copy.deepcopy(moduleDict)
    for key in tempDict:
        for out in tempDict[key]["mod"].output:
            if out not in tempDict:
                moduleDict[out] = {'mod': ConjunctionModule(out, ""), 'lastReceived':State.LOW, "currentPress":0}
        
    for key in moduleDict:
        for k2 in moduleDict[key]["mod"].output:
            if not k2:
                continue
            if isinstance(moduleDict[k2]['mod'], ConjunctionModule):
                moduleDict[k2]['mod'].pulseMemory[key] = State.LOW
                moduleDict[k2]['mod'].highPulse[key] = 0

    
    return moduleDict

def pushButton(moduleDict):

    lowPulses = 0
    highPulses = 0

    for k in moduleDict:
            moduleDict[k]["currentPress"] = 0

    start = "button"
    startPulse = State.LOW
    sendQueue = [("broadcaster", startPulse, start)]
    machinePulsesReceived = 0

    while sendQueue:
        
        pulseGroup = sendQueue.pop(0)
        receiver = pulseGroup[0]
        pulse = pulseGroup[1]
        sender = pulseGroup[2]

        if pulse == State.HIGH:
                highPulses += 1
        else:
            lowPulses += 1

        receivingModule = moduleDict[receiver]["mod"]
        
        if isinstance(receivingModule, FlipFlop) and pulse == State.LOW:
            #print("Flip!")
            receivingModule.flip()

        if isinstance(receivingModule, ConjunctionModule):
            #print("cnojmod: ", receiver)
            receivingModule.updateMemory(sender, pulse)
        
        if isinstance(receivingModule, MachineModule):
            machinePulsesReceived+= 1

        nexPulse = receivingModule.transmitPulse(pulse)

        moduleDict[receiver]["lastReceived"] = pulse
        moduleDict[receiver]["currentPress"] = nexPulse

        if nexPulse == 0:
            continue

        sendQueue += [(x, nexPulse, receiver) for x in receivingModule.output]
  
    return lowPulses, highPulses, (machinePulsesReceived == 1)

def part1(data):
    moduleDict = data
    totalLow = 0
    totalHigh = 0

    for i in range(0,1000):
        lo, hi, _ = pushButton(moduleDict)
        totalLow+= lo
        totalHigh += hi

    return totalLow*totalHigh

from math import lcm

def part2(data):
    # Doing some input digging:
    # only hb -> rx
    # js  -> hb
    # zb  -> hb
    # bs  -> hb
    # rr  -> hb


    # Now the keys areall appearing in some large output array
    # Want to find cycle of these keys 

    # Hb is & -> all senders to hb must be 1 for it to send a low pulse
 
    moduleDict = data  

    global buttonPresses

    buttonPresses += 1

    while True:
        pushButton(moduleDict)
        
        if moduleDict["hb"]["mod"].allHaveBeenHigh():
            return lcm(*moduleDict["hb"]["mod"].highPulse.values())
            
        buttonPresses += 1


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
            print("{} - Part 1: {} Pulse multiplier  ".format(file, result))
        
        if not noPartTwo:
            result = part2(copy.deepcopy(data))
            print("{} - Part 2: {} Button presses ".format(file, result))

if __name__ == "__main__":
    main(sys.argv[1:])