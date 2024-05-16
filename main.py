import random
import pygame
import sys
import time
from particle import Particle
from quadtree import Quadtree, Point, AABB
from spatialhash import SpatialHash
from spatialhash2 import SpatialHash2

NUM_PARTICLES = 400

WIDTH = 3000
HEIGHT = 3000

# Set up the colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

delta = 0
fpses = []
pygame.init()

display = pygame.display.set_mode((800, 800))

screen = pygame.Surface((WIDTH, HEIGHT))
pygame.display.set_caption('PARTYCLES')
screen.fill((0, 0, 0))

clock = pygame.time.Clock()

particles = []
for i in range(0, NUM_PARTICLES):
    a = Particle('GREEN')
    a.color = GREEN
    particles.append(a)

for i in range(0, NUM_PARTICLES):
    chaser = Particle('RED')
    chaser.color = RED
    particles.append(chaser)

while True:
    start = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))

    sp = SpatialHash(cell_size=50, numcells=WIDTH/50)
    for particle in particles:
        sp.add_object(particle, particle.pos)

    # sp2 = SpatialHash2(cell_size=100)
    # for particle in particles:
    #     sp2.add_point(particle.pos, particle)

    # rebuild the quadtree every frame
    # qt.clear()
    # for pi in range(0, len(particles)):
    #     p = particles[pi]
    #     qt.insert(Point(p.pos.x, p.pos.y, pi))
    #
    # qt.drawQuads(screen)
    # # pygame.draw.rect(screen, (10, 30, 10), pygame.Rect(0, 0, WIDTH, HEIGHT), width=100)

    # for i in range(0, int(WIDTH / sp.cell_size)):
    #     pygame.draw.line(screen, WHITE, (i*sp.cell_size, 0), (i*sp.cell_size, HEIGHT))
    # for i in range(0, int(HEIGHT / sp.cell_size)):
    #     pygame.draw.line(screen, WHITE, (0, i*sp.cell_size), (WIDTH, i*sp.cell_size))

    for p in particles:
        p.update(delta, sp)
        p.draw(screen)

    # take the WIDTHxHEIGHT field and smush it onto an 800x800 window
    zoomed_screen = pygame.transform.smoothscale(screen, (800, 800))
    display.blit(zoomed_screen, (0, 0))

    # # Flip everything to the display
    pygame.display.flip()
    # Draw the window onto the screen
    # pygame.display.update()
    if len(fpses) > 60:
        avg = sum(fpses) / len(fpses)
        print(1000.0/avg)
        fpses.clear()
    else:
        fpses.append((time.time() - start) * 1000)
    delta = clock.tick(60) / 1000.0
