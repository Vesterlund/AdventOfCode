f = open("input.txt", "r")

calList = []
tempCal = 0

for row in f:
    row = row.strip("\n")
    
    if(row == ""):
        calList.append(tempCal)
        tempCal = 0
    else:
        tempCal += int(row)
if(tempCal != 0):
    calList.append(tempCal)

f.close()

max3 = sorted(calList, reverse=True)[:3]
print(max3)
print(sum(max3))