# play.py
# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""Subcontroller module for Breakout

This module contains the subcontroller to manage a single game in the Breakout App. 
Instances of Play represent a single game.  If you want to restart a new game, you are 
expected to make a new instance of Play.

The subcontroller Play manages the paddle, ball, and bricks.  These are model objects.  
Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer."""
from constants import *
from game2d import *
from models import *


# PRIMARY RULE: Play can only access attributes in models.py via getters/setters
# Play is NOT allowed to access anything in breakout.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)

class Play(object):
    """An instance controls a single game of breakout.
    
    This subcontroller has a reference to the ball, paddle, and bricks. It animates the 
    ball, removing any bricks as necessary.  When the game is won, it stops animating.  
    You should create a NEW instance of Play (in Breakout) if you want to make a new game.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See 
    subcontrollers.py from Lecture 25 for an example.
    
    INSTANCE ATTRIBUTES:
        _paddle [Paddle]: the paddle to play with 
        _bricks [list of Brick]: the list of bricks still remaining 
        _ball   [Ball, or None if waiting for a serve]:  the ball to animate
        _tries  [int >= 0]: the number of tries left 
    
    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Breakout. It is okay if you do, but you MAY NOT ACCESS 
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that 
    you need to access in Breakout.  Only add the getters and setters that you need for 
    Breakout.
    
    You may change any of the attributes above as you see fit. For example, you may want
    to add new objects on the screen (e.g power-ups).  If you make changes, please list
    the changes with the invariants.
                  
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getBricks(self):
        """Returns: the list of Bricks still remaining."""
        return self._bricks
    
    
    def getPaddle(self):
        """Returns: the paddle to paly with."""
        return self._paddle
    
    
    def getBall(self):
        """Returns: the ball to animate."""
        return self._ball
    
    
    def getTries(self):
        """Returns: the number of tries left."""
        return self._tries
    
    # INITIALIZER (standard form) TO CREATE PADDLES AND BRICKS
    def __init__(self):
        """Initializes paddle and the list of bricks."""
        self._paddle=Paddle()
        self._bricks=[]
        self._ball=Ball()
        x=BRICK_SEP_H/2.0+BRICK_WIDTH/2.0
        y=GAME_HEIGHT-BRICK_Y_OFFSET-BRICK_HEIGHT/2.0
        for i in range(0,BRICK_ROWS):
            c=BRICK_COLORS[i/2]
            for j in range(0,BRICKS_IN_ROW):
                brick=Brick(x,y,c)
                self._bricks.append(brick)
                x=x+(BRICK_WIDTH+BRICK_SEP_H)
            x=BRICK_SEP_H/2.0+BRICK_WIDTH/2.0
            y=y-(BRICK_HEIGHT+BRICK_SEP_V)
        self._tries=3
        
            
    
    # UPDATE METHODS TO MOVE PADDLE, SERVE AND MOVE THE BALL
    def updatePaddle(self,input):
        """Uses left/right key to move paddle.
        
        Parameter: input
        Precondition: input is an instance of GInput."""
        assert isinstance(input, GInput)
        self._paddle.updatePaddle(input)
    
    
    def serveBall(self):
        """Serves the ball."""
        self._ball=Ball()
        
        
    def updateBall(self):
        """Updates the ball.
        
        Moves the ball and calls helper-function to handle the situation
        if the ball collides with the wall, the paddle or the bricks.
        """
        self._ball.moveBall()
        self.bounceWall()
        self.bouncePaddle()
        self.bounceBricks()    
    
        
    # DRAW METHOD TO DRAW THE PADDLES, BALL, AND BRICKS
    def draw(self,view):
        """Draws the paddle, ball and bricks.
        
        Parameter: view
        Precondition: view is an instance of GView.
        """
        assert isinstance(view,GView)
        for brick in self._bricks:
            brick.draw(view)
        self._paddle.draw(view)
        self._ball.draw(view)
        
        
    # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION
    def bounceWall(self):
        """Handles the situtaion when the ball collides with the walls.
        
        Changes the vertical velocity to the opposite if the ball collides with the top wall;
        changes the horizontal velocity to the opposite if the ball collides with the left and right walls.
        """
        if self._ball.top>=GAME_HEIGHT:
            self._ball.changeVy()
        elif self._ball.right>=GAME_WIDTH:
            self._ball.changeVx()
        elif self._ball.left<=0:
            self._ball.changeVx()
        
            
    def bouncePaddle(self):
        """Handles the situation when the ball collides with the paddle.
        
        Changes the vertical velocity to the opposite if the ball collides with the paddle.
        """
        if self._paddle.collides(self._ball):
            self._ball.changeVy()
            
            
    def bounceBricks(self):
        """Handles the situation when the ball collides with the brick.
        
        Changes the vertical velocity to the opposite if the ball collides with the brick;
        removes the brick from the list of bricks if the ball has collided with it.
        """
        for brick in self._bricks:
            if brick.collides(self._ball):
                self._ball.changeVy()
                self._bricks.remove(brick)
                
                
    # ADD ANY ADDITIONAL METHODS (FULLY SPECIFIED) HERE
    def reduceTries(self):
        self._tries=self._tries-1
