from collections import Counter
from functools import cmp_to_key

def readFile(filepath:str):
    f = open(filepath)

    fileContent = f.read()
    f.close()

    return fileContent

def strArrToNum(arr):
    return list(map(int, arr))

def cardToValueMap(card):
    values = ['0', 'J', '2','3','4','5','6','7','8','9','T','J','Q','K','A']

    return values.index(card)
    

def parseInput(fileContent):

    rows = fileContent.split("\n")
    
    hands = []


    for row in rows:
        data = row.split(" ")

        hand, bid = data[0], data[1]

        hands.append((hand,int(bid)))

    return hands


def getHandType(hand):
    values = Counter(hand).values()
    nUniqueVals = len(values)

    if nUniqueVals == 5:
        return 1
    elif nUniqueVals == 4:
        return 2
    elif nUniqueVals == 3 and max(values) == 2:
        return 3
    elif nUniqueVals == 3:
        return 4
    elif nUniqueVals == 2 and max(values) == 3:
        return 5
    elif nUniqueVals == 2:
        return 6
    else:
        return 7

def sortHands(h1, h2):

    if (h1[1] > h2[1]):
        return 1
    
    elif (h1[1] == h2[1]):
        for c1, c2 in zip(h1[0], h2[0]):
            if c1 == c2:
                continue
            
            return 1 if cardToValueMap(c1) > cardToValueMap(c2) else -1
        
        return 0
    else:
        return -1

def getJokerValue(hand : str):
    keys = list(Counter(hand).keys())
    vals = list(Counter(hand).values())

    replaceWith = ""

    maxFound = 0

    for i in range(len(vals)):
        if keys[i] != "J":
            if vals[i] > maxFound:
                maxFound = vals[i]
                replaceWith = keys[i]
            elif vals[i] == maxFound:
                replaceWith = keys[i] if cardToValueMap(keys[i])> cardToValueMap(replaceWith) else replaceWith


    return hand.replace("J", replaceWith)



def solve(filepath, part):
    hands = parseInput(readFile(filepath))

    handWithType = []

    for hand in hands:
        cards = hand[0] if part == 1 else getJokerValue(hand[0])

        handWithType.append((hand[0], getHandType(cards), hand[1]))

    
    handsWithType = sorted(handWithType,key=cmp_to_key(sortHands))


    totalWinnings = 0
    for i,hand in enumerate(handsWithType):
        totalWinnings += (i+1)*hand[2]

    
    print("{} - Part {}: Total winnings {}".format(filepath, part, totalWinnings))


for file in ["example.txt", "input.txt"]:
    solve(file,1)
    solve(file,2)
