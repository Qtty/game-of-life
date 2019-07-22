#!/usr/bin/python

from pygame import init,display,image,event,key,Surface
from pygame.locals import *
from game import *
from constants import *
from sys import argv
from time import sleep
from json import loads,dumps

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

def updateScreenConway(field):
    
    for i in range(height / cellHeight):
        for j in range(width / cellWidth):
            if field[i][j]: window.blit(blackCell,(j * cellWidth,i * cellHeight))
            else: window.blit(whiteCell,(j * cellWidth,i * cellHeight))
    window.blit(grid,(0,0))
    display.flip()

def Conway():
    field = initConway(width / cellWidth,height / cellHeight)
    with open("forms","r") as f:
        d = loads(f.read())
    c = 1
    x = 0
    while c:
        for e in event.get():
            if e.type == QUIT:
                c = 0
            elif e.type == MOUSEBUTTONDOWN:
                field[e.pos[1] / cellHeight][e.pos[0] / cellWidth] = 1 - field[e.pos[1] / cellHeight][e.pos[0] / cellWidth]
                if field[e.pos[1] / cellHeight][e.pos[0] / cellWidth]: window.blit(blackCell,(e.pos[0] - e.pos[0] % cellWidth,e.pos[1] - e.pos[1] % cellHeight))
                else: window.blit(whiteCell,(e.pos[0] - e.pos[0] % cellWidth,e.pos[1] - e.pos[1] % cellHeight))
                display.flip()
            elif e.type == KEYDOWN:
                if e.key == K_RETURN:
                    x = 1 - x
                elif e.key == K_g:
                    for i in d["glider"]:
                        field[i[1]][i[0]] = 1
                        window.blit(blackCell,(i[0] * cellWidth,i[1] * cellHeight))
                    display.flip()
                elif e.key == K_r:
                    window.fill(WHITE)
                    window.blit(grid,(0,0))
                    field = [[0 for j in range(width / cellWidth)] for i in range(height / cellHeight)]
                    x = 0
                    display.flip()
        if x:
            field = updateConway(field,width / cellWidth,height / cellHeight)
            updateScreenConway(field)
            #sleep(0.01)

def Wolfram():
    field,cases = initWolfram(int(argv[1]),width/cellWidth)
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

window = initScreen()
grid = window.copy()
grid.set_colorkey(WHITE)

blackCell = Surface((cellWidth,cellHeight))
blackCell.fill(BLACK)
whiteCell = Surface((cellWidth,cellHeight))
whiteCell.fill(WHITE)

Conway()