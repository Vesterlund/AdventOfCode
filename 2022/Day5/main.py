# File parse
f = open("input.txt", "r")
x = []
for row in f:
    if(row != '\n'):
        x.append(row.strip('\n'))
f.close()


# General parsing
storage = []
instructions = []

stored = False

width = 0
height = 0
for row in x:
    if(stored):
        instructions.append(row)
    elif(row[1] == '1'):
        stored = True
        width = int(row[-2])
    else:
        storage.append(row)
        height += 1

storage.reverse()
warehouse = [[] for _ in range(width)]
for i,row in enumerate(storage):
    for j in range(width):
        if(row[4*j + 1] != ' '):
            warehouse[j].append(row[4*j + 1])


#Quick maths
for i in instructions:
    parts = i.split()

    amt = int(parts[1])
    src = int(parts[3]) - 1
    dst = int(parts[5]) - 1

    temp = warehouse[src][-amt:]
    #temp.reverse()
    warehouse[src] = warehouse[src][:-amt]
    warehouse[dst] = warehouse[dst] + temp

flag = ""

for col in warehouse:
    flag += col[-1]

print("flag: {}".format(flag))
