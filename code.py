# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
score1 = 0
score2 = 0
player1 = '0'
player2 = '0'

paddle1_vel = [0,0]
paddle2_vel = [0,0]
pad1 = [[HALF_PAD_WIDTH, (HEIGHT/2) - HALF_PAD_HEIGHT], [HALF_PAD_WIDTH, (HEIGHT / 2) + HALF_PAD_HEIGHT]]
pad2 = [[WIDTH - HALF_PAD_WIDTH, (HEIGHT/2) - HALF_PAD_HEIGHT], [WIDTH - HALF_PAD_WIDTH, (HEIGHT/2) + HALF_PAD_HEIGHT]]               

LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new bal in middle of table
ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [2,0]


# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, x, y, ball_vel
    x = random.randrange(120, 240) / 60.0
    y = random.randrange(60, 180) / 60.0
    ball_pos = [WIDTH/2, HEIGHT/2]    
    if direction == RIGHT:
        ball_vel = [x,y]
    elif direction == LEFT:
        ball_vel = [-x, -y]
    return ball_pos, ball_vel
    
  
# define event handlers
def new_game(spawn_ball):
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, score1, score2 , player1, player2  # these are numbers
    score1 = 0
    score2 = 0
    player1 = str(score1)
    player2 = str(score2)
    spawn_ball(RIGHT)
            

def draw(canvas):
    global score1, score2, player1, player2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
            
    # draw ball
    canvas.draw_circle((ball_pos[0], ball_pos[1]), BALL_RADIUS, 10, "purple", "purple")
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    elif ball_pos[1] >= (HEIGHT - 1) - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    
    # update paddle's vertical position, keep paddle on the screen
    if pad1[0][1] < 0:
        pad1[0][1] = 0
        pad1[1][1] = PAD_HEIGHT 
    elif pad1[1][1] > HEIGHT - 1:
        pad1[0][1] = HEIGHT - PAD_HEIGHT 
        pad1[1][1] = HEIGHT - 1
    else:
        pad1[0][1] += paddle1_vel[1]    
        pad1[1][1] += paddle1_vel[1]
        
    if pad2[0][1] < 0:
        pad2[0][1] = 0
        pad2[1][1] = PAD_HEIGHT 
    elif pad2[1][1] > HEIGHT - 1:
        pad2[0][1] = HEIGHT - PAD_HEIGHT
        pad2[1][1] = HEIGHT - 1
    else:
        pad2[0][1] += paddle2_vel[1]    
        pad2[1][1] += paddle2_vel[1]
    
    # draw paddles
    canvas.draw_line(pad1[0],pad1[1], PAD_WIDTH, "blue")
    canvas.draw_line(pad2[0],pad2[1], PAD_WIDTH, "green")
    
    # determine whether paddle and ball collide
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if ball_pos[1] >= pad1[0][1] and ball_pos[1] <= pad1[1][1]:
            ball_vel[0] = ball_vel[0] + (ball_vel[0])//100
            ball_vel[0] = - ball_vel[0]
           
        else:
            score2 += 1
            player2 = str(score2)
            spawn_ball(LEFT)
            
                
    if ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH:
        if ball_pos[1] >= pad2[0][1] and ball_pos[1] <= pad2[1][1]:
            ball_vel[0] = ball_vel[0] + (ball_vel[0])//100
            ball_vel[0] = - ball_vel[0]

        else:
            score1 += 1
            player1 = str(score1)
            spawn_ball(RIGHT)
            
    
    # draw scores
    canvas.draw_text(player1,(150, 70), 40, "yellow", "serif")
    canvas.draw_text(player2,(450, 70), 40, "red", "serif")
    

def keydown(key):
    global acc, paddle1_vel, paddle2_vel
    acc = [0, 3]
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel[1] -= acc[1]
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel[1] += acc[1]
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel[1] -= acc[1]
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel[1] += acc[1]
    
    return paddle1_vel, paddle2_vel, acc
   
def keyup(key):
    acc = [0, 3]
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel[1] += acc[1]
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel[1] -= acc[1]
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel[1] += acc[1]
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel[1] -= acc[1]

def button_handler():
    new_game(spawn_ball)
        
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
button1 = frame.add_button('Restart', button_handler)


# start frame
new_game(spawn_ball)
frame.start()
