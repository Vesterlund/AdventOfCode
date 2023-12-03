import regex as re

f = open("input.txt")

fileContent = f.read()
fileContent = fileContent.split()

numDict = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}


totalSum = 0

for row in fileContent:
    start = 0
    end = len(row) - 1
    
    m = re.finditer(r"one|two|three|four|five|six|seven|eight|nine", row, overlapped=True)
    results = [mm for mm in m]

      
    firstWordStart = end
    lastWordEnd = 0

    foundWords = results != []
    if foundWords:
        firstWordStart = results[0].span()[0]
        lastWordEnd = results[-1].span()[1]
    
    tempString = "ab"
    foundCounter = 0
  


    while(start <= firstWordStart and foundCounter < 1):
        
        if str.isnumeric(row[start]):
            tempString = row[start] + tempString[1]
            foundCounter += 1
            break
        
        start+=1

    if start > firstWordStart:
        tempString = str(numDict[results[0].group(0)]) + tempString[1]
        foundCounter += 1

    while(lastWordEnd <= end and foundCounter < 2):
        
        if str.isnumeric(row[end]):
            tempString = tempString[0] + row[end]
            foundCounter += 1
            break
        
        end -= 1
    
    if lastWordEnd > end:
        tempString = tempString[0] + str(numDict[results[-1].group(0)])
        foundCounter += 1

    #print(row + " | " + str(lastWordEnd) + " | " + tempString)

    totalSum += int(tempString)

print("Total sum: " + str(totalSum))