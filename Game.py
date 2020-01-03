import numpy as np
from PIL import Image
import cv2
from random import randint
from Settings import Settings

class Snake:
    def __init__(self, x, y):
        self.x = randint(0, x-1)
        self.y = randint(0, y-1)
        self.snake = [[self.x,self.y]]

    def move(self, x, y):
        for i in range(len(self.snake)):
            self.snake[i][0] += x
            self.snake[i][1] += y
        self.x = self.snake[0][0]
        self.y = self.snake[0][1]

class Game:
    def __init__(self):
        self.s = Settings()
        self.snake = Snake(self.s.game_x, self.s.game_y)
        self.food = [None, None]
        self.reward = 0
        self.place_food()

    def place_food(self):
        food_x = randint(0, self.s.game_x-1)
        food_y = randint(0, self.s.game_y-1)
        """
        while [food_x, food_y] not in self.snake.snake:
            food_x = randint(0, self.s.game_x)
            food_y = randint(0, self.s.game_y)
        """
        self.food = [food_x, food_y]

    def reset(self):
        self.done = False
        self.snake = Snake(self.s.game_x, self.s.game_y)
        self.place_food()
        return (self.snake.snake, self.food)

    def step(self, action):
        if action == 0: #move right
            self.snake.move(1,0)
        elif action == 1: #move left
            self.snake.move(-1,0)
        elif action == 2: #move up
            self.snake.move(0,1)
        elif action == 3: #move down
            self.snake.move(0,-1)

        if (self.snake.x == self.s.game_x) or (self.snake.y == self.s.game_y):
            #snake hit wall (case 1)
            self.done = True
        elif (self.snake.x < 0) or (self.snake.y < 0):
            #snake hit wall (case 2)
            self.done = True
        elif (self.snake.x == self.food[0]) and (self.snake.y == self.food[1]):
            #snake got food
            self.reward = self.s.food_reward
            self.place_food()
        elif (self.snake.x, self.snake.y) in self.snake.snake[1:]:
            #snake hit body
            self.reward = self.s.body_reward
            self.done = True

        new_state = (self.snake.snake, self.food)
        return (new_state, self.reward)

    def render(self):
        print(self.snake.snake, self.food, self.done)
        if self.done:
            return
            if cv2.waitKey(500) & 0xFF == ord("q"):
                return
        else:
            if cv2.waitKey(1) & 0xFF == ord("q"):
                return
        board = np.zeros((self.s.game_x, self.s.game_y, 3), dtype=np.uint8)
        food_color = (0, 255, 0)
        snake_color = (255, 175, 0)
        """
        for i in range(len(self.snake.snake)):
            board[self.snake.snake[i][0]][self.snake.snake[i][1]] = snake_color
        """
        board[self.snake.x][self.snake.y] = snake_color
        board[self.food[0]][self.food[1]] = food_color
        img = Image.fromarray(board, "RGB")
        img = img.resize((300,300))
        cv2.imshow("image", np.array(img))

