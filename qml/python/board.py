# -*- coding: utf-8 -*-

import os
import os.path
try:
    import pyotherside
except:
    print("no pyotherside module loaded")

import sgfparser
from game import Game

counter = 0

path = ""
cursor = None

def setPath(qtPath):
    global path
    path = qtPath

def loadBoard(filename):
    global cursor

    if os.path.isfile(filename):
        sgfPath = filename
    else:
        sgfPath = os.path.join(path,"../content","sgf",filename);
    pyotherside.send('log', sgfPath)
    try:
        f = open(sgfPath)
        s = f.read()
        f.close()
    except IOError:
        pyotherside.send('log', "Cannot open %s" % filename)
        return

    try:
        cursor = sgfparser.Cursor(s)
    except sgfparser.SGFError:
        pyotherside.send('log', 'Error in SGF file!')
        return
    pyotherside.send('log', 'File %s loaded' % filename)
    pyotherside.send('log', 'Found %d problems' % cursor.root.numChildren)
    return cursor.root.numChildren

def getGame(n):
    global cursor

    cursor.game(n)

    game = Game(cursor)
    game.normalize()
    #pyotherside.send('log', "Game loaded !!")

    return {
        "tree": game.tree,
        "size": game.get_size(),
        "side": game.side,
        "current_player": game.current_player,
    }
