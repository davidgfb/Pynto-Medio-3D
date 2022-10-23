import pygame
from pygame.mouse import set_pos, set_visible
from pygame.locals import *
from pygame.display import set_mode
from pygame.event import get
from pygame import init, QUIT, KEYDOWN, K_ESCAPE, K_RETURN, K_PAUSE,\
                   K_p, MOUSEMOTION, K_w, K_s, K_d, K_a
from pygame.key import get_pressed

from OpenGL.GL import *
from OpenGL.GL import glEnable
from OpenGL.GLU import *

from numpy import array

display = (1280, 720)
displayCenter = array(set_mode(display, 1073741826).get_size())\
                // 2

init()
tuple(map(glEnable, (GL_DEPTH_TEST, GL_LIGHTING,\
                     GL_COLOR_MATERIAL, GL_LIGHT0))) #opc
glShadeModel(GL_SMOOTH)
glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
tuple(glLightfv(*a) for a in ((GL_LIGHT0, GL_AMBIENT,\
                               array(((1,) * 3 + (2,))) / 2),\
       (GL_LIGHT0, GL_DIFFUSE, (1,) * 4))) #opc

sphere = gluNewQuadric()
w, h = display

glMatrixMode(GL_PROJECTION)
gluPerspective(45, w / h, 0.1, 50)

glMatrixMode(GL_MODELVIEW)
gluLookAt(*((0, -8,) + (0,) * 6 + (1,)))

viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

glLoadIdentity()

# init mouse movement and center mouse on screen

mouseMove, up_down_angle, paused, run = [0, 0], 0, False, True

set_pos(displayCenter)
set_visible(False)

while run:
    for event in get():
        if event.type == QUIT or\
           (event.type == KEYDOWN and\
            (event.key == K_ESCAPE or event.key == K_RETURN)):
            run = False

        if event.type == KEYDOWN and\
           (event.key == K_PAUSE or event.key == K_p):
            paused = not paused
            set_pos(displayCenter)

        if not paused: 
            if event.type == MOUSEMOTION:
                mouseMove = event.pos - displayCenter
                
            set_pos(displayCenter)

    if not paused:
        # get keys
        keypress = get_pressed()
        #mouseMove = pygame.mouse.get_rel()
    
        # init model view matrix
        glLoadIdentity()

        # apply the look up and down
        x, y = mouseMove
        up_down_angle += y / 10

        glRotatef(up_down_angle, 1, 0, 0)

        # init the view matrix
        glPushMatrix()
        glLoadIdentity()

        x, y, z = 0, 0, 0

        # apply the movment 
        if keypress[K_w]:
            z = 0.1

        if keypress[K_s]:
            z = -0.1

        if keypress[K_d]:
            x = -0.1

        if keypress[K_a]:
            x = 0.1

        glTranslatef(x, y, z)

        # apply the left and right rotation
        glRotatef(mouseMove[0]*0.1, 0.0, 1.0, 0.0)

        # multiply the current matrix by the get the new view matrix and store the final vie matrix 
        glMultMatrixf(viewMatrix)
        viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

        # apply view matrix
        glPopMatrix()
        glMultMatrixf(viewMatrix)

        glLightfv(GL_LIGHT0, GL_POSITION, [1, -1, 1, 0])

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glPushMatrix()

        glColor4f(0.5, 0.5, 0.5, 1)
        glBegin(GL_QUADS)
        glVertex3f(-10, -10, -2)
        glVertex3f(10, -10, -2)
        glVertex3f(10, 10, -2)
        glVertex3f(-10, 10, -2)
        glEnd()

        glTranslatef(-1.5, 0, 0)
        glColor4f(0.5, 0.2, 0.2, 1)
        gluSphere(sphere, 1.0, 32, 16) 

        glTranslatef(3, 0, 0)
        glColor4f(0.2, 0.2, 0.5, 1)
        gluSphere(sphere, 1.0, 32, 16) 

        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)

pygame.quit()
