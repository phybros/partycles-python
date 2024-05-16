import random
import pygame
from pygame.math import Vector2
import line_profiler
from quadtree import Point, AABB

WIDTH = 3000
HEIGHT = 3000

MARGIN = 100
MARGIN_FORCE = 0.2

K = 0.5

MIN_DISTANCES = {
    'GREEN': {
        'GREEN': 40,
        'RED': 100
    },
    'RED': {
        'GREEN': 40,
        'RED': 100
    }
}
FORCES = {
    'GREEN': {
        'GREEN': 0.9,
        'RED': -1.0
    },
    'RED': {
        'GREEN': 1.0,
        'RED': 0.8
    }
}
RADII = {
    'GREEN': {
        'GREEN': 500,
        'RED': 50
    },
    'RED': {
        'GREEN': 500,
        'RED': 1000
    }
}


class Particle:
    type = "SELF"
    pos = Vector2()
    mass = 1
    color = (255, 0, 0)

    def __init__(self, type):
        self.type = type
        self.pos = Vector2(random.randrange(0, WIDTH), random.randrange(0, HEIGHT))

    def mapFromTo(self, x, a, b, c, d):
        y = (x - a) / (b - a) * (d - c) + c
        return y

    def calculate_margin_force(self):
        total_force = Vector2()

        to_max_x = WIDTH - self.pos.x
        if to_max_x < MARGIN:
            force = Vector2(-MARGIN_FORCE, 0)
            force *= self.mapFromTo(to_max_x, 0.0, MARGIN, 1.0, 0.0)
            force *= K * 2
            total_force += force

        to_max_y = HEIGHT - self.pos.y
        if to_max_y < MARGIN:
            force = Vector2(0, -MARGIN_FORCE)
            force *= self.mapFromTo(to_max_y, 0.0, MARGIN, 1.0, 0.0)
            force *= K * 2
            total_force += force

        if self.pos.x < MARGIN:
            force = Vector2(MARGIN_FORCE, 0)
            force *= self.mapFromTo(self.pos.x, 0.0, MARGIN, 1.0, 0.0)
            force *= K * 2
            total_force += force

        if self.pos.y < MARGIN:
            force = Vector2(0, MARGIN_FORCE)
            force *= self.mapFromTo(self.pos.y, 0.0, MARGIN, 1.0, 0.0)
            force *= K * 2
            total_force += force

        return total_force

    @line_profiler.profile
    def update(self, delta, sp):
        dir = Vector2()
        total_force = Vector2()
        acc = Vector2()
        vel = Vector2()
        #
        # particles = qt.query(AABB(Point(self.pos.x, self.pos.y), 500))
        # # print(len(particles))
        #
        # for other in particles:
        #     particle = allparticles[other.data]

        particles = sp.get_objects_in_range(self.pos, WIDTH/10)
        # particles = sp.get_points_in_range(self.pos, 200)
        for particle in particles:
            # for particle in allparticles:
            if particle == self:
                continue

            dir = particle.pos - self.pos
            # if dir.x > 0.5 * 800:
            #     dir.x -= 800
            # if dir.x < -0.5 * 800:
            #     dir.x += 800
            # if dir.y > 0.5 * 800:
            #     dir.y -= 800
            # if dir.y < -0.5 * 800:
            #     dir.y += 800

            dis = dir.magnitude()
            if dis > 0:
                dir = dir.normalize()

            mindist = MIN_DISTANCES[self.type][particle.type]
                # if self.type in MIN_DISTANCES and particle.type in \
                #                                                  MIN_DISTANCES[self.type] else 200
            radii = RADII[self.type][particle.type]
                # if self.type in RADII and particle.type in \
                #                                        RADII[self.type] else 500
            forces = FORCES[self.type][particle.type]
                # if self.type in FORCES and particle.type in FORCES[
                # self.type] else 1



            total_force += self.calculate_margin_force()

            if dis < mindist:
                force = dir * abs(forces) * -3
                force *= self.mapFromTo(dis, 0.0, mindist, 1.0, 0.0)
                force *= K
                total_force += force
            if dis < radii:
                force = dir * forces
                force *= self.mapFromTo(dis, 0.0, radii, 1.0, 0.0)
                force *= K
                total_force += force

        acc += total_force / self.mass
        vel += acc

        # friction
        vel *= 0.85

        self.pos += vel
        # self.pos.x = (self.pos.x + 800) % 800
        # self.pos.y = (self.pos.y + 800) % 800

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, 5)
