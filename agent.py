import torch
import random
import numpy as np
from collections import deque
from environment import SnakeGameAI
from environment import Direction
from environment import GParams
from environment import Point
from model import Linear_QNet
from model import QTrainer
from helper import plot

# Constants
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001
STATE_SIZE = 11
ACTION_SIZE = 3
HIDDEN_SIZE = 256


class Agent:
    def __init__(self):
        self.generation = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        self.model = Linear_QNet(STATE_SIZE, HIDDEN_SIZE, ACTION_SIZE)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

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

    def remember(self, state, action, reward, next_state, done):
        # pop left if MAX_MEMORY is reached
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            # list of tuples
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        states, actions, rewards, next_states, done = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves : tradeoff exploration / exploitation
        self.epsilon = 80 - self.generation
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            initialstate = torch.tensor(state, dtype=torch.float)
            prediction = self.model(initialstate)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI()
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(
            state_old,
            final_move,
            reward,
            state_new,
            done
        )

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            game.reset()
            agent.generation += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Generation : ', agent.generation, end=" | ")
            print('Score : ', score, end=" | ")
            print('Record : ', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.generation
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    train()
