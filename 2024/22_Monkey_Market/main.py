import sys, getopt
import time
import numpy as np
import math
import re
from enum import Enum
import copy
import queue
from collections import defaultdict
from functools import cache
np.set_printoptions(threshold=sys.maxsize, linewidth=sys.maxsize)

def readFile(filepath:str):
    f = open(filepath)

    fileContent = f.read()
    f.close()

    return fileContent

def parseInput(filePath:str):
    fileContent = readFile(filePath)
    data = fileContent.split("\n")
    
    
    return list(map(int,data))


def mix(secret, inp):
    
    return secret ^ inp
    

def prune(secret):
    return secret % 16777216

def generateSecret(seed):
    
    s_temp = seed*64
    seed = prune(mix(seed, s_temp))

    s_temp = seed // 32
    seed = prune(mix(seed, s_temp))
    
    s_temp = seed * 2048
    seed = prune(mix(seed, s_temp))
    
    return seed
    
    
def part1(data):
    initial_secrets = data
    
    secret_sum = 0
    
    for secret in initial_secrets:
        for _ in range(2000):
            secret = generateSecret(secret)

        secret_sum += secret
    
    return secret_sum


def part2(data):
    initial_secrets = data
    
    seqence_score = {}
 
    for secret in initial_secrets:
        
        seen_sequences = set()
        prev_num = secret % 10
        seq = []
        
        for _ in range(2000):
            secret = generateSecret(secret)

            c_num = secret % 10
            diff = c_num - prev_num
            prev_num = c_num
            
            if len(seq) < 3:
                seq.append(diff)
                continue
            
            seq.append(diff)
            seq_id = ",".join(str(x) for x in seq)
            seq = seq[1:]
            
            if seq_id in seen_sequences:
                continue
            
            seen_sequences.add(seq_id)
            
            if seq_id not in seqence_score:
                seqence_score[seq_id] = 0
            
            seqence_score[seq_id] += c_num
    
    return max(seqence_score.values())

    

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
            s_t = time.perf_counter()
            result = part1(copy.deepcopy(data))
            e_t = time.perf_counter()
            print("{} - Part 1: {} | {:.3}s".format(file, result, e_t - s_t))
        
        if not noPartTwo:
            s_t = time.perf_counter()
            result = part2(copy.deepcopy(data))
            e_t = time.perf_counter()
            print("{} - Part 2: {} | {:.3}s".format(file, result, e_t - s_t))

if __name__ == "__main__":
    main(sys.argv[1:])