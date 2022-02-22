import time

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from scene import Scene

scene = Scene()
viewpoint_x = 24
viewpoint_y = 6
viewpoint_z = 12
look_at_x = 0
look_at_y = 0
look_at_z = 0
up_vector_x = 0
up_vector_y = 1
up_vector_z = 0


def init(width, height):
    start_time = time.time()

    scene.prepare()

    glClearDepth(1.0)
    glDepthRange(0.0, 0.85)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width) / float(height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    print("Done in", time.time() - start_time, "s")


def axis():
    axsize = 1
    glBegin(GL_LINES)
    glColor(1, 0, 0)
    glVertex3f(axsize, 0, 0)
    glVertex3f(-axsize, 0, 0)
    glColor(0, 1, 0)
    glVertex3f(0, axsize, 0)
    glVertex3f(0, -axsize, 0)
    glColor(0, 0, 1)
    glVertex3f(0, 0, axsize)
    glVertex3f(0, 0, -axsize)
    glEnd()


def draw_scene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewpoint_x, viewpoint_y, viewpoint_z,
              look_at_x, look_at_y, look_at_z,
              up_vector_x, up_vector_y, up_vector_z)

    scene.draw()
    # axis()

    glutSwapBuffers()


def resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width) / float(height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def key_listener(*args):
    global viewpoint_x
    global viewpoint_y
    global viewpoint_z
    global look_at_x
    global look_at_y
    global look_at_z

    key = args[0]
    speed = 0.4

    if key == '\033':
        glutDestroyWindow(window_id)
        sys.exit()
    if key == '\161':  # q
        viewpoint_x = viewpoint_x + speed
    if key == '\141':  # a
        viewpoint_x = viewpoint_x - speed
    if key == '\167':  # w
        viewpoint_y = viewpoint_y + speed
    if key == '\163':  # s
        viewpoint_y = viewpoint_y - speed
    if key == '\145':  # e
        viewpoint_z = viewpoint_z + speed
    if key == '\144':  # d
        viewpoint_z = viewpoint_z - speed
    if key == '\165':  # u
        look_at_x = look_at_x + speed
    if key == '\152':  # j
        look_at_x = look_at_x - speed
    if key == '\151':  # i
        look_at_y = look_at_y + speed
    if key == '\153':  # k
        look_at_y = look_at_y - speed
    if key == '\157':  # o
        look_at_z = look_at_z + speed
    if key == '\154':  # l
        look_at_z = look_at_z - speed

if __name__ == '__main__':
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1200, 1200)
    glutInitWindowPosition(50, 50)
    glutInit(sys.argv)

    window_id = glutCreateWindow("Radiosity")
    glutDisplayFunc(draw_scene)
    glutIdleFunc(draw_scene)
    glutKeyboardFunc(key_listener)
    glutReshapeFunc(resize)

    init(1200, 1200)

    glutMainLoop()
