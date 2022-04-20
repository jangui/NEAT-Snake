import numpy as np
from PIL import Image
import cv2
from random import randint

class Snake:
    def __init__(self, x: int, y: int) -> None:
        """ Init snake """
        self.body = [ [x, y] ]
        self.tail_prev_pos = self.body[-1].copy()

    def move(self, x: int, y: int) -> None:
        """ Move snake """
        # get save old tail position in case we need to grow
        self.tail_prev_pos = self.body[-1].copy()

        # move body
        body = self.body.copy()
        for i in range(1, len(self.body)):
            body[i] = self.body[i-1].copy()
        self.body = body

        # move head
        self.body[0][0] += x
        self.body[0][1] += y

    def grow(self):
        """ Grow snake """
        self.body.append(self.tail_prev_pos)

class Game:
    def __init__(self, dimensions: (int, int)) -> None:
        """ Init the game of snake """
        self.dimensions = dimensions
        self.reset()

    def reset(self) -> np.ndarray:
        """ Reset Game """
        self.board = np.zeros((self.dimensions[0], self.dimensions[1]))
        self.done = False
        self.place_snake()
        self.place_food()
        self.points = 0
        return self.board

    def place_snake(self) -> None:
        """ Place the snake on a random position on the board """
        snake_x = randint(0, self.dimensions[0] - 1)
        snake_y = randint(0, self.dimensions[1] - 1)
        self.board[snake_y][snake_x] = -1
        self.snake = Snake(snake_x, snake_y)

    def place_food(self) -> None:
        """
        Place food on a random position on the board
        note: snake must be already placed
        """
        food_x = randint(0, self.dimensions[0] - 1)
        food_y = randint(0, self.dimensions[1] - 1)

        # replace food if in snake's body
        while self.board[food_x][food_y] == -1:
            food_x = randint(0, self.dimensions[0] - 1)
            food_y = randint(0, self.dimensions[1] - 1)

        self.board[food_y][food_x] = 1
        self.food = (food_x, food_y)

    def step(self, action: int) -> np.ndarray:
        """ One game step. """
        x = y = 0
        match action:
            case 0: # move right
                x = 1
            case 1: # move left
                x = -1
            case 2: # move up
                y = 1
            case 3: # move down
                y = -1
        valid_move = self.move_snake(x, y)

        if not valid_move:
            self.done = True
            print(f'Game Over! Points: {self.points}')

        return self.board

    def move_snake(self, x: int, y: int) -> bool:
        """ Move the snake horizontally in the x direction and vertically in y """
        snake_head_x, snake_head_y = self.snake.body[0]
        snake_tail_x, snake_tail_y = self.snake.body[-1]

        # find new head position on board
        new_snake_head_x = snake_head_x + x
        new_snake_head_y = snake_head_y + y

        # check for horizontal wall collisions
        if new_snake_head_x >= self.dimensions[0] or new_snake_head_x < 0:
            return False

        # check for vertical wall collisions
        if new_snake_head_y >= self.dimensions[1] or new_snake_head_y < 0:
            return False

        # check for collisions vs own body
        new_head_position = self.board[new_snake_head_y][new_snake_head_x]
        if new_head_position == -1:
            return False

        # if no collision, move snake
        self.snake.move(x, y)
        self.board[new_snake_head_y][new_snake_head_x] = -1

        # if we ate food, grow snake and dont update tail's position
        if new_head_position == 1:
            self.snake.grow()
            self.place_food()
            self.points += 1
            return True

        # if food not eaten, move the tail
        self.board[snake_tail_y][snake_tail_x] = 0
        return True

    def render(self) -> None:
        if self.done:
            return
        else:
            if cv2.waitKey(1) & 0xFF == ord("q"):
                return

        print(self.board)

        board = np.zeros((self.dimensions[0], self.dimensions[1], 3), dtype=np.uint8)
        food_color = (0, 0, 255)
        snake_color = (255, 175, 0)

        # loop over snake rendering whole body
        for i in range(len(self.snake.body)):
            board[self.snake.body[i][1]][self.snake.body[i][0]] = snake_color

        board[self.food[1]][self.food[0]] = food_color

        img = Image.fromarray(board, "RGB")
        img = img.resize((300,300))
        cv2.imshow("Snake", np.array(img))
