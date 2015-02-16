#Pong

# Implementation of classic arcade game Pong

###############################################
#Import libraries

import simplegui
import random

###############################################
# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
X = 0
Y = 1
P1_START = True
Paddle_Vel = 5

#Player 1
P1_Score = 0
paddle1_pos = [0+PAD_WIDTH, HEIGHT//2]
paddle1_vel = [0,0]

#Player 2
P2_Score = 0
paddle2_pos = [WIDTH-PAD_WIDTH, HEIGHT//2]
paddle2_vel = [0,0]

# Ball positioning and velocity
ball_pos = [WIDTH//2, HEIGHT//2]

ball_vel = [0.0,0.0]


###############################################
# helper function to start and restart the game

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
 
    v_mult = -1
    if direction:
        v_mult = 1
   
    ball_pos = [WIDTH//2, HEIGHT//2]
    #create 
    ball_vel = [(random.randrange(120,240)/60)*v_mult,(random.randrange(60,180)/-60)]

def check_score():
    """See if the ball has gone into the gutter, or into a paddle"""
    global P1_START, P1_Score, P2_Score
    
    if ball_pos[X] < WIDTH//2 :
        if ball_pos[Y] >= paddle1_pos[Y]- HALF_PAD_HEIGHT and ball_pos[Y] <= paddle1_pos[Y] + HALF_PAD_HEIGHT:
            #Struck the player 2 paddle
            ball_vel[X] = - (ball_vel[X] + ball_vel[X]*0.1)
            ball_vel[Y] =  (ball_vel[Y] + ball_vel[Y]*0.1)
        else:
            P2_Score += 1
            P1_START = True
            spawn_ball(P1_START)
    else:
        if ball_pos[Y] >= paddle2_pos[Y]- HALF_PAD_HEIGHT and ball_pos[Y] <= paddle2_pos[Y] + HALF_PAD_HEIGHT:
            ball_vel[X] = - (ball_vel[X] + ball_vel[X]*0.1)
            ball_vel[Y] =  (ball_vel[Y] + ball_vel[Y]*0.1)
        else:
            P1_Score += 1
            P1_START = False
            spawn_ball(P1_START)
        
    
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global P1_Score, P2_Score  # these are ints
    P1_START = True
    P1_Score = 0
    P2_Score = 0
   
    paddle1_pos = [0+PAD_WIDTH, HEIGHT//2]
    paddle2_pos = [WIDTH-PAD_WIDTH, HEIGHT//2]
    
    spawn_ball(P1_START)

###############################################
# define event handlers

        
def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
        
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
              
    # Update ball position
    ball_pos[X] += ball_vel[X]
    ball_pos[Y] += ball_vel[Y]
    
    #Check for collisions, change dirrection if occurs.
    if (ball_pos[Y] <= BALL_RADIUS or ball_pos[Y] >= HEIGHT-BALL_RADIUS):
        ball_vel[Y] = - ball_vel[Y]
    # Check for ball in gutter
    if (ball_pos[X] <= (BALL_RADIUS+PAD_WIDTH) or ball_pos[X] >= WIDTH-(BALL_RADIUS+PAD_WIDTH)):
        check_score()
    
    # draw ball
    c.draw_circle(ball_pos,BALL_RADIUS,2,"White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos[Y] + paddle1_vel[Y] - HALF_PAD_HEIGHT > 0 and paddle1_pos[Y] + paddle1_vel[Y] + HALF_PAD_HEIGHT < HEIGHT:
        paddle1_pos[Y] += paddle1_vel[Y]
    else:
        #If velocity is faster than 1 I still want to be able to go to the end
        if paddle1_vel[Y]/abs(paddle1_vel[Y]) == -1:
            paddle1_pos[Y] = 0 + 1 + HALF_PAD_HEIGHT
        else:
            paddle1_pos[Y] = HEIGHT - 1 - HALF_PAD_HEIGHT
            
    if paddle2_pos[Y] + paddle2_vel[Y] - HALF_PAD_HEIGHT > 0 and  paddle2_pos[Y] + paddle2_vel[Y] + HALF_PAD_HEIGHT < HEIGHT:
        paddle2_pos[Y] += paddle2_vel[Y]
    else:
        #If velocity is faster than 1 I still want to be able to go to the end
        if paddle2_vel[Y]/abs(paddle2_vel[Y]) == -1:
            paddle2_pos[Y] = 0 + 1 + HALF_PAD_HEIGHT
        else:
            paddle2_pos[Y] = HEIGHT - 1 - HALF_PAD_HEIGHT
    
    # draw paddles
    c.draw_line([paddle2_pos[X]+PAD_WIDTH//2,paddle2_pos[Y]-PAD_HEIGHT//2], 
                [paddle2_pos[X]+PAD_WIDTH//2,paddle2_pos[Y]+PAD_HEIGHT//2],
                PAD_WIDTH, "WHITE")
    c.draw_line([paddle1_pos[X]-HALF_PAD_WIDTH,paddle1_pos[Y]-PAD_HEIGHT//2], 
                [paddle1_pos[X]-HALF_PAD_WIDTH,paddle1_pos[Y]+PAD_HEIGHT//2],
                PAD_WIDTH, "WHITE")
    
    # draw scores
    c.draw_text(str(P1_Score), [WIDTH//2 - 70,50], 36, "White")
    c.draw_text(str(P2_Score), [WIDTH//2 + 50,50], 36, "White")
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    # Key handlers for arrows
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel[Y] -= Paddle_Vel
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel[Y] += Paddle_Vel
    
    #Key Handlers for w,s 
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel[Y] -= Paddle_Vel
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel[Y] += Paddle_Vel
    
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    # Key handlers for arrows
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel[Y] += Paddle_Vel
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel[Y] -= Paddle_Vel
    
    #Key Handlers for w,s 
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel[Y] += Paddle_Vel
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel[Y] -= Paddle_Vel
        
    
def tick():
    pass

def reset_button():
    new_game()
    
        

###############################################
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)

###############################################
# register event handlers for control elements
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
timer = simplegui.create_timer(1000,tick)
frame.add_button("Restart", reset_button)
###############################################
# start frame
new_game()
frame.start()
timer.start()
