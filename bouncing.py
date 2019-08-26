'''
bouncing.py
simulates a gas
'''

from visual import *
from visual.graph import *
from random import *

#create a box that has walls and a floor and a ceiling
side = 4.0          #length of a side
thickness = 0.3     #thickness of walls

wallRight = box(pos = (side,0,0),length = thickness, height = 2*side, width = 2*side, color=color.gray(0.7))
wallRight.velocity = vector(-0.1,0,0)
wallLeft = box(pos = (-side,0,0),length = thickness, height = 2*side, width = 2*side, color=color.gray(0.7))
wallBack = box(pos = (0,0,-side),length = 2*side, height = 2*side, width = thickness, color=color.gray(0.7))
wallTop = box(pos = (0,side,0),length = 2*side, height = 0.5, width = 2*side, color=color.gray(0.7))
wallBot = box(pos = (0,-side,0),length = 2*side, height = 0.5, width = 2*side, color=color.gray(0.7))

#define acceleration
a = vector(0,0,-9.8)

#create gas molecules
no_particles = 10
ball_radius = 0.2
max_pos = side - 0.5*thickness - ball_radius    #how far up to a wall a molecule is allowed to go
k = 1.4E-23
T = 300
M_atom = 4E-3/6E23
avg_vel = sqrt(2*k*T/M_atom)
max_vel = avg_vel

ball_list = []
for i in range(no_particles):
    ball = sphere(color = color.cyan, radius = ball_radius)     #define a molecule
    ball.pos = max_pos*vector(uniform(-1,1), uniform(-1,1), uniform(-1,1))
    ball.velocity = max_vel*vector(uniform(-1,1), uniform(-1,1), uniform(-1,1))
    ball.trail = curve(pos=[ball.pos], color = ball.color)
    ball_list.append(ball)


dt = 1E-3           #time step for calculations
win = 500

#create a window for animation of gas
scene = display(title = "Helium Gas", width = win, height = win, x = 0, y = 0, center = (0.5,0.5,0.5))

#create a window for histogram plot of the velocity distribution
delta_v  = 100      #bin size for histogram
vdist = gdisplay(x = 0, y = win, ymax = no_particles*delta_v/1000.0, width = win, height = 0.6*win, xtitle = 'v', ytitle = 'N')
theory = gcurve(color = color.yellow)
dv = 10.0
for v in arange(0.0, 3000.0 + dv, dv):
    theory.plot(pos = (v, (delta_v/dv)*no_particles*4.0*pi*((M_atom/(2*pi*k*T))**1.5*exp((-0.5*M_atom*v**2)/(k*T))*v**2*dv)))
observed = ghistogram(bins = arange(0.0,3000.0, delta_v), accumulate = True,average = 1, color = color.red)

v_list = []

while True:
    rate(100)       #sets number of times repeated
    for ball in ball_list:
        #move balls
        ball.pos = ball.pos + ball.velocity*dt + 1/2.0*a*dt*dt
        #check for collisions with right wall, reflect if collision
        if ball.pos.x > wallRight.pos.x:
            ball.velocity.x = -ball.velocity.x + wallRight.velocity.x
            ball.pos.x = -0.5*thickness - ball.radius + ball.pos.x
        if ball.pos.x < wallLeft.pos.x:
            ball.velocity.x = - ball.velocity.x
            ball.pos.x = 0.5*thickness + ball.radius + ball.pos.x
        if ball.pos.y > max_pos:
            ball.velocity.y = -ball.velocity.y
            ball.pos.y = 2*max_pos - ball.pos.y
        if ball.pos.y < -max_pos:
            ball.velocity.y = -ball.velocity.y
            ball.pos.y = -2*max_pos - ball.pos.y
        if ball.pos.z < - max_pos:
            ball.velocity.z = -ball.velocity.z
            ball.pos.z = -2*max_pos - ball.pos.z
        if ball.pos.z > max_pos:
            ball.velocity.z = -ball.velocity.z
            ball.pos.z = 2*max_pos - ball.pos.z
        v_list.append(mag(ball.velocity))
        observed.plot(data = v_list)
        if wallRight.pos.x > -2:
            wallRight.pos.x = wallRight.pos.x + wallRight.velocity.x*dt
    del v_list[:]



