#################################################################
# 15-112-n18 Term Project
# Your Name: Olivia Ross
# Your Andrew ID: oross
# Your Section: A
#################################################################

from tkinter import *
import math

def getDistance(x1, y1, x2, y2):
    return ((((x2-x1))**2)+((y2-y1)**2))**(1/2)

####################################
# Player class
####################################

class Player(object):
    def __init__(self, cx, cy, color):
        self.birthData = (cx, cy, color)

        self.cx = cx
        self.cy = cy
        self.color = color

        self.bulk = 32
        self.power = 2
        self.speed = self.bulk//4
        self.health = 30

        self.masked = False
        self.maskTimer = 10
        
    def __repr__(self):
        return "The %s warrior stands tall at (%d, %d)." % (self.color, self.cx, self.cy)

    def getPosition(self):
        return (self.cx, self.cy)

    def draw(self, canvas):
        cx, cy, r = self.cx, self.cy, self.bulk
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill=self.color)

    def move(self, direction):
        dx, dy = direction
        self.cx += dx * self.speed
        self.cy += dy * self.speed
        
    def isTouchingOther(self, other):
        cx, cy, radius = self.cx, self.cy, self.bulk
        if (getDistance(cx, cy, other.cx, other.cy) <= 
                                    (radius + other.bulk)):
            if isinstance(other, Mask): self.putOnMask(other)
            return other

    def attack(self, other):
        if isinstance(self.isTouchingOther(other), Player):
            other.reactToAttack(self)

    def reactToAttack(self, other):
        if isinstance(self.isTouchingOther(other), Player):
            self.health -= other.power
            print("health decreased by ", other.power)

    def putOnMask(self, mask):
        if isinstance(mask, Mask):
            self.bulk = mask.bulk
            self.power = mask.power
            self.health = mask.health
            self.speed = mask.speed

    def returnToNormal(self):
        cx, cy, color = self.birthData
        self.__init__(cx, cy, color)

    def onTimerFired(self):
        if self.masked:
            self.maskTimer -= 1

            if self.maskTimer <= 0:
                self.returnToNormal()

####################################
# Mask class
####################################
class Mask(object):
    def __init__(spirit):
        self.spirit = spirit

        self.cx = None
        self.cy = None
        self.color = "black"

        self.bulk = 10
        self.power = 2
        self.speed = 5
        self.health = 30
        self.altitude = 8

        if spirit == "Rabbit":
            #speed boost
            self.speed *= 5
            self.color = "pink"
        elif spirit == "Frog":
            #jump height boost
            self.altitude *= 5
            self.color = "green"
        elif spirit == "Bear":
            #bulk boost
            self.bulk *= 5
            self.color = "brown"
        elif spirit == "Turtle":
            #health increase
            self.health *= 5
            self.color = "green2"
        elif spirit == "Ape":
            #power increase
            self.power *= 5
            self.color = "red"

    def placeMaskInWorld(self, data):
        self.cy = random.randint(self.bulk, data.width)
        self.cy = random.randint(self.bulk, data.height)

    def speak(canvas):
        canvas.create_text(self.cx, self.cy+20, 
            "I am the %s spirit of this Mask." % self.spirit, font="Arial 20")

        return "I am the %s spirit of this Mask." % self.spirit

    def draw(self, canvas):
        if self.cx != None and self.cy != None:
            canvas.create_rectangle(self.cx-self.bulk, self.cy-self.bulk,
                    self.cx+self.bulk, self.cy+self.bulk, fill=self.color)

####################################
# Level class
####################################
class Level(object):
    def __init__(self):
        self.data = [
            [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False,  True,  True,  True, False, False, False, False, False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
            [ True,  True,  True,  True,  True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True,  True,  True,  True,  True],
            [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
            [ True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True]
        ]

        self.rows = len(self.data)
        self.cols = len(self.data[0])

        self.cellHeight = 600//self.rows
        self.cellWidth = 1200//self.cols


    def draw(self, canvas, height, width):
        canvas.create_rectangle(0, 0, width, height, fill="lightblue")

        for row in range(self.rows):
            for col in range(self.cols):
                if self.data[row][col] == True:
                    x0, y0 = self.cellWidth*col, self.cellHeight*row
                    x1, y1 = x0 + self.cellWidth, y0 + self.cellHeight
                    canvas.create_rectangle(x0, y0, x1, y1, fill="darkgreen")

    def cornerInRectangle(self, corner, rectangle):
        cornerX, cornerY = corner
        rectX0, rectY0, rectX1, rectY1 = rectangle

        if (rectX0 < cornerX < rectX1) and (rectY0 < cornerY < rectY1):
            return True

        return False


    def detectActiveLayerCollision(self, player):
        if not isinstance(player, Player): return
        cx, cy, r = player.cx, player.cy, player.bulk
        for row in range(self.rows):
            for col in range(self.cols):
                if self.data[row][col] == True: ## actual ground and stuff
                    x0, y0 = self.cellWidth*col, self.cellHeight*row
                    x1, y1 = x0 + self.cellWidth, y0 + self.cellHeight
                    rectangle = (x0, y0, x1, y1)
                    circleRect = (cx-r, cy-r, cx+r, cy+r)
                    if (self.cornerInRectangle((cx-r, cy-r), rectangle) or 
                        self.cornerInRectangle((cx+r, cy-r), rectangle) or
                        self.cornerInRectangle((cx-r, cy+r), rectangle) or
                        self.cornerInRectangle((cx+r, cy+r), rectangle) or
                        self.cornerInRectangle((x0, y0), circleRect) or
                        self.cornerInRectangle((x0, y1), circleRect) or
                        self.cornerInRectangle((x1, y0), circleRect) or
                        self.cornerInRectangle((x1, y1), circleRect)):
                        return True

        return False

####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    data.level = Level()
    data.playerOne = Player(32, (data.height - data.height//12) - 32, "red")
    data.playerTwo = Player(data.width - 32, (data.height - data.height//12) - 32,"purple")
    data.frogMask = Mask("Frog")

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    print(event.keysym)
    # PLAYER ONE CONTROLS
    if event.keysym == "Left":
        data.playerOne.move((-1, 0))
        if data.level.detectActiveLayerCollision(data.playerOne):
            print("Collision! Movement disabled!")
            data.playerOne.move(( 1, 0))
    elif event.keysym == "Right":
        data.playerOne.move(( 1, 0))
        if data.level.detectActiveLayerCollision(data.playerOne):
            print("Collision! Movement disabled!")
            data.playerOne.move((-1, 0))
    elif event.keysym == "Up":
        data.playerOne.move((0, -1))
        if data.level.detectActiveLayerCollision(data.playerOne):
            print("Collision! Movement disabled!")
            data.playerOne.move((0,  1))
    elif event.keysym == "Down":
        data.playerOne.move((0,  1))
        if data.level.detectActiveLayerCollision(data.playerOne):
            print("Collision! Movement disabled!")
            data.playerOne.move((0, -1))

    if event.keysym == "Shift_L":
        data.playerOne.attack(data.playerTwo)
        print("playerOne attacked!")
        print("P2: health decreased to ", data.playerTwo.health)

    # PLAYER TWO CONTROLS
    if event.keysym == "w":
        data.playerTwo.move((0, -1))
        if data.level.detectActiveLayerCollision(data.playerTwo):
            print("Collision! Movement disabled!")
            data.playerOne.move((0,  1))
    elif event.keysym == "s":
        data.playerTwo.move((0,  1))
        if data.level.detectActiveLayerCollision(data.playerTwo):
            print("Collision! Movement disabled!")
            data.playerTwo.move((0, -1))
    elif event.keysym == "a":
        data.playerTwo.move((-1, 0))
        if data.level.detectActiveLayerCollision(data.playerTwo):
            print("Collision! Movement disabled!")
            data.playerTwo.move(( 1, 0))
    elif event.keysym == "d":
        data.playerTwo.move(( 1, 0))
        if data.level.detectActiveLayerCollision(data.playerTwo):
            print("Collision! Movement disabled!")
            data.playerTwo.move((-1, 0))
    if event.char == "e":
        data.playerTwo.attack(data.playerOne)
        print("playerTwo attacked!")
        print("P1: health decreased to ", data.playerOne.health)


def timerFired(data):
    # update game data once every tick
    pass

def redrawAll(canvas, data):
    data.level.draw(canvas, data.height, data.width)
    data.playerOne.draw(canvas)
    data.playerTwo.draw(canvas)

    canvas.create_text(data.width//4, data.height//12, text="P1 HP: %d" % 
                                    data.playerOne.health, font="Arial 20")
    canvas.create_text(3*data.width//4, data.height//12, text="P2 HP: %d" % 
                                    data.playerTwo.health, font="Arial 20")

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
