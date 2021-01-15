import pygame
import random
from enum import Enum
from collections import namedtuple


pygame.init()


# Enums to limit Direction
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


# Datastructure for points
Point = namedtuple('Point', 'x', 'y')
BLOCK_SIZE = 20  # Pixel size of 1 block


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
        self.__place_food()

    def __place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self.__place_food()

    def play_step(self):
        pass
        # 1. collect user input

        # 2. move

        # 3. check if game over

        # 4. place new food or just move

        # 5. update ui and clock

        # 6. return game over and score


if __name__ == '__main__':
    game = SnakeGame()

    # game loop
    while True:
        game.play_step()

        # break if game over

    pygame.quit()
