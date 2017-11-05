"""
Author: Guilherme David Branco
NIBBLE/SNAKE CLONE GAME to learn PYGAME
"""
import random
import pygame
from snake import Snake
from collections import deque
from pygame.locals import *
from config import *

class SnakeRun(object):
    def __init__(self):
        pygame.display.set_caption("SNAKE CLONE")
        self.block_size = BLOCK_SIZE
        self.window = pygame.display.set_mode((800,600))
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("./waffle.otf", 20)
        self.world = Rect((0,0), WORLD_SIZE)
        self.playing = START_MENU

    def reset(self):
        self.playing = PLAYING
        self.next_direction = DIRECTION_UP
        self.score = 0
        self.snake = Snake(self.world.center, SNAKE_INIT_LENGTH)
        self.food = set()
        self.add_food()
    
    def add_food(self):
        while not (self.food and random.randrange(4)):
            food = Vector(map(random.randrange, self.world.bottomright))
            if food not in self.food and food not in self.snake:
                self.food.add(food)
    
    def handle_input(self, event):
        if event.key in KEY_DIRECTION:
            self.next_direction = KEY_DIRECTION[event.key]
        elif event.key == K_SPACE and (self.playing == START_MENU or not self.playing):
            self.reset()

    def update(self, dt):
        self.snake.update(dt, self.next_direction)
        head = self.snake.head()
        if head in self.food:
            self.food.remove(head)
            self.add_food()
            self.snake.grow()
            self.score += len(self.snake) * BASE_SCORE

        if self.snake.intersect() or not self.world.collidepoint(self.snake.head()):
            self.playing = 0

    def draw_text(self, text, p):
        self.screen.blit(self.font.render(text, 1, TEXT_COLOR), p)

    def get_rect(self, p):
        return pygame.Rect(p[0]*BLOCK_WIDTH, p[1]*BLOCK_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT)

    def draw_grid(self):
        for x in range(0, SCREEN_WIDTH, BLOCK_WIDTH):
            pygame.draw.line(self.screen, TEXT_COLOR, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, BLOCK_HEIGHT):
            pygame.draw.line(self.screen, TEXT_COLOR, (0, y), (SCREEN_WIDTH, y))

    def draw(self):
        self.screen.fill(COLOR_BG)
        self.draw_grid()
        for p in self.snake:
            pygame.draw.rect(self.screen, COLOR_SNAKE_OUT, self.get_rect(p))
            pygame.draw.rect(self.screen, COLOR_SNAKE_IN, pygame.Rect(p[0]*BLOCK_WIDTH+ 4, p[1]*BLOCK_HEIGHT + 4, 
                             BLOCK_WIDTH - 8, BLOCK_HEIGHT - 8))
        for f in self.food:
            pygame.draw.rect(self.screen, COLOR_APPLE, self.get_rect(f))
    
    def draw_start(self):
        self.screen.fill(COLOR_BG)
        self.draw_text("SNAKE CLONE", (SCREEN_WIDTH/2 - 150, SCREEN_HEIGHT/2))


    def draw_gameover(self):
        self.screen.fill(DEATH_COLOR)
        self.draw_text("Game over! Aperte espaco para novo jogo", (SCREEN_WIDTH/2 - 200, SCREEN_HEIGHT/2))
        self.draw_text("Seu score foi de {}".format(self.score), (SCREEN_WIDTH/2 - 200, SCREEN_HEIGHT/2 + 50))

    def play(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            for e in pygame.event.get():
                if e.type == QUIT:
                    return
                elif e.type == KEYDOWN:
                    self.handle_input(e)
            if self.playing == PLAYING:
                self.update(dt)
                self.draw()
            elif self.playing == START_MENU:
                self.draw_start()
            else:
                self.draw_gameover()
            pygame.display.update()

def main():
    pygame.init()
    SnakeRun().play()
    pygame.quit()

if __name__ == "__main__":
    main()
