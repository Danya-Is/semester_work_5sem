from triangle import Triangle
from primitives import Vertex

from OpenGL.GLUT import *

max_patch_edge = 1.0
light_constant = 20


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
        t1.set_colour(0.3, 0.3, 0.3)
        t2.set_colour(0.3, 0.3, 0.3)

        # стена
        w1 = Triangle(Vertex(4, 0, 4), Vertex(0, 0, 4), Vertex(4, 4, 4))
        w2 = Triangle(Vertex(0, 0, 4), Vertex(4, 4, 4), Vertex(0, 4, 4))
        w1.set_colour(0.3, 0.5, 0.2)
        w2.set_colour(0.3, 0.5, 0.2)

        # куб
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

        # источник света
        light1 = Triangle(Vertex(0, 3, 2), Vertex(0, 3.5, 2), Vertex(0, 3, 2.5))
        light2 = Triangle(Vertex(0, 3.5, 2), Vertex(0, 3.5, 2.5), Vertex(0, 3, 2.5))
        light1.set_light(light_constant, light_constant, light_constant)
        light1.set_colour(light_constant, light_constant, light_constant)
        light2.set_light(light_constant, light_constant, light_constant)
        light2.set_colour(light_constant, light_constant, light_constant)

        self.block_triangles.extend([c1, c2, c3, c4, c5, c6, c7, c8, c9, c10])
        self.triangles.extend([t1, t2, w1, w2, light1, light2])

    def prepare(self):
        print("prepare")
        self.break_into_patches()
        self.form_factors = [[-1] * len(self.patches) for row in range(len(self.patches))]
        self.hid = [[-1] * len(self.patches) for row in range(len(self.patches))]
        self.calculate_hid()
        print("hid calculated")
        self.calculate_form_factors()
        print("form factors calculated")
        self.radiosity()
        self.radiosity()
        self.radiosity()

    def draw(self):
        for patch in self.patches:
            patch.draw()
        # for patch in self.block_triangles:
        #     patch.draw()

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
                    # self.form_factors[i][j] = p1.form_factor_by(p2, self.hid[i][j])
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
        for p2 in self.patches:
            p2.light_red += p2.reflected_red
            p2.light_green += p2.reflected_green
            p2.light_blue += p2.reflected_blue
        for i, p1 in enumerate(self.patches):
            inc_r = 0
            inc_g = 0
            inc_b = 0
            for j, p2 in enumerate(self.patches):
                if i == j:
                    continue
                if self.radiosity_iterations > 0 and p1.is_light:
                    continue

                f = self.form_factors[i][j]
                if f == 0:
                    continue
                inc_r += f * p2.light_red
                inc_g += f * p2.light_green
                inc_b += f * p2.light_blue

                # p2.light_red += f * p1.light_red/2
                # p2.light_green += f * p1.light_green/2
                # p2.light_blue += f * p1.light_blue/2

            p1.red += inc_r
            p1.green += inc_g
            p1.blue += inc_b
            p1.reflected_red += inc_r
            p1.reflected_green += inc_g
            p1.reflected_blue += inc_b

        for p2 in self.patches:
            p2.light_red = 0
            p2.light_green = 0
            p2.light_blue = 0
        self.radiosity_iterations += 1

    def radiosity1(self):
        for i, p1 in enumerate(self.patches):
            inc_r = 0
            inc_g = 0
            inc_b = 0
            for j, p2 in enumerate(self.patches):
                if i == j:
                    continue
                if self.radiosity_iterations > 0 and p1.is_light:
                    continue

                f = self.form_factors[i][j]
                if f == 0:
                    continue
                inc_r += f * p2.light_red
                inc_g += f * p2.light_green
                inc_b += f * p2.light_blue

                # p2.light_red += f * p1.light_red/2
                # p2.light_green += f * p1.light_green/2
                # p2.light_blue += f * p1.light_blue/2

            p1.red += inc_r
            p1.green += inc_g
            p1.blue += inc_b
            p1.light_red += inc_r
            p1.light_green += inc_g
            p1.light_blue += inc_b

        for p2 in self.patches:
            p2.light_red = 0
            p2.light_green = 0
            p2.light_blue = 0
        self.radiosity_iterations += 1

