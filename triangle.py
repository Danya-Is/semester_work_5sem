import math
from math import sqrt

from OpenGL.GL import *

from primitives import Vertex, Vector
from hemicube import HemiCube


class Triangle:
    red = 0.3
    green = 0.3
    blue = 0.3

    light_red = 0.0
    light_green = 0.0
    light_blue = 0.0

    reflected_red = 0.0
    reflected_green = 0.0
    reflected_blue = 0.0

    is_light = False
    is_obstruction = False

    def __init__(self, a: Vertex, b: Vertex, c: Vertex):
        self.a = a
        self.b = b
        self.c = c
        self.center = self._center()
        self.normal = self._normal()

    def _center(self):
        a = self.a
        b = self.b
        c = self.c
        return Vertex((a.x + b.x + c.x) / 3, (a.y + b.y + c.y) / 3, (a.z + b.z + c.z) / 3)

    def _normal(self):
        a = self.a
        b = self.b
        c = self.c
        v1x = b.x - a.x
        v1y = b.y - a.y
        v1z = b.z - a.z

        v2x = c.x - a.x
        v2y = c.y - a.y
        v2z = c.z - a.z
        wrki = sqrt((v1y * v2z - v1z * v2y) ** 2 + (v1z * v2x - v1x * v2z) ** 2 + (v1x * v2y - v1y * v2x) ** 2)
        nx = (v1y * v2z - v1z * v2y) / wrki
        ny = (v1z * v2x - v1x * v2z) / wrki
        nz = (v1x * v2y - v1y * v2x) / wrki
        return Vector(nx, ny, nz)

    def set_light(self, r, g, b):
        self.light_red = r
        self.light_green = g
        self.light_blue = b
        self.is_light = True

    def set_colour(self, r, g, b):
        self.red = r
        self.green = g
        self.blue = b

    def draw(self):
        glBegin(GL_TRIANGLES)
        glColor(self.red, self.green, self.blue)
        glVertex3f(self.a.x, self.a.y, self.a.z)
        glVertex3f(self.b.x, self.b.y, self.b.z)
        glVertex3f(self.c.x, self.c.y, self.c.z)
        glEnd()

    def max_edge(self):
        a = self.a
        b = self.b
        c = self.c
        ab = a.distance_by(b)
        ac = a.distance_by(c)
        bc = b.distance_by(c)

        return max(ab, ac, bc)

    def area(self):
        a = self.a
        b = self.b
        c = self.c
        ab = a.distance_by(b)
        ac = a.distance_by(c)
        bc = b.distance_by(c)
        return square(ab, ac, bc)

    def split(self):
        a = self.a
        b = self.b
        c = self.c
        ab = a.distance_by(b)
        ac = a.distance_by(c)
        bc = b.distance_by(c)

        m = max(ab, ac, bc)

        if ab == m:
            return self.split_edge(a, b, c)

        if ac == m:
            return self.split_edge(a, c, b)

        if bc == m:
            return self.split_edge(b, c, a)

    def split_edge(self, a, b, c):
        middle = Vertex(a.x + ((b.x - a.x) / 2), a.y + ((b.y - a.y) / 2), a.z + ((b.z - a.z) / 2))
        triangle1 = Triangle(middle, b, c)
        triangle2 = Triangle(c, a, middle)
        triangle1.set_light(self.light_red, self.light_green, self.light_blue)
        triangle1.set_colour(self.red, self.green, self.blue)
        triangle2.set_light(self.light_red, self.light_green, self.light_blue)
        triangle2.set_colour(self.red, self.green, self.blue)
        return triangle1, triangle2

    def form_factor_by(self, patch, hid):
        if hid == 0:
            return 0.0
        center1 = self.center
        center2 = patch.center
        normal1 = self.normal
        normal2 = patch.normal
        connector = center1.diff(center2).to_vector()
        cos_i = normal1.cos_by(connector)
        cos_j = normal2.cos_by(connector)

        r = center1.distance_by(center2)

        ff = ((cos_i * cos_j) / (math.pi * (r ** 2))) * hid * self.area()

        if ff < 0:
            print("ff<0")
            return 0.0

        return ff

    def form_factor_by2(self, patch):
        center = self.center
        normal = self.normal
        u = self.a.diff(self.b).to_vector().vector_normalize()
        r = u.vector_with_normal(normal)
        hemicube = HemiCube(10)
        ff = 0
        ff += hemicube.ff_on_one_side(center, True)

        return ff

    def contains(self, p):
        ab = self.a.distance_by(self.b)
        bc = self.b.distance_by(self.c)
        ca = self.c.distance_by(self.a)
        ap = self.a.distance_by(p)
        bp = self.b.distance_by(p)
        cp = self.c.distance_by(p)

        delta = square(ap, bp, ab) + square(ap, cp, ca) + square(bp, cp, bc) - square(ab, bc, ca)
        if abs(delta) < 0.01:
            return True
        return False

    def visible_by(self, patch, i, j, patches):
        connector = self.center.diff(patch.center).to_vector()
        dot = patch.center
        for x, p in enumerate(patches):
            if x == i or x == j or not p.is_obstruction:
                continue
            if dot.intersects(connector, p, self.center):
                return 0
        return 1


def square(a, b, c):
    per = (a + b + c) / 2
    vl = (per - a) * (per - b) * (per - c) * per
    if vl < 0.0:
        return 0.0

    return math.sqrt((per - a) * (per - b) * (per - c) * per)
