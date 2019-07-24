from itertools import combinations
from time import time

def initWolfram(rule,w):
    cases = [(rule >> i) & 1 for i in range(8)]
    field = [0 for i in range(w)]
    #field[w/2] = 1
    return (field,cases)

def updateWolfram(row,field,cases):
    tmp = []
    for i in range(len(field)):
        x = 0
        for j in range(-1,2):
            x = x * 2 + field[(i + j) % len(field)]
        tmp.append(cases[x])
    return tmp

def initConway(w,h):
    field = []
    return field

def updateConway(field,w,h,queue):
    field = set(field)
    while True:
        if queue.qsize() < 9000:
            aliveCells,deadCells = [],[]
            centers = {}
            for i in field:
                tmp = [((i[0] + a) % w,(i[1] + b) % h) for a,b in ((0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1))]
                
                if len(field.intersection(tmp)) in [2,3]: aliveCells.append(i)
                else: deadCells.append(i)

                getCenters(i,centers,field,w,h)

            for i in centers:
                if centers[i] == 3: aliveCells.append(i)
            aliveCells = set(aliveCells)
            queue.put((aliveCells,deadCells))
            
            field = aliveCells

def printField(field):
    #for debugging purposes
    for i in range(len(field)):
        x = ""
        for j in range(len(field[0])):
            x += str(field[i][j])
        print x

def neighbours(cell,field,w,h):
    l = []
    centers = []
    for i in range(-2,3):
        for j in range(-2,3):
            if ((cell[0] + i) % w,(cell[1] + j) % h) in field:
                l.append((cell[0] + i,cell[1] + j))
    l = [i for i in combinations(l,3) if cell in i]
    for i in l:
        t = []
        for j in i:
            t.append([((j[0] - a) % w,(j[1] - b) % h) for a,b in ((0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1))])
        centers += list(set(t[0]).intersection(t[1],t[2]))
    centers = [i for i in centers if centers.count(i) == 1]
    return centers

def getCenters(cell,centers,field,w,h):
    tmp = [((cell[0] + a) % w,(cell[1] + b) % h) for a,b in ((0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)) if ((cell[0] + a) % w,(cell[1] + b) % h) not in field]
    for i in tmp:
        if i in centers: centers[i] += 1
        else: centers[i] = 1   
