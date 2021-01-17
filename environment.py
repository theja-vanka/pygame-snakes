import numpy as np
import pygame
import random
from enum import Enum
from collections import namedtuple

# Introduce the following changes to game :
# 1. Reset function
# 2. Reward function
# 3. play(action) -> direction
# 4. game_iteration
# 5. is_collision
pygame.init()

# Datastructure for points
Point = namedtuple('Point', 'x, y')
font = pygame.font.Font('assets/PressStart2P-Regular.ttf', 10)


# Enums to limit Direction
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


class GParams(Enum):
    INNER_BLOCK = 12  # Snake tail size
    BLOCK_SIZE = 20  # Pixel size of 1 block
    SPEED = 40  # Higher is faster
    IB_OFFSET = 4  # Snake growth offset


class ColorParams(Enum):
    # rgb colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (200, 0, 0)
    LIGHTRED = (200, 100, 0)
    BLUE = (0, 0, 255)
    SKYBLUE = (0, 100, 255)


class SnakeGameAI():
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snakes')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
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
        self.frame_iteration = 0

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

    def play_step(self, action):
        # 1. collect user input
        self.frame_iteration += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 2. move
        self.__move_snake(action)  # update the head
        self.snake.insert(0, self.head)

        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self.__place_food()
        else:
            self.snake.pop()

        # 5. update ui and clock
        self.__update_ui()
        self.clock.tick(GParams.SPEED.value)

        # 6. return game over and score
        game_over = False
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        condition1 = pt.x > self.w - GParams.BLOCK_SIZE.value
        condition2 = pt.x < 0
        condition3 = pt.y > self.h - GParams.BLOCK_SIZE.value
        condition4 = pt.y < 0
        if condition1 or condition2 or condition3 or condition4:
            return True
        # Snake collision starts at 1 index
        if pt in self.snake[1:]:
            return True

        return False

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
                ColorParams.SKYBLUE.value,
                pygame.Rect(
                    pt.x+GParams.IB_OFFSET.value,
                    pt.y+GParams.IB_OFFSET.value,
                    GParams.INNER_BLOCK.value,
                    GParams.INNER_BLOCK.value
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
        pygame.draw.rect(
            self.display,
            ColorParams.LIGHTRED.value,
            pygame.Rect(
                self.food.x+GParams.IB_OFFSET.value,
                self.food.y+GParams.IB_OFFSET.value,
                GParams.INNER_BLOCK.value,
                GParams.INNER_BLOCK.value
            )
        )

        text = font.render(
            "Score : " + str(self.score),
            True,
            ColorParams.WHITE.value
        )
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def __move_snake(self, action):
        # [straight, right, left]

        clock_wise = [
            Direction.RIGHT,
            Direction.DOWN,
            Direction.LEFT,
            Direction.UP
        ]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            self.direction = clock_wise[idx]  # no change
        elif np.array_equal(action, [0, 1, 0]):
            # r -> d -> l -> u
            next_idx = (idx + 1) % 4
            self.direction = clock_wise[next_idx]  # right turn
        else:
            # r -> u -> l -> d
            next_idx = (idx - 1) % 4
            self.direction = clock_wise[next_idx]  # left turn

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += GParams.BLOCK_SIZE.value
        elif self.direction == Direction.LEFT:
            x -= GParams.BLOCK_SIZE.value
        elif self.direction == Direction.DOWN:
            y += GParams.BLOCK_SIZE.value
        elif self.direction == Direction.UP:
            y -= GParams.BLOCK_SIZE.value

        self.head = Point(x, y)
