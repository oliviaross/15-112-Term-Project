#################################################################
# 15-112-n18 Term Project
# Your Name: Olivia Ross
# Your Andrew ID: oross
# Your Section: A
#################################################################

from tkinter import *
import math

#Import game classes
from level import *
from player import *
from mask import *

"""
TO DO:
    - Level logic
        - Player should not be able to walk through floors, 
            walls, blocks, etc.
"""

####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    Player(0, 0, None).testPlayerClass(data)
    Mask(None).testMaskClass(dsta)

    level1 = Level()

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    pass
def timerFired(data):
    # update game data once every tick
    pass

def redrawAll(canvas, data):
    # draw stuff
    pass

#################################################################
# use the run function as-is
#################################################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
   
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("Closing window....bye!")

run(1200, 600)
