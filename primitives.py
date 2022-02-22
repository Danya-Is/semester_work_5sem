import math

import numpy as np


class Vertex:

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __neg__(self):
        return Vertex(-self.x, -self.y, -self.z)

    def to_vector(self):
        return Vector(self.x, self.y, self.z)

    def diff(self, v):
        return Vertex(self.x - v.x, self.y - v.y, self.z - v.z)

    def add(self, v):
        return Vertex(self.x + v.x, self.y + v.y, self.z + v.z)

    def intersects(self, direction, triangle, end):
        n = triangle.normal
        p0 = triangle.center
        dot_pr = direction.dot(n)
        if abs(dot_pr) > 0:
            pi = self.add(direction.mult(-n.dot(self.diff(p0)) / dot_pr).to_vertex())
            return triangle.contains(pi) and pi.in_range(self, end)
        return False

    def distance_by(self, v):
        vector1 = np.array([self.x, self.y, self.z])
        vector2 = np.array([v.x, v.y, v.z])

        return np.sqrt(np.sum(np.square(vector1 - vector2)))

    def in_range(self, d1, d2):
        x = self.x
        y = self.y
        z = self.z
        x_check = (d1.x <= x <= d2.x) or (d2.x <= x <= d1.x)
        y_check = (d1.y <= y <= d2.y) or (d2.y <= y <= d1.y)
        z_check = (d1.z <= z <= d2.z) or (d2.z <= z <= d1.z)
        return x_check and y_check and z_check


class Vector:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)

    def diff(self, v):
        return Vector(self.x - v.x, self.y - v.y, self.z - v.z)

    def add(self, v):
        return Vector(self.x + v.x, self.y + v.y, self.z + v.z)

    def mult(self, n):
        return Vector(self.x * n, self.y * n, self.z * n)

    def norm(self):
        return math.sqrt(self.dot(self))

    def normalize(self):
        norm = self.norm()
        if norm > 0.01:
            self.x = self.x / norm
            self.y = self.y / norm
            self.z = self.z / norm
        return self

    def vector_with_normal(self, v):
        x1 = self.x
        y1 = self.y
        z1 = self.z
        x2 = v.x
        y2 = v.y
        z2 = v.z

        wrki = math.sqrt((y1 * z2 - z1 * y2) ** 2 + (z1 * x2 - x1 * z2) ** 2 + (x1 * y2 - y1 * x2) ** 2)
        nx = (y1 * z2 - z1 * y2) / wrki
        ny = (z1 * x2 - x1 * z2) / wrki
        nz = (x1 * y2 - y1 * x2) / wrki
        return Vector(nx, ny, nz)

    def angle_by(self, v):
        cos = self.cos_by(v)
        angle = np.arccos(cos)
        return angle

    def cos_by(self, v):
        v1 = np.array(self.to_array())
        v2 = np.array(v.to_array())
        dot_pr = abs(self.dot(v))
        norms = np.linalg.norm(v1) * np.linalg.norm(v2)

        if norms == 0.0:
            cos = 0
        else:
            cos = dot_pr / norms
        # angle = np.arccos(cos)
        if cos > 1:
            print("cos > 1")
        return cos

    def to_array(self):
        return [self.x, self.y, self.z]

    def to_vertex(self):
        return Vertex(self.x, self.y, self.z)

    def dot(self, v):
        return self.x * v.x + self.y * v.y + self.z * v.z


def dot_product(v1: Vertex, v2: Vertex):
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z


def length(v):
    return math.sqrt(dot_product(v, v))
