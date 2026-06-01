import pygame
import math
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
    def draw(self):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.r)

centerx = WIDTH//2
centery = HEIGHT//2
DT = 0.005
sun_mass = 2000000

sun = body(centerx, centery, 25, mass=sun_mass, vx = 0, vy=0, dt=DT, c="Yellow")
def speed(distance):
    e = (math.sqrt((G*sun_mass)/distance))
    return e
mercury = body(centerx-60,  centery, 3, 0.33, 0, speed(60),  DT, (169,169,169))
venus = body(centerx-90,  centery, 5, 4.87, 0, speed(90),  DT, (230,194,128))
earth = body(centerx-130, centery, 5, 5.97, 0, speed(130), DT, (0,100,255))
mars = body(centerx-180, centery, 4, 0.64, 0, speed(180), DT, (193,68,14))
jupiter = body(centerx-280, centery, 12, 1898, 0, speed(280), DT, (216,160,96))
saturn = body(centerx-380, centery, 10, 568,  0, speed(380), DT, (226,191,125))
uranus = body(centerx-500, centery, 8, 86.8, 0, speed(500), DT, (173,216,230))
neptune = body(centerx-620, centery, 8, 102,  0, speed(620), DT, (39,64,139))
system = [sun, mercury,venus, earth, mars, jupiter, saturn, uranus, neptune]
def main():
    running = True
    clock = pygame.time.Clock()

    while running:
        
        win.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        for i in system:
            i.draw()
            i.gravity(system, DT)
        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()
main()
