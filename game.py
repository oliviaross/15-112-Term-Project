#################################################################
# 15-112-n18 Term Project
# Your Name: Olivia Ross
# Your Andrew ID: oross
# Your Section: A
#################################################################

from tkinter import *

def getDistance(x1, y1, x2, y2):
    return math.sqrt(((x2-x1)**2)+((y2-y1)**2))

class Player(object):
	def __init__(cx, cy, color):
		self.birthData = (cx, cy, color)

		self.cx = cx
		self.cy = cy
		self.color = color

		self.bulk = 10
		self.power = 2
		self.speed = 5
		self.health = 30

		self.masked = False
		self.maskTimer = 10

	def draw(self, canvas):
		cx, cy, r = self.cx, self.cy, self.bulk
		canvas.create_oval(cx-r, cy-r, cx+r, cx-r, fill=self.color)

	def move(self, direction):
		dx, dy = direction

		self.cx += dx * self.speed
		self.cy += dx * self.speed

	def isTouchingOther(self, other):
		cx, cy, radius = self.cx, self.cy, self.bulk
		if (getDistance(cx, cy, other.cx, other.cy) <= 
									(radius + other.radius)):
			if isinstance(other, Mask): self.putOnMask(other)
			return other

	def attackOther(self, other):
		if isinstance(self.isTouchingOther(other), Player):
			other.reactToAttack()

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
		__init__(self.birthData)

	def onTimerFired(self):
		if self.masked:
			self.maskTimer -= 1

			if self.maskTimer <= 0:
				self.returnToNormal()

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

		if spirit = "Rabbit":
			#speed boost
			self.speed *= 5
			self.color = "pink"
		elif spirit = "Frog":
			#jump height boost
			self.altitude *= 5
			self.color = "green"
		elif spirit = "Bear":
			#bulk boost
			self.bulk *= 5
			self.color = "brown"
		elif spirit = "Turtle":
			#health increase
			self.health *= 5
			self.color = "green2"
		elif spirit = "Ape":
			#power increase
			self.power *= 5
			self.color = "red"

	def placeMaskInWorld(self, data)
		self.cy = random.randint(self.bulk, data.width)
		self.cy = random.randint(self.bulk, data.height)

	def speak(canvas):
		canvas.create_text(self.cx, self.cy+20, 
			"I am the %s spirit of this Mask." % self.spirit, font="Arial 20")

	def draw(self, canvas):
		if self.cx != None and self.cy != None:
			canvas.create_rectangle(self.cx-self.bulk, self.cy-self.bulk
					self.cx+self.bulk, self.cy+self.bulk, fill=self.color)
	
####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    pass

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
