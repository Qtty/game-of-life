#!/usr/bin/python

from pygame import init,display,image,event,key,Surface,draw,font
import string
from pygame.locals import *
from game import *
from constants import *
from sys import argv
from time import sleep,time
from json import loads,dumps
import multiprocessing as mp
from os import getpid,kill
from signal import SIGKILL

def initScreen():
    init()
    window = display.set_mode((width,height),RESIZABLE)
    window.fill(WHITE)
    tmp = Surface((1,height))
    tmp.fill(GRAY)
    for i in range(width/cellWidth):
        window.blit(tmp,(i * cellWidth,0))

    tmp = Surface((width,1))
    tmp.fill(GRAY)
    for i in range(height/cellHeight):
        window.blit(tmp,(0,i * cellHeight))

    display.flip()
    return window

def updateScreenWolfram(field,row):
    for i in range(len(field)):
        if field[i]:
            window.blit(blackCell,(i * cellWidth,row * cellHeight))
    display.flip()

def updateScreenConway(aliveCells,deadCells):
    for i in aliveCells:
        window.blit(blackCell,(i[0] * cellWidth,i[1] * cellHeight))
    for i in deadCells:
        window.blit(whiteCell,(i[0] * cellWidth,i[1] * cellHeight))
    
    window.blit(grid,(0,0))
    display.flip()

def get_key():
    while 1:
        evnt = event.poll()
        if evnt.type == KEYDOWN:
            if (evnt.key >= 0x100 and evnt.key <= 0x109): return evnt.key - 0xD0
            else: return evnt.key
        else: pass

def display_box(message):
    "Print a message in a box in the middle of the window"
    fontobject = font.Font(None,18)
    draw.rect(window, BLACK,((window.get_width() / 2) - 100,(window.get_height() / 2) - 10,200,20), 0)
    draw.rect(window, WHITE,((window.get_width() / 2) - 102,(window.get_height() / 2) - 12,204,24), 1)
    if len(message) != 0: window.blit(fontobject.render(message, 1, WHITE),((window.get_width() / 2) - 100, (window.get_height() / 2) - 10))
    display.flip()

def ask(question):
    "ask(question) -> answer"
    font.init()
    answer = ""
    tmp = window.copy()
    display_box("{}: {}".format(question,answer))
    while 1:
        inkey = get_key()
        if inkey == K_BACKSPACE: answer = answer[0:-1]
        elif inkey == K_RETURN: break
        elif inkey == K_MINUS: answer.append("_")
        elif inkey <= 127: answer += chr(inkey)
        display_box("{}: {}".format(question,answer))
    window.blit(tmp,(0,0))
    return answer

def Conway():
    field = initConway(width / cellWidth,height / cellHeight)
    with open("forms","r") as f:
        d = loads(f.read())
    c = 1
    x = 0
    done = 0
    save = 0
    saving = []
    while c:
        for e in event.get():
            if e.type == QUIT:
                c = 0
                kill(p.pid,SIGKILL)
            
            elif e.type == MOUSEBUTTONDOWN:
                if (e.pos[0] / cellWidth,e.pos[1] / cellHeight) not in field:
                    field.append((e.pos[0] / cellWidth,e.pos[1] / cellHeight))
                    window.blit(blackCell,(e.pos[0] - e.pos[0] % cellWidth,e.pos[1] - e.pos[1] % cellHeight))
                    if save: saving.append((e.pos[0] / cellWidth,e.pos[1] / cellHeight))
                else:
                    del field[field.index((e.pos[0] / cellWidth,e.pos[1] / cellHeight))]
                    window.blit(whiteCell,(e.pos[0] - e.pos[0] % cellWidth,e.pos[1] - e.pos[1] % cellHeight))
                    if save: del saving[saving.index((e.pos[0] / cellWidth,e.pos[1] / cellHeight))]
                display.flip()
            
            elif e.type == KEYDOWN:
                if e.key == K_RETURN:
                    x = 1 - x
                    if not done:
                        queue = mp.Queue()
                        p = mp.Process(target=updateConway,args=(field,width / cellWidth,height / cellHeight,queue))
                        p.start()
                        done = 1

                elif e.key == K_l:
                    form = ask("form?")
                    pos = int(ask("place?"))
                    field = list(field)
                    for i in d[form]:
                        field.append((i[0] + pos,i[1] + pos))
                        window.blit(blackCell,((pos + i[0]) * cellWidth,(pos + i[1]) * cellHeight))
                    field = set(field)
                    display.flip()
                
                elif e.key == K_r:
                    window.fill(WHITE)
                    window.blit(grid,(0,0))
                    field = initConway(width / cellWidth,height / cellHeight)
                    x = 0
                    done = 0
                    kill(p.pid,SIGKILL)
                    display.flip()
                
                elif e.key == K_s:
                    save = 1 - save
                    if not save:
                        saving.sort()
                        saving = [[i[0]-saving[0][0],i[1]][::-1] for i in saving]
                        saving.sort()
                        saving = [[i[0]-saving[0][0],i[1]][::-1] for i in saving]
                        d[ask("form name?")] = tuple(saving)
                        saving = []
                    with open("forms","w") as f:
                        f.write(dumps(d))
        if x:
            try:
                field,dead = queue.get()
                updateScreenConway(field,dead)
            except:
                pass

def Wolfram(rule):
    field,cases = initWolfram(rule,width/cellWidth)
    c = 1
    while c:
        for e in event.get():
            if e.type == QUIT:
                c = 0
            elif e.type == MOUSEBUTTONDOWN:
                field[e.pos[0] / cellWidth] = 1
                window.blit(blackCell,(e.pos[0] - e.pos[0] % cellWidth,0))
                display.flip()
            elif e.type == KEYDOWN:
                if e.key == K_RETURN:
                    c = 0
    for row in range(1,height):
        updateScreenWolfram(field,row - 1)
        field = updateWolfram(row,field,cases)

    c = 1
    while c:
        for e in event.get():
            if e.type == QUIT:
                c = 0

if __name__ == "__main__":
    if (len(argv) < 2) or ((argv[1] == "wolfram") and (len(argv) != 3)):
        print "Usage: {} wolfram rule\n       {} conway".format(argv[0],argv[0])
        exit(0)
    
    window = initScreen()
    grid = window.copy()
    grid.set_colorkey(WHITE)

    blackCell = Surface((cellWidth,cellHeight))
    blackCell.fill(BLACK)
    whiteCell = Surface((cellWidth,cellHeight))
    whiteCell.fill(WHITE)
    
    if argv[1] == "wolfram":
        try: Wolfram(int(argv[2]))
        except:
            print "[-] rule must be int in range(256)"
            exit(0)
    elif argv[1] == "conway":
        Conway()
    else:
        print "[-] invalid mode"