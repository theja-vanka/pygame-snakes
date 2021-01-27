import torch
import numpy as np
from train.environment import SnakeGameAI
from train.environment import Direction
from train.environment import GParams
from train.environment import Point
from train.model import Linear_QNet

# Constants
STATE_SIZE = 11
ACTION_SIZE = 3
HIDDEN_SIZE = 256


class Agent:
    def __init__(self):
        self.path = './experiments/best61.pth'
        self.model = Linear_QNet(STATE_SIZE, HIDDEN_SIZE, ACTION_SIZE)
        self.model.load_state_dict(torch.load(self.path))

    def get_state(self, game):
        head = game.snake[0]
        point_l = Point(head.x - GParams.BLOCK_SIZE.value, head.y)
        point_r = Point(head.x + GParams.BLOCK_SIZE.value, head.y)
        point_u = Point(head.x, head.y - GParams.BLOCK_SIZE.value)
        point_d = Point(head.x, head.y + GParams.BLOCK_SIZE.value)

        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        # [
        #   danger straight , danger right, danger left,
        #   direction left, direction right, direction up, direction down,
        #   food left, food right, food up, food down
        # ]
        state = [
            # Danger straight state
            (dir_l and game.is_collision(point_l)) or
            (dir_r and game.is_collision(point_r)) or
            (dir_u and game.is_collision(point_u)) or
            (dir_d and game.is_collision(point_d)),

            # Danger right state
            (dir_l and game.is_collision(point_u)) or
            (dir_r and game.is_collision(point_d)) or
            (dir_u and game.is_collision(point_r)) or
            (dir_d and game.is_collision(point_l)),

            # Danger left state
            (dir_l and game.is_collision(point_d)) or
            (dir_r and game.is_collision(point_u)) or
            (dir_u and game.is_collision(point_l)) or
            (dir_d and game.is_collision(point_r)),

            # Move direction state
            dir_l,  # direction left
            dir_r,  # direction right
            dir_u,  # direction up
            dir_d,  # direction down

            # Food direction state
            game.food.x < game.head.x,  # food left
            game.food.x > game.head.x,  # food right
            game.food.y < game.head.y,  # food up
            game.food.y > game.head.y   # food down
        ]

        return np.array(state, dtype=int)

    def get_action(self, state):
        # random moves : tradeoff exploration / exploitation
        final_move = [0, 0, 0]
        initialstate = torch.tensor(state, dtype=torch.float)
        prediction = self.model(initialstate)
        move = torch.argmax(prediction).item()
        final_move[move] = 1
        return final_move


def run():
    agent = Agent()
    game = SnakeGameAI(train=False)
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        _, done, score = game.play_step(final_move)

        if done:
            print('Score : ', score)
            break


if __name__ == '__main__':
    run()
