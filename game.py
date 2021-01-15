import pygame
import random
from enum import Enum
from collections import namedtuple


pygame.init()


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple('Point', 'x', 'y')
BLOCK_SIZE = 20


class SnakeGame():
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snakes')
        self.clock = pygame.time.Clock()

        # init game style
        self.direction = Direction.RIGHT
        self.head = Point(self.w/2, self.h/2)
        self.snake = [
            self.head,
            Point(self.head.x-BLOCK_SIZE, self.head.y),
            Point(self.head.x-(2*BLOCK_SIZE), self.head.y)
        ]
        self.score = 0
        self.food = None

    def play_step(self):
        pass


if __name__ == '__main__':
    game = SnakeGame()

    # game loop
    while True:
        game.play_step()

        # break if game over

    pygame.quit()
