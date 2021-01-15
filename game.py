import pygame
import random
from enum import Enum
from collections import namedtuple


# Enums to limit Direction
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


class GParams(Enum):
    TRAIL_SIZE = 12  # Snake tail size
    BLOCK_SIZE = 20  # Pixel size of 1 block
    SPEED = 40  # Higher is faster
    TAIL_OFFSET = 4  # Snake growth offset


class ColorParams(Enum):
    # rgb colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (200, 0, 0)
    BLUE = (0, 0, 255)
    BLUE2 = (0, 100, 255)


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
            Point(self.head.x-(GParams.BLOCK_SIZE.value), self.head.y),
            Point(self.head.x-(2*GParams.BLOCK_SIZE.value), self.head.y)
        ]
        self.score = 0
        self.food = None
        self.__place_food()

    def __place_food(self):
        x = random.randint(
            0,
            (self.w-GParams.BLOCK_SIZE.value)//GParams.BLOCK_SIZE.value
        )*GParams.BLOCK_SIZE.value
        y = random.randint(
            0,
            (self.h-GParams.BLOCK_SIZE.value)//GParams.BLOCK_SIZE.value
        )*GParams.BLOCK_SIZE.value
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
        self.__update_ui()
        self.clock.tick(GParams.SPEED.value)
        # 6. return game over and score
        game_over = False
        return game_over, self.score

    def __update_ui(self):
        self.display.fill(ColorParams.BLACK.value)

        for pt in self.snake:
            pygame.draw.rect(
                self.display,
                ColorParams.BLUE.value,
                pygame.Rect(
                    pt.x,
                    pt.y,
                    GParams.BLOCK_SIZE.value,
                    GParams.BLOCK_SIZE.value
                )
            )
            pygame.draw.rect(
                self.display,
                ColorParams.BLUE2.value,
                pygame.Rect(
                    pt.x+GParams.TAIL_OFFSET.value,
                    pt.y+GParams.TAIL_OFFSET.value,
                    GParams.TRAIL_SIZE.value,
                    GParams.TRAIL_SIZE.value
                )
            )

        pygame.draw.rect(
            self.display,
            ColorParams.RED.value,
            pygame.Rect(
                self.food.x,
                self.food.y,
                GParams.BLOCK_SIZE.value,
                GParams.BLOCK_SIZE.value
            )
        )

        text = font.render(
            "Score : " + str(self.score),
            True,
            ColorParams.WHITE.value
        )
        self.display.blit(text, [0, 0])
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()

    # Datastructure for points
    Point = namedtuple('Point', 'x, y')
    font = pygame.font.Font('PressStart2P-Regular.ttf', 10)

    game = SnakeGame()

    # game loop
    while True:
        game_over, score = game.play_step()

        # break if game over
        if game_over is True:
            break

    print('Final Score')

    pygame.quit()
