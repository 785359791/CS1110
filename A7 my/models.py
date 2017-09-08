# models.py
# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""Models module for Breakout

This module contains the model classes for the Breakout game. That is anything that you
interact with on the screen is model: the paddle, the ball, and any of the bricks.

Technically, just because something is a model does not mean there has to be a special 
class for it.  Unless you need something special, both paddle and individual bricks could
just be instances of GRectangle.  However, we do need something special: collision 
detection.  That is why we have custom classes.

You are free to add new models to this module.  You may wish to do this when you add
new features to your game.  If you are unsure about whether to make a new class or 
not, please ask on Piazza."""
import random # To randomly generate the ball velocity
from constants import *
from game2d import *


# PRIMARY RULE: Models are not allowed to access anything except the module constants.py.
# If you need extra information from Play, then it should be a parameter in your method, 
# and Play should pass it as a argument when it calls the method.


class Paddle(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball, as well as move it
    left and right.  You may wish to add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER TO CREATE A NEW PADDLE
    def __init__(self):
        """Initializer: Creates a new paddle.
        
        An instance is a subclass of GRectangle. The initializer calls
        the initializer of GRectangle with information provided in constants.py"""
        GRectangle.__init__(self,x=GAME_WIDTH/2.0,bottom=PADDLE_OFFSET,width=PADDLE_WIDTH,height=PADDLE_HEIGHT,fillcolor=colormodel.BLACK)
        
        
    # METHODS TO MOVE THE PADDLE AND CHECK FOR COLLISIONS
    def updatePaddle(self,input):
        """Animates the paddle.
        
        Parameter: input
        Precondition: input is an instance of GInput. """
        assert isinstance(input,GInput)
        if input.is_key_down('left'):
            self.x =max(self.x-5, PADDLE_WIDTH/2.0)
        elif input.is_key_down('right'):
           self.x =min(self.x+5, GAME_WIDTH-PADDLE_WIDTH/2.0)
    
    
    def collides(self,ball):
        """Returns True if the ball collides with the paddle.
        
        Parameter: ball, the ball to check
        Precondition: ball is of class Ball"""
        assert isinstance(ball,Ball)
        x=ball.x
        y=ball.y
        r=ball.width
        result=False
        if ball._vy<0:
            if self.contains(x-r,y-r):
                result=True
            elif self.contains(x+r,y-r):
                result=True
            return result
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Brick(GRectangle):
    """An instance is the game brick.
    
    This class contains a method to detect collision with the ball.  You may wish to 
    add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER TO CREATE A BRICK
    def __init__(self,x,y,c):
        """Initializer: Creates a brick.
        
        Note that this is a proper initializer, because Brick is a subclass
        of GRectange so it calls the initializer of GRectangel.
        However, since the position and color of the brick will vary in different rows and columns,
        it needs to know the the value of x, y and color. We pass them as arguments.
        
        Parameter x: The x coordinate of the brick
        Precondition: x is a float or an int.
        
        Parameter y: The y coordinate of the brick
        Precondition: y is a float or an int.
        
        Parameter c: The color of the brick
        Precondition: c is an instance of RGB.
        """
        assert type(x)==int or type(x)==float
        assert type(y)==int or type(y)==float
        assert isinstance(c,colormodel.RGB)
        GRectangle.__init__(self,x=x,y=y,width=BRICK_WIDTH,height=BRICK_HEIGHT,fillcolor=c,lincolor=c)
    
    
    # METHOD TO CHECK FOR COLLISION
    def collides(self,ball):
        """Returns: True if the ball collides with this brick
        
        Parameter ball: The ball to check
        Precondition: ball is of class Ball"""
        assert isinstance(ball,Ball)
        x=ball.x
        y=ball.y
        r=ball.width
        result=False
        if self.contains(x-r,y-r):
            result=True
        elif self.contains(x+r,y-r):
            result=True
        elif self.contains(x-r,y+r):
            result=True
        elif self.contains(x+r,y+r):
            result=True
        return result
        
        
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Ball(GEllipse):
    """Instance is a game ball.
    
    We extend GEllipse because a ball must have additional attributes for velocity.
    This class adds this attributes and manages them.
    
    INSTANCE ATTRIBUTES:
        _vx [int or float]: Velocity in x direction 
        _vy [int or float]: Velocity in y direction 
    
    The class Play will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with no
    setters for the velocities.
    
    How? The only time the ball can change velocities is if it hits an obstacle
    (paddle or brick) or if it hits a wall.  Why not just write methods for these
    instead of using setters?  This cuts down on the amount of code in Gameplay.
    
    NOTE: The ball does not have to be a GEllipse. It could be an instance
    of GImage (why?). This change is allowed, but you must modify the class
    header up above.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER TO SET RANDOM VELOCITY
    def __init__(self):
        """Initializer: Creates a ball.
        
        An instance is the subclass of GEllipse. It calls the initializer of GEllipse
        with the value offered in constants.py.
        In particular, it needs attributes _vx and _vy that keep track of the velocity.
        Therefore, we override the __init__ method in GEllipse.
        We choose component _vy randomly from 1.0 to 5.0; we start _vy with the value of -3.0.
        """
        GEllipse.__init__(self,width=BALL_DIAMETER,height=BALL_DIAMETER,fillcolor=colormodel.BLACK,x=GAME_WIDTH/2.0,y=GAME_HEIGHT/2.0)
        self._vx = random.uniform(1.0,5.0) 
        self._vx = self._vx * random.choice([-1, 1])
        self._vy = -3.0

    
    # METHODS TO MOVE AND/OR BOUNCE THE BALL
    def moveBall(self):
        """Moves the ball and handles the phsical law.
        
        Each time the new method is called, it should move the ball one step.
        To do this, we simply add the ball's velocity attributes to the ball's
        corresponding position coordinates.
        """
        self.x=self.x+self._vx
        self.y=self.y+self._vy
    
    def changeVy(self):
        """Change the vertical velocity of the ball.
        
        Whenever the ball collides with the paddle or the brick,
        the vertical component of velocity should change to its opposite value.
        """
        self._vy=-self._vy
        
    def changeVx(self):
        """Change the horizontal velocity of the ball.
        
        Whenever the ball collides with the walls,
        the horizontal component of velocity should change to its opposite value.
        """
        self._vx=-self._vx
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE