import pygame
import numpy as np

class Vehicle:
    def __init__(self, x, y, max_speed):
        self.pos = pygame.math.Vector2(x, y)  
        self.vel = pygame.math.Vector2(0, 0)  
        self.acc = pygame.math.Vector2(0, 0)  
        self.max_speed = max_speed  
        self.max_force = 0.1  
        self.screen_width = WIDTH
        self.screen_height = HEIGHT

    def apply_force(self, force):
        self.acc += force

    def update(self):
        self.vel += self.acc
        if self.vel.length() > 0:
            self.vel = self.vel.normalize() * self.max_speed
        self.pos += self.vel
        self.acc *= 0

        if self.pos.x < 0:
            self.apply_force(pygame.math.Vector2(1, 0))
        elif self.pos.x > self.screen_width:
            self.apply_force(pygame.math.Vector2(-1, 0))
        if self.pos.y < 0:
            self.apply_force(pygame.math.Vector2(0, 1))
        elif self.pos.y > self.screen_height:
            self.apply_force(pygame.math.Vector2(0, -1))

    def draw(self, screen):
        direction = self.vel.angle_to(pygame.math.Vector2(1, 0))
        rotated_image = pygame.transform.rotate(vehicle_image, direction)
        screen.blit(rotated_image, self.pos - pygame.math.Vector2(rotated_image.get_size()) / 2)

    def seek1(self, target):
        desired = target - self.pos
        if desired.length() < self.max_speed:
            self.vel *= 0
        else:
            desired = desired.normalize() * self.max_speed
            steer = desired - self.vel
            if steer.length() > self.max_force:
                steer.scale_to_length(self.max_force)
            self.apply_force(steer)

    def seek(self, target):
        desired = target - self.pos
        if desired.length() < self.max_speed:
            self.vel *= 0
        else:
            desired = desired.normalize() * self.max_speed
            steer = desired - self.vel
            if steer.length() > self.max_force:
                steer.scale_to_length(self.max_force)
            return steer

    def seek2(self, target):
        desired = target - self.pos
        d = desired.magnitude()
        if desired.length() < self.max_speed:
            self.vel *= 0
        else:
            if d < 1 :
                m = d / 1 * self.max_speed
                desired *= m
            else :
                desired = desired.normalize() * self.max_speed
            steer = desired - self.vel
            if steer.length() > self.max_force:
                steer.scale_to_length(self.max_force)
            return steer

    def wander(self, target):
        angle = np.random.uniform(-np.pi / 16, np.pi / 16)
        random_heading = pygame.math.Vector2(*self.vel).rotate_rad(angle)
        seek_force = self.seek(target)
        if seek_force is not None:
            new_heading = random_heading + seek_force
        else:
            new_heading = random_heading

        if new_heading.length() > 0:
            self.vel = new_heading.normalize() * self.max_speed
        else:
            angle = np.random.uniform(-np.pi / 16, np.pi / 16)
            self.vel = pygame.math.Vector2(1, 0).rotate_rad(angle) * self.max_speed

        if self.pos.distance_to(target) < 10:
            self.vel *= 0


WIDTH = 640
HEIGHT = 480

START_X = 100
START_Y = 100
MAX_SPEED = 2

TARGET_X = 500
TARGET_Y = 300

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Avtonomni liki")

vehicle_image = pygame.image.load("vehicle.png").convert_alpha()
vehicle_image = pygame.transform.scale(vehicle_image, (50, 50))

vehicle = Vehicle(START_X, START_Y, MAX_SPEED)

clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEMOTION:
            TARGET_X, TARGET_Y = event.pos

    target = pygame.math.Vector2(TARGET_X, TARGET_Y)
    #vehicle.seek1(target)

    #if vehicle.pos.x < 0 or vehicle.pos.x > WIDTH or vehicle.pos.y < 0 or vehicle.pos.y > HEIGHT:
     #   vehicle.vel *= -1  # obrnemo hitrost vozila
      #  vehicle.seek(pygame.math.Vector2(START_X, START_Y))
        #vehicle.vel *= 0

    vehicle.wander(target)
    vehicle.update()

    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (128, 128, 128), (TARGET_X, TARGET_Y), 10, 2)
    vehicle.draw(screen)

    pygame.display.update()

    clock.tick(60)
