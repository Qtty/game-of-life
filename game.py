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
    field = [[0 for j in range(w)] for i in range(h)]
    return field

def updateConway(field,w,h):
    newField = [[0 for j in range(w)] for i in range(h)]
    for i in range(h):
        for j in range(w):
            tmp = [field[(i + a) % h][(j + b) % w] for a,b in ((0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1))]
            if field[i][j]:
                if tmp.count(1) in [2,3]:
                    newField[i][j] = 1
            elif tmp.count(1) == 3:
                newField[i][j] = 1
    return newField

def printField(field):
    for i in range(len(field)):
        x = ""
        for j in range(len(field[0])):
            x += str(field[i][j])
        print x


