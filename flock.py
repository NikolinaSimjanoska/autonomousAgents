import pygame
import numpy as np
import random
from pygame import Vector2


class Vehicle:
    def __init__(self, x, y, max_speed, color):
        self.pos = pygame.math.Vector2(x, y)  
        self.vel = pygame.math.Vector2(0, 0)  
        self.acc = pygame.math.Vector2(0, 0)  
        self.max_speed = max_speed  
        self.max_force = 0.1 
        self.color = color
        self.screen_width = WIDTH
        self.screen_height = HEIGHT
        self.x = x
        self.y = y
        self.vel_x = random.randint(-3, 3)
        self.vel_y = random.randint(-3, 3)

    def apply_force(self, force):
        self.acc += force

    def update(self, vehicles):
        alignment = self.align(vehicles)
        cohesion = self.cohere(vehicles)
        separation = self.separate(vehicles)

        alignment *= 0
        cohesion *= 0
        separation *= 1

        self.acc += alignment + cohesion + separation
        self.vel += self.acc
        #if self.vel.length() > 0:
        if self.vel.length_squared() > 0.0001:
            self.vel.scale_to_length(MAX_SPEED)
        else:
            self.vel = Vector2(1, 0).rotate(random.uniform(0, 360)) * MAX_SPEED
        self.pos += self.vel
        self.acc *= 0

        if self.pos.x < 0:
            self.pos.x += WIDTH
        elif self.pos.x > WIDTH:
            self.pos.x -= WIDTH
        if self.pos.y < 0:
            self.pos.y += HEIGHT
        elif self.pos.y > HEIGHT:
            self.pos.y -= HEIGHT

    def draw(self, screen):
        direction = self.vel.angle_to(pygame.math.Vector2(1, 0))
        triangle_points = [
            self.pos + pygame.math.Vector2(1, 0).rotate(-direction) * TRIANGLE_SIZE,
            self.pos + pygame.math.Vector2(1, 0).rotate(-direction + 120) * TRIANGLE_SIZE,
            self.pos + pygame.math.Vector2(1, 0).rotate(-direction - 120) * TRIANGLE_SIZE,
        ]
        pygame.draw.polygon(screen, self.color, triangle_points)

    def separate1(self, vehicles):
        desired_separation = 60
        sum = pygame.math.Vector2(0, 0)
        count = 0
        for other in vehicles:
            d = self.pos.distance_to(other.pos)
            if d > 0 and d < desired_separation:
                diff = self.pos - other.pos
                diff.normalize_ip()
                diff /= d
                sum += diff
                count += 1
        if count > 0:
            sum /= count
            sum.normalize_ip()
            sum *= self.max_speed
            steer = sum - self.vel
            if steer.length() > self.max_force:
                steer.scale_to_length(self.max_force)
            return steer

    def separate(self, vehicles):
        desired_separation = 60
        sum = Vector2(0, 0)
        count = 0
        for other in vehicles:
            distance = self.pos.distance_to(other.pos)
            if 0 < distance < desired_separation:
                diff = self.pos - other.pos
                diff.normalize_ip()
                diff /= distance
                sum += diff
                count += 1
        if count > 0:
            sum /= count
            if sum.length() > 0:
                sum.normalize_ip()
                sum *= self.max_speed
                steer = sum - self.vel
                if steer.length() > self.max_force:
                    steer.scale_to_length(self.max_force)
                return steer
        return Vector2(0, 0)

    def align(self, vehicles):
        sum = Vector2(0, 0)
        count = 0
        for other in vehicles:
            distance = self.pos.distance_to(other.pos)
            if 0 < distance < NEIGHBOR_DISTANCE:
                sum += other.vel
                count += 1
        if count > 0:
            sum /= count
            if sum.length() > 0:
                sum.normalize_ip()
                sum *= MAX_SPEED
                steer = sum - self.vel
                if self.vel.length() > 0:
                    self.vel.scale_to_length(MAX_SPEED)
                else:
                    self.vel = Vector2(1, 0).rotate(random.uniform(0, 360)) * MAX_SPEED
                return steer
            else:
                return Vector2(0, 0)
        else:
            return Vector2(0, 0)

    def cohere1(self, vehicles):
        sum = Vector2(0, 0)
        count = 0
        for other in vehicles:
            distance = self.pos.distance_to(other.pos)
            if 0 < distance < NEIGHBOR_DISTANCE:
                sum += other.pos
                count += 1
        if count > 0:
            sum /= count
            desired = sum - self.pos
            if desired.length() > 0:
                desired.normalize_ip()
                desired *= MAX_SPEED
                steer = desired - self.vel
                if steer.length() > MAX_FORCE:
                    steer.scale_to_length(MAX_FORCE)
                return steer
            else:
                return Vector2(0, 0)
        else:
            return Vector2(0, 0)

    def cohere(self, vehicles):
        sum = Vector2(0, 0)
        count = 0
        for other in vehicles:
            distance = self.pos.distance_to(other.pos)
            if 0 < distance < NEIGHBOR_DISTANCE:
                sum += other.pos
                count += 1
                if distance < MIN_DISTANCE:
                    move_away = self.pos - other.pos
                    sum += move_away
                    count += 1
        if count > 0:
            sum /= count
            desired = sum - self.pos
            if desired.length() > 0:
                desired.normalize_ip()
                desired *= MAX_SPEED
                steer = desired - self.vel
                if steer.length() > MAX_FORCE:
                    steer.scale_to_length(MAX_FORCE)
                return steer
            else:
                return Vector2(0, 0)
        else:
            return Vector2(0, 0)


WIDTH = 800
HEIGHT = 600

MAX_SPEED = 0.3

NEIGHBOR_DISTANCE = 100  
MAX_FORCE = 0.1
MIN_DISTANCE = 5

TRIANGLE_SIZE = 30
TRIANGLE_COLOR = (100,100,100)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulacija jata")


vehicles = []
for i in range(50):
    x = np.random.uniform(0, WIDTH)
    y = np.random.uniform(0, HEIGHT)
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    vehicle = Vehicle(x, y, MAX_SPEED, color)
    vehicles.append(vehicle)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    for vehicle in vehicles:
        vehicle.update(vehicles)

        vehicle.draw(screen)

    pygame.display.flip()

pygame.quit()

