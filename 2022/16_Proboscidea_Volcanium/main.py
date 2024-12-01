import sys, getopt
import re
import numpy as np


def readFile(filepath:str):
    f = open(filepath)

    fileContent = f.read()
    f.close()

    return fileContent.split("\n")

def parseInput(filePath:str):

    fileContent = readFile(filePath)

    valveIndex = set()
    valveInfo = dict()
    
    for row in fileContent:
        valveRegex = r'([A-Z][A-Z])'
        
        valves = re.findall(valveRegex, row)

        for valve in valves:
            if valve not in valveIndex:
                valveIndex.add(valve)

        flowrate = re.search(r"\d+",row).group(0)
        valveInfo.update({valves[0]: {"flow": flowrate, "links": valves[1:]}})

    return [valveIndex, valveInfo]

def createShortestMatrix(cMatrix):
    shortestMatrix = cMatrix
    anotherStep = cMatrix
    power = 2
    while np.min(shortestMatrix) == 0 and power < 31:
        anotherStep = anotherStep + np.matmul(anotherStep, anotherStep)

        for i in range(len(shortestMatrix)):
            for j in range(len(shortestMatrix)):
                if shortestMatrix[i][j] == 0 and anotherStep[i][j] != 0:
                    shortestMatrix[i][j] = power


        power += 1

    np.fill_diagonal(shortestMatrix, 0)

    return shortestMatrix



def part1(data):

    valves = list(data[0])
    valves.sort()
    valveInfo = data[1]

    nValves = len(valves)

    connectionMatrix = np.zeros((nValves, nValves))
    
    closedValveFlow = np.zeros((nValves, 1))

    for valve in valveInfo.keys():
        i = valves.index(valve)
        closedValveFlow[i] = valveInfo[valve]["flow"]
        for connectionValve in valveInfo[valve]["links"]:
            j = valves.index(connectionValve)
            connectionMatrix[i][j] = 1


    currentValve = 0
    shortestMatrix = createShortestMatrix(connectionMatrix)
    closedValveFlow = np.transpose(closedValveFlow)

    maxTime = 30
    cTime = 0

    totalUnitFlow = 0
    totalFlow = 0

    while cTime < maxTime:
        timeLeft = maxTime - cTime
        currentStep = closedValveFlow*(timeLeft - shortestMatrix)
        nextStep = closedValveFlow*(timeLeft-2*shortestMatrix)
        

        measure = currentStep + nextStep

        chosenValve = np.argmax(measure[currentValve])

        


        deltaTime = shortestMatrix[currentValve][chosenValve] + 1

        totalFlow += totalUnitFlow * deltaTime
        totalUnitFlow += closedValveFlow[0][chosenValve]
        cTime += deltaTime + 1
        closedValveFlow[0][chosenValve] = 0

        print("== Minute {} ==\nValve realeasing {}\nMoving {} -> {}".format(int(cTime),totalUnitFlow,currentValve, chosenValve))

        currentValve = chosenValve
        

    print(totalFlow)

    openValves = []



    return

def part2(data):
    return


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
    

    problemFiles = ["example.txt", "input.txt"]

    problemFiles = problemFiles if not onlyExample else problemFiles[:1]

    for file in problemFiles:
        data = parseInput(file)

        if not noPartOne:
            part1(data)
        
        if not noPartTwo:
            part2(data)






if __name__ == "__main__":
   main(sys.argv[1:])