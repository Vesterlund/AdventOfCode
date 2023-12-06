#inp = "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"
f = open("input.txt", 'r')
inp = f.read().strip()
f.close()

marker_pos = 14

memory = list(inp[0:marker_pos])
ind = marker_pos

def duplicate(l):
    for i,item in enumerate(l):
        if(item in l[i+1:]):
            return True

    return False

for c in inp[marker_pos:]:
    ind += 1
    
    memory = memory[1:] + [c]
    
    if(not duplicate(memory)):
        print("Index {}".format(ind))
        break