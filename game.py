#################################################################
# 15-112-n18 Term Project
# Your Name: Olivia Ross
# Your Andrew ID: oross
# Your Section: A
#################################################################

from tkinter import *
import math
import random

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
        self.speed = self.bulk*2
        self.health = 30

        self.mask = None
        self.maskTimer = 70
        
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
        if other.cx == None: return None #handle mask case

        cx, cy, radius = self.cx, self.cy, self.bulk
        if (getDistance(cx, cy, other.cx, other.cy) <= 
                                    (radius + other.bulk)):
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
            if self.mask == None:
                if mask.bulk != None and mask.spirit == "Bear": self.bulk += mask.bulk
                if mask.power != None: self.power *= mask.power
                if mask.health != None: self.health *= mask.health
                if mask.speed != None: self.speed *= mask.speed

                self.mask = mask

    def returnToNormal(self):
        self.__init__(self.cx, self.cy, self.color)

    def onTimerFired(self, data):
        for mask in data.maskList:
            if isinstance(self.isTouchingOther(mask), Mask): 
                self.putOnMask(mask)
                mask.reactToPlayer()

        if self.mask != None:
            self.maskTimer -= 1

            if self.maskTimer <= 0:
                data.maskList.pop(data.maskList.index(self.mask))
                self.returnToNormal()



####################################
# Mask class
####################################
class Mask(object):
    def __init__(self, spirit):
        self.spirit = spirit

        self.cx = None
        self.cy = None
        self.color = "black"

        self.bulk = 32
        self.power = None
        self.speed = None
        self.health = None
        self.altitude = None

        if spirit == "Rabbit":
            #speed boost
            self.speed = 3
            self.color = "pink"
        elif spirit == "Frog":
            #jump height boost
            self.altitude = 5
            self.color = "green"
        elif spirit == "Bear":
            #bulk boost
            self.bulk = 32
            self.color = "brown"
        elif spirit == "Turtle":
            #health increase
            self.health = 5
            self.color = "green2"
        elif spirit == "Ape":
            #power increase
            self.power = 5
            self.color = "red"

    def placeMaskInWorld(self, data): ###!
        canPlace = False

        self.cx = random.randint(int(self.bulk), int(data.width))
        self.cy = random.randint(int(self.bulk), int(data.height))

        while not canPlace:
            for row in range(data.level.rows):
                for col in range(data.level.cols):
                    if self.cx//data.level.cellWidth == col and self.cy//data.level.cellHeight == row:
                        self.cx = random.randint(int(self.bulk), int(data.width))
                        self.cy = random.randint(int(self.bulk), int(data.height))
                    else: 
                        canPlace = True

    def speak(self, canvas):
        canvas.create_text(self.cx, self.cy+20, 
            text="I am the %s spirit of this Mask." % self.spirit, font="Arial 20")

    def reactToPlayer(self):
        self.color = "black"

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
        
    data.maskList = []
    data.maskList.append(Mask("Ape"))
    data.maskList[0].placeMaskInWorld(data)

    data.gameTimer = 0

def mousePressed(event, data):
    # use event.x and event.y
    spiritList = ["Ape", "Frog", "Rabbit", "Turtle", "Bear"]
    data.maskList.append(Mask(random.choice(spiritList)))

    for mask in data.maskList:
        mask.placeMaskInWorld(data)

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
    elif event.keysym == "Up": #should be jumping animation
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
    if event.keysym == "w": #should be jumping animation
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
    data.gameTimer += 1

    while(data.gameTimer <= 600):
    # update game data once every tick
       data.playerOne.onTimerFired(data)
       data.playerTwo.onTimerFired(data)

def redrawAll(canvas, data):
    while(data.gameTimer <= 600):
        data.level.draw(canvas, data.height, data.width)
        data.playerOne.draw(canvas)
        data.playerTwo.draw(canvas)

        for mask in data.maskList:
            mask.draw(canvas)
            mask.speak(canvas)

        canvas.create_text(data.width//4, data.height//12, text="P1 HP: %d" % 
                                        data.playerOne.health, font="Arial 20")
        canvas.create_text(3*data.width//4, data.height//12, text="P2 HP: %d" % 
                                        data.playerTwo.health, font="Arial 20")
    else: 
        if data.playerOne.health > data.playerTwo.health:
            canvas.create_text(data.width//2, data.height//2, 
                text="Player one wins!", font="Arial 20")

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
