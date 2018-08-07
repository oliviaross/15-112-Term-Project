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
