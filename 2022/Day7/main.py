import json
f = open("input.txt", "r")

def traverse(index, instructions, folders, cDir):
    subTree = {}
    folderSize = 0
    while(index < len(instructions)):
        row = instructions[index]
        index += 1
        if(row == "$ cd .."):
            subTree["_size"] = folderSize
            folders.append(folderSize)
            
            return subTree, index, folderSize, folders

        if(row.startswith("$ cd ")):
            dirName = row.split()[2]
            
            subTree[dirName], index, subFolderSize, folders = traverse(index, instructions, folders, dirName) 
            folderSize += subFolderSize
        if(not row.startswith("dir") and not row.startswith("$")):
            size, filename = row.split()
            subTree[filename] = int(size)
            folderSize += int(size)
    subTree["_size"] = folderSize
    folders.append(folderSize)
    return subTree, index, folderSize, folders
        

tree = {}
folders = []
wdir = None

instructions = []
for row in f:
    instructions.append(row.strip("\n"))

f.close()

tree, _, _, folders = traverse(0, instructions, folders, "")
#print(json.dumps(tree,sort_keys=True,indent=2))
#print(folders)

folderSum = 0

for folderSize in folders:
    #folderSize = folders[folder]
    if folderSize <= 100000:
        folderSum += folderSize

#44359867

totalSpace = 70000000
minUnused = 30000000
used = tree["/"]["_size"]
freeSize = totalSpace - used

chosen = used


for folderSize in folders:
    if(freeSize + folderSize >= minUnused):
        chosen = min(chosen, folderSize)

    


print("Total size: {}, foldersize: {}".format(folderSum, chosen))