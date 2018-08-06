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

    def draw(self, canvas):
        if self.cx != None and self.cy != None:
            canvas.create_rectangle(self.cx-self.bulk, self.cy-self.bulk,
                    self.cx+self.bulk, self.cy+self.bulk, fill=self.color)