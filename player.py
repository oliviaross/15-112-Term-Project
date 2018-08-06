####################################
# Player class
####################################
import math

def getDistance(x1, y1, x2, y2):
    return math.sqrt(((x2-x1)**2)+((y2-y1)**2))

class Player(object):
    def __init__(self, cx, cy, color):
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
        
    def __repr__(self):
        return "The %s warrior stands tall at (%d, %d)." % (self.color, self.cx, self.cy)

    def getPosition(self):
        return (self.cx, self.cy)

    def draw(self, canvas):
        cx, cy, r = self.cx, self.cy, self.bulk
        canvas.create_oval(cx-r, cy-r, cx+r, cx-r, fill=self.color)

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

testPlayerClass()