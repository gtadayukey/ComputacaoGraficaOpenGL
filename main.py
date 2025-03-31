import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

pygame.init()

# project settings
screen_width = 1600
screen_height = 800
background_color = (0, 0, 0, 1)
drawing_color = (1, 1, 1, 1)

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('OpenGL in Python')

# Translation variables
trans_x, trans_y, trans_z = 0, 0, 0
translation_speed = 0.1

# Mirroring variables
mirror_x, mirror_y, mirror_z = 1, 1, 1

# Scale variables
scale_x, scale_y, scale_z = 1, 1, 1
scaling_speed = 0.1


# Load texture function
def load_texture(image_path):
    texture_surface = pygame.image.load(image_path)
    texture_data = pygame.image.tostring(texture_surface, "RGB", True)

    width = texture_surface.get_width()
    height = texture_surface.get_height()

    # Generate texture ID
    texture_id = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texture_id)

    # Set the texture parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

    # Load the texture to OpenGL
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)

    return texture_id


# Initialize the texture
texture_id = load_texture("diamante.jpg")  # Replace with your texture file path


def initialise():
    glClearColor(background_color[0], background_color[1], background_color[2], background_color[3])
    glColor(drawing_color)

    # Enable texture mapping
    glEnable(GL_TEXTURE_2D)

    # Disable face culling to render all faces (even back faces)
    glDisable(GL_CULL_FACE)

    # projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, (screen_width / screen_height), 0.1, 100.0)

    # modelview
    glMatrixMode(GL_MODELVIEW)
    glTranslate(0, 0, -6)  # Adjusting camera position
    glLoadIdentity()
    glViewport(0, 0, screen.get_width(), screen.get_height())
    glEnable(GL_DEPTH_TEST)


def apply_texture():
    # Bind the texture
    glBindTexture(GL_TEXTURE_2D, texture_id)

    # Draw the cube with texture on its faces
    glBegin(GL_QUADS)

    # Front face
    glTexCoord2f(0, 0)
    glVertex3f(-1, -1, 1)
    glTexCoord2f(1, 0)
    glVertex3f(1, -1, 1)
    glTexCoord2f(1, 1)
    glVertex3f(1, 1, 1)
    glTexCoord2f(0, 1)
    glVertex3f(-1, 1, 1)

    # Back face
    glTexCoord2f(0, 0)
    glVertex3f(-1, -1, -1)
    glTexCoord2f(1, 0)
    glVertex3f(-1, 1, -1)
    glTexCoord2f(1, 1)
    glVertex3f(1, 1, -1)
    glTexCoord2f(0, 1)
    glVertex3f(1, -1, -1)

    # Top face
    glTexCoord2f(0, 0)
    glVertex3f(-1, 1, -1)
    glTexCoord2f(1, 0)
    glVertex3f(-1, 1, 1)
    glTexCoord2f(1, 1)
    glVertex3f(1, 1, 1)
    glTexCoord2f(0, 1)
    glVertex3f(1, 1, -1)

    # Bottom face
    glTexCoord2f(0, 0)
    glVertex3f(-1, -1, -1)
    glTexCoord2f(1, 0)
    glVertex3f(1, -1, -1)
    glTexCoord2f(1, 1)
    glVertex3f(1, -1, 1)
    glTexCoord2f(0, 1)
    glVertex3f(-1, -1, 1)

    # Right face
    glTexCoord2f(0, 0)
    glVertex3f(1, -1, -1)
    glTexCoord2f(1, 0)
    glVertex3f(1, 1, -1)
    glTexCoord2f(1, 1)
    glVertex3f(1, 1, 1)
    glTexCoord2f(0, 1)
    glVertex3f(1, -1, 1)

    # Left face
    glTexCoord2f(0, 0)
    glVertex3f(-1, -1, -1)
    glTexCoord2f(1, 0)
    glVertex3f(-1, -1, 1)
    glTexCoord2f(1, 1)
    glVertex3f(-1, 1, 1)
    glTexCoord2f(0, 1)
    glVertex3f(-1, 1, -1)

    glEnd()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()

    # Apply translation
    glTranslatef(trans_x, trans_y, trans_z)

    # Apply mirroring
    glScalef(mirror_x, mirror_y, mirror_z)

    # Apply scaling based on WSADQE keys
    glScalef(scale_x, scale_y, scale_z)

    glRotatef(1, 10, 0, 1)

    # Apply texture and draw the cube
    apply_texture()

    glPopMatrix()


done = False
initialise()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                trans_x -= translation_speed
            elif event.key == pygame.K_RIGHT:
                trans_x += translation_speed
            elif event.key == pygame.K_UP:
                trans_y += translation_speed
            elif event.key == pygame.K_DOWN:
                trans_y -= translation_speed
            elif event.key == pygame.K_PAGEUP:
                trans_z += translation_speed
            elif event.key == pygame.K_PAGEDOWN:
                trans_z -= translation_speed
            elif event.key == pygame.K_x:
                mirror_x *= -1  # Toggle mirror on X-axis
            elif event.key == pygame.K_y:
                mirror_y *= -1  # Toggle mirror on Y-axis
            elif event.key == pygame.K_z:
                mirror_z *= -1  # Toggle mirror on Z-axis
            elif event.key == pygame.K_w:
                scale_y += scaling_speed  # Scale in Y axis (increase size)
            elif event.key == pygame.K_s:
                scale_y -= scaling_speed  # Scale in Y axis (decrease size)
            elif event.key == pygame.K_a:
                scale_x -= scaling_speed  # Scale in X axis (decrease size)
            elif event.key == pygame.K_d:
                scale_x += scaling_speed  # Scale in X axis (increase size)
            elif event.key == pygame.K_q:
                scale_z -= scaling_speed  # Scale in Z axis (decrease size)
            elif event.key == pygame.K_e:
                scale_z += scaling_speed  # Scale in Z axis (increase size)

    display()
    pygame.display.flip()
    pygame.time.wait(100)

pygame.quit()
