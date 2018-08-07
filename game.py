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
        self.speed = self.bulk//2
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
# Testing player class
####################################

def testPlayerClass(data):
    print("Testing Player class...", end="")
    local_cx, local_cy = (data.width//2, data.height//2)

    # A player is initialized with a location and color to indentify it. 
    player1 = Player(local_cx, local_cy, "red")
    assert(type(player1) == Player)
    assert(isinstance(player1, Player))

    # Check to see that we indeed have the player where it was placed. 
    assert(str(player1) == ("The %s warrior stands tall at (%d, %d)." % (player1.color, local_cx, local_cy)))
    assert(str([player1]) == ("[The %s warrior stands tall at (%d, %d).]" % (player1.color, local_cx, local_cy)))
   
    # The move() function takes a unit direction and multiplies the vector by a speed
    # scalar to get the length of the vector traveled

    player1.move((0, 1))
    local_cx += 0*player1.speed
    local_cy += 1*player1.speed

    assert(player1.getPosition() == (local_cx, local_cy))

    # Time to test interactions with other players:
    local_cx, local_cy = (data.width//2, data.height//2)
    player2 = Player(local_cx, local_cy, "purple")
    assert(type(player2) == Player)
    assert(isinstance(player2, Player))

    # All players begin with a radius/bulk of ten. With no x-distance 
    # and a vertical distance of 5, the two players should be 
    # colliding right now. Let's check their interactions. 

    player2.move((0, -1)) # move player2 to the center of the screen
    assert(player1.isTouchingOther(player2) == player2)

    # Let's move player2 even farther away from player1, to check that they 
    # know when they don't collide. 

    player2.move((0, -1))
    player2.move((0, -1))
    player2.move((0, -1))
    player2.move((0, -1))

    assert(player1.isTouchingOther(player2) == None)

    # Now to test their fighting abilites. When one player attacks another, 
    # the other should react to the attack. 

    player2.move((0, 1))
    player2.move((0, 1))
    player2.move((0, 1))
    player2.move((0, 1)) # moves player2 back to original position

    assert(player1.isTouchingOther(player2) == player2)

    local_health = player1.health
    local_power = player2.power
    dhealth = local_health - local_power # local calculation of damage

    player2.attack(player1)

    assert(player1.health == dhealth)

    # Just for fun, let's test the returnToNormal function call to see if 
    # it actually works. 

    local_cx, local_cy = (data.width//2, data.height//2)

    player1.returnToNormal()
    player2.returnToNormal()

    assert(player1.getPosition() == (local_cx, local_cy))
    assert(player2.getPosition() == (local_cx, local_cy))

    assert(player1.isTouchingOther(player2) == player2)
    assert(player2.isTouchingOther(player1) == player1)

    print("Done!")

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
# Testing mask class
####################################

def testMaskClass():

    testPlayer = Player(0, 0, "black")

    #Try putting on the rabbit Mask
    assert(Mask("Rabbit").speak() == "I am the Rabbit spirit of this Mask.")
    
    testPlayer.putOnMask(Mask("Rabbit"))

    frogMask = Mask("Frog")
    bearMask = Mask("Bear")
    turtleMask = Mask("Turtle")
    apeMask = Mask("Ape")


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

    def detectActiveLayerCollision(self, player):
        if not isinstance(player, Player): return
        for row in range(self.rows):
            for col in range(self.cols):
                if self.data[row][col] == True: ## actual ground and stuff
                    x0, y0 = self.cellWidth*col, self.cellHeight*row
                    x1, y1 = x0 + self.cellWidth, y0 + self.cellHeight
                    if ((x0 < player.cx - player.bulk) and (player.cx + player.bulk < x1)
                         and (y0 < player.cy < y1)):
                        print(x0, player.cx, x1) 
                        print(y0, player.cx, x1)
                        return True
        return False


####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    data.level = Level()
    data.player = Player(32, (data.height - data.height//12) - 35, "red")

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    if event.char == "t":
        print(data.level.detectActiveLayerCollision(data.player))

    if event.keysym == "Left":
        data.player.move((-1, 0))
        if data.level.detectActiveLayerCollision(data.player):
            print("Collision! Movement disabled!")
            data.player.move(( 1, 0))

    elif event.keysym == "Right":
        data.player.move(( 1, 0))
        if data.level.detectActiveLayerCollision(data.player):
            print("Collision! Movement disabled!")
            data.player.move((-1, 0))

    elif event.keysym == "Up":
        data.player.move((0, -1))
        if data.level.detectActiveLayerCollision(data.player):
            print("Collision! Movement disabled!")
            data.player.move((0, 1))

def timerFired(data):
    # update game data once every tick
    pass

def redrawAll(canvas, data):
    data.level.draw(canvas, data.height, data.width)
    data.player.draw(canvas)

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
