from collections import deque
from config import *
import pygame
class Snake(object):
    def __init__(self, start, length):
        self.head_sprite = pygame.image.load("./sprites/snake_head.png")
        self.head_sprite.set_colorkey(WHITE)
        self.speed = SNAKE_SPEED
        self.timer = 1.0 / self.speed
        self.growth_pending = 0
        self.direction = DIRECTION_UP
        self.segments = deque([start - self.direction * i for i in range(SNAKE_INIT_LENGTH)])
    
    def __iter__(self):
        return iter(self.segments)

    def __len__(self):
        return len(self.segments)

    def change_direction(self, direction):
        if self.direction != -direction:
            self.direction = direction

    def head(self):
        return self.segments[0]
    
    def update(self, dt, direction):
        self.timer -= dt
        if self.timer > 0:
            return
        self.change_direction(direction)
        self.timer += 1/self.speed
        self.segments.appendleft(self.head() + self.direction)
        if self.growth_pending > 0:
            self.growth_pending -= 1
        else:
            self.segments.pop()

    def grow(self):
        self.growth_pending += 1
        self.speed += SNAKE_INC_SPEED
    
    def intersect(self):
        it = iter(self)
        head = next(it)
        return head in it