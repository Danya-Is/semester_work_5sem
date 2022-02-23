from triangle import Triangle
from primitives import Vertex

from OpenGL.GLUT import *

max_patch_edge = 1
light_constant = 50


class Scene:
    patches = []
    triangles = []
    block_triangles = []
    form_factors = []
    hid = []
    radiosity_iterations = 0

    def __init__(self):

        # пол
        t1 = Triangle(Vertex(0, 0, 0), Vertex(0, 0, 4), Vertex(4, 0, 0))
        t2 = Triangle(Vertex(4, 0, 0), Vertex(0, 0, 4), Vertex(4, 0, 4))
        t1.set_colour(0.8, 0.8, 0.8)
        t2.set_colour(0.8, 0.8, 0.8)

        # стена1
        w1 = Triangle(Vertex(4, 0, 4), Vertex(0, 0, 4), Vertex(4, 4, 4))
        w2 = Triangle(Vertex(0, 0, 4), Vertex(4, 4, 4), Vertex(0, 4, 4))
        w1.set_colour(0.3, 0.5, 0.2)
        w2.set_colour(0.3, 0.5, 0.2)

        # стена2
        w3 = Triangle(Vertex(4, 0, 4), Vertex(4, 0, 0), Vertex(4, 4, 0))
        w4 = Triangle(Vertex(4, 0, 4), Vertex(4, 4, 4), Vertex(4, 4, 0))
        w3.set_colour(0.6, 0.3, 0.2)
        w4.set_colour(0.6, 0.3, 0.2)

        # куб1
        c1 = Triangle(Vertex(2, 0, 2.5), Vertex(2, 0, 3.5), Vertex(2, 3, 3.5))
        c2 = Triangle(Vertex(2, 3, 3.5), Vertex(2, 3, 2.5), Vertex(2, 0, 2.5))
        c3 = Triangle(Vertex(2, 0, 2.5), Vertex(2, 3, 2.5), Vertex(1.5, 0, 2.5))
        c4 = Triangle(Vertex(1.5, 0, 2.5), Vertex(2, 3, 2.5), Vertex(1.5, 3, 2.5))
        c5 = Triangle(Vertex(2, 0, 3.5), Vertex(2, 3, 3.5), Vertex(1.5, 0, 3.5))
        c6 = Triangle(Vertex(1.5, 0, 3.5), Vertex(2, 3, 3.5), Vertex(1.5, 3, 3.5))
        c7 = Triangle(Vertex(1.5, 0, 2.5), Vertex(1.5, 0, 3.5), Vertex(1.5, 3, 3.5))
        c8 = Triangle(Vertex(1.5, 3, 3.5), Vertex(1.5, 3, 2.5), Vertex(1.5, 0, 2.5))
        c9 = Triangle(Vertex(1.5, 3, 2.5), Vertex(1.5, 3, 3.5), Vertex(2, 3, 3.5))
        c10 = Triangle(Vertex(2, 3, 3.5), Vertex(1.5, 3, 2.5), Vertex(2, 3, 2.5))

        # куб2
        c21 = Triangle(Vertex(1.7, 0, 1), Vertex(1.7, 0, 2), Vertex(1.7, 1, 2))
        c22 = Triangle(Vertex(1.7, 1, 2), Vertex(1.7, 1, 1), Vertex(1.7, 0, 1))
        c23 = Triangle(Vertex(1.7, 0, 1), Vertex(1.7, 1, 1), Vertex(0.7, 0, 1))
        c24 = Triangle(Vertex(0.7, 0, 1), Vertex(1.7, 1, 1), Vertex(0.7, 1, 1))
        c25 = Triangle(Vertex(1.7, 0, 2), Vertex(1.7, 1, 2), Vertex(0.7, 0, 2))
        c26 = Triangle(Vertex(0.7, 0, 2), Vertex(1.7, 1, 2), Vertex(0.7, 1, 2))
        c27 = Triangle(Vertex(0.7, 0, 1), Vertex(0.7, 0, 2), Vertex(0.7, 1, 2))
        c28 = Triangle(Vertex(0.7, 1, 2), Vertex(0.7, 1, 1), Vertex(0.7, 0, 1))
        c29 = Triangle(Vertex(0.7, 1, 1), Vertex(0.7, 1, 2), Vertex(1.7, 1, 2))
        c210 = Triangle(Vertex(1.7, 1, 2), Vertex(0.7, 1, 1), Vertex(1.7, 1, 1))

        # источник света
        light1 = Triangle(Vertex(0, 3, 2), Vertex(0, 3.5, 2), Vertex(0, 3, 2.5))
        light2 = Triangle(Vertex(0, 3.5, 2), Vertex(0, 3.5, 2.5), Vertex(0, 3, 2.5))
        light1.set_light(light_constant, light_constant, light_constant)
        light1.set_colour(light_constant, light_constant, light_constant)
        light2.set_light(light_constant, light_constant, light_constant)
        light2.set_colour(light_constant, light_constant, light_constant)

        self.block_triangles.extend([c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c21, c22, c23, c24, c25, c26, c27, c28, c29, c210])
        self.triangles.extend([t1, t2, w1, w2, w3, w4, light1, light2])

    def prepare(self):
        print("prepare")
        self.break_into_patches()
        self.form_factors = [[-1] * len(self.patches) for _ in range(len(self.patches))]
        self.hid = [[-1] * len(self.patches) for _ in range(len(self.patches))]
        self.calculate_hid()
        print("hid calculated")
        self.calculate_form_factors()
        print("form factors calculated")
        self.radiosity1()
        while 1:
            old_value = self.patches[0].total_red
            self.radiosity()
            if self.patches[0].total_red - old_value < 0.1:
                break

        for p in self.patches:
            p.visible_red = p.total_red * p.red / 2
            p.visible_green = p.total_green * p.green / 2
            p.visible_blue = p.total_blue * p.blue / 2

    def draw(self):
        for patch in self.patches:
            patch.draw()

    def break_into_patches(self):
        big_patches = self.triangles

        while len(big_patches):
            patch = big_patches.pop()
            if patch.max_edge() <= max_patch_edge:
                self.patches.append(patch)
            else:
                big_patches.extend(patch.split())

        big_patches = self.block_triangles

        while len(big_patches):
            patch = big_patches.pop()
            if patch.max_edge() <= max_patch_edge:
                patch.is_obstruction = True
                self.patches.append(patch)
            else:
                big_patches.extend(patch.split())

    def calculate_form_factors(self):
        for i, p1 in enumerate(self.patches):
            for j, p2 in enumerate(self.patches):
                if i == j:
                    self.form_factors[i][j] = 0.0
                else:
                    self.form_factors[i][j] = p1.form_factor_by(p2, self.hid[i][j])

    def calculate_hid(self):
        for i, p1 in enumerate(self.patches):
            for j, p2 in enumerate(self.patches):
                if i == j:
                    self.hid[i][j] = 1
                elif self.hid[j][i] != -1:
                    self.hid[i][j] = self.hid[j][i]
                else:
                    self.hid[i][j] = p1.visible_by(p2, i, j, self.patches)

    def radiosity(self):
        for i, p1 in enumerate(self.patches):
            if p1.is_light:
                continue
            inc_r = 0
            inc_g = 0
            inc_b = 0
            for j, p2 in enumerate(self.patches):
                if i == j:
                    continue
                if p2.is_light:
                    continue

                f = self.form_factors[i][j]
                if f == 0:
                    continue
                inc_r += f * p2.reflected_red
                inc_g += f * p2.reflected_green
                inc_b += f * p2.reflected_blue

            p1.new_reflected_red = inc_r
            p1.new_reflected_green = inc_g
            p1.new_reflected_blue = inc_b

        for p in self.patches:
            p.reflected_red = p.red * p.new_reflected_red / 2
            p.reflected_green = p.green * p.new_reflected_green / 2
            p.reflected_blue = p.blue * p.new_reflected_blue / 2

            p.total_red += p.new_reflected_red
            p.total_green += p.new_reflected_green
            p.total_blue += p.new_reflected_blue

    def radiosity1(self):
        for i, p1 in enumerate(self.patches):
            inc_r = 0
            inc_g = 0
            inc_b = 0
            for j, p2 in enumerate(self.patches):
                if i == j:
                    continue
                if not p2.is_light:
                    continue

                f = self.form_factors[i][j]
                if f == 0:
                    continue
                inc_r += f * p2.light_red
                inc_g += f * p2.light_green
                inc_b += f * p2.light_blue

            p1.total_red += inc_r
            p1.total_green += inc_g
            p1.total_blue += inc_b
            p1.reflected_red += inc_r * p1.red / 2
            p1.reflected_green += inc_g * p1.green / 2
            p1.reflected_blue += inc_b * p1.blue / 2
