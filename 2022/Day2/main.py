f = open("input.txt", "r")
# Rock  A X
# Paper B Y
# Sci   C Z



def translate(c):
    if c == 'X': return ('A',1)
    if c == 'Y': return ('B',2)
    if c == 'Z': return ('C',3)


def theLandOfIf(a,b):
    if a == 'A' and b == 'X': return (0,3)
    if a == 'A' and b == 'Y': return (3,1)
    if a == 'A' and b == 'Z': return (6,2)
    if a == 'B' and b == 'X': return (0,1)
    if a == 'B' and b == 'Y': return (3,2)
    if a == 'B' and b == 'Z': return (6,3)
    if a == 'C' and b == 'X': return (0,2)
    if a == 'C' and b == 'Y': return (3,3)
    if a == 'C' and b == 'Z': return (6,1)
score = 0
score2 = 0
for row in f:
    row = row.strip("\n")
    move = row.split()
    a,b = theLandOfIf(move[0],move[1])
    score2 += a + b
    move[1], pScore = translate(move[1])
    
    if(move[0] == move[1]): score += 3
    if(move[0] == 'A' and move[1] == 'B'): score += 6
    if(move[0] == 'B' and move[1] == 'C'): score += 6
    if(move[0] == 'C' and move[1] == 'A'): score += 6

    score += pScore
    
f.close()

print("Score: {}\nScore2: {}".format(score,score2))