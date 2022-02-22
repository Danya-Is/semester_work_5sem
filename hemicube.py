from OpenGL.GL import *
from OpenGL.GLUT import *


class HemiCube(object):
    def __init__(self, dim=300):
        self.dim = dim

    def ff_on_one_side(self, patch2, is_top_face):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        x_dim = self.dim
        y_dim = self.dim
        if not is_top_face:
            y_dim = self.dim // 2
        glViewport(0, 0, x_dim, y_dim)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        patch2.draw()
        glutSwapBuffers()
        pixels = glReadPixelsb(0, 0, x_dim, y_dim, GL_RGBA, GL_UNSIGNED_BYTE)

