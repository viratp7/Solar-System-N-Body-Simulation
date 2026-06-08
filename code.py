import pygame
import math
from collections import deque
pygame.init()
WIDTH, HEIGHT = 1500, 1000
FPS = 60
G = 6.6743
win = pygame.display.set_mode((WIDTH, HEIGHT))

class body:
    def __init__(self, x, y, r, mass, vx, vy, dt, c):
        self.x = x
        self.y = y
        self.oldx = x - (vx * dt)
        self.oldy = y - (vy * dt)
        self.r = r
        self.mass = mass
        self.color = c
        self.rings = deque(maxlen = 5000)
    def gravity(self, planetss, dt):
        acceleration_x = 0
        acceleration_y = 0
        for planet in planetss:

            if planet == self:
                continue
            else:
                distance = math.sqrt((self.x - planet.x) **2 + (self.y - planet.y) **2 )
                distance = max(distance, 5)
                acceleration = (G * planet.mass ) / distance **2
                angle = math.atan2(planet.y - self.y, planet.x - self.x)
                acceleration_x += acceleration * math.cos(angle)
                acceleration_y += acceleration * math.sin(angle)
            
        vy = (self.y - self.oldy)/dt
        vx = (self.x - self.oldx)/dt
        newx = self.x + (vx * dt) + acceleration_x * dt * dt
        newy = self.y + (vy * dt) + acceleration_y * dt * dt
        self.oldx = self.x
        self.x = newx
        self.oldy = self.y
        self.y = newy
        self.rings.append((int(self.x), int(self.y)))
    def draw(self, zoom, cx, cy):
        screen_x = cx + (self.x - cx) * zoom
        screen_y = cy + (self.y - cy) * zoom
        pygame.draw.circle(win, self.color, (int(screen_x), int(screen_y)), int(max(1,self.r*zoom)))
        zoomed_lines = []
        if len(self.rings) > 1:
            for lx, ly in self.rings:
                s_x = cx + (lx - cx) * zoom
                s_y = cy + (ly - cy) * zoom
                zoomed_lines.append((int(s_x), int(s_y)))

            pygame.draw.aalines(win, 'White', False, list(zoomed_lines))

centerx = WIDTH//2
centery = HEIGHT//2
DT = 0.005
sun_mass = 200000


sun = body(centerx, centery, 200, mass=sun_mass, vx = 0, vy=0, dt=DT, c="Yellow")

def speed(distance):
    e = (math.sqrt((G*sun_mass)/distance))
    return e

mer_pos = 354
mercury = body(centerx-mer_pos, centery, 3, 0.33, 0, speed(mer_pos), DT, (169,169,169))

ven_pos = 488
venus = body(centerx-ven_pos, centery, 5, 4.87, 0, speed(ven_pos), DT, (230,194,128))

ear_pos = 599
earth = body(centerx-ear_pos, centery, 6, 5.97, 0, speed(ear_pos), DT, (0,100,255))

mars_pos = 808
mars = body(centerx-mars_pos, centery, 4, 0.64, 0, speed(mars_pos), DT, (193,68,14))

jup_pos = 2078
jupiter = body(centerx-jup_pos, centery, 40, 1898, 0, speed(jup_pos), DT, (216,160,96))

sat_pos = 3828
saturn = body(centerx-sat_pos, centery, 18, 568, 0, speed(sat_pos), DT, (226,191,125))

uran_pos = 7664
uranus = body(centerx-uran_pos, centery, 12, 86.8, 0, speed(uran_pos), DT, (173,216,230))

nept_pos = 12000
neptune = body(centerx-nept_pos, centery, 12, 102, 0, speed(nept_pos), DT, (39,64,139))

system = [sun, mercury,venus, earth, mars, jupiter, saturn, uranus, neptune]
def main():
    running = True
    clock = pygame.time.Clock()
    zoom = 1 
    anchor_x = int(system[0].x)
    anchor_y = int(system[0].y)
    Maxz = 10
    Minz = 0.05
    while running:


        win.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    zoom = min(Maxz, zoom * 1.1)
                elif event.button == 5:
                    zoom = max(Minz, zoom / 1.1)
        for i in system:
            i.gravity(system, DT)
        for i in system:
            i.draw(zoom, anchor_x, anchor_y)
        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()
main()
