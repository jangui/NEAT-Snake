from collections import deque
from enum import Enum

class Direction(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3

class Snake:
    """ Class for the player's Snake """

    def __init__(self, snake_pos: (int, int), color: (int, int, int)):
        """ initialize snake at given starting position """
        self.body = deque()
        self.color = color
        self.body.append(snake_pos)
        self.direction = Direction.LEFT

    def change_direction(self, direction: int):
        """ change the snake's direction """
        match direction:
            case 0:
                self.direction = Direction.LEFT
            case 1:
                self.direction = Direction.RIGHT
            case 2:
                self.direction = Direction.UP
            case 3:
                self.direction = Direction.DOWN


    def move(self, ate_food=False):
        """ move the snake's body """
        head_x, head_y = self.body[0]

        match self.direction:
            case Direction.LEFT:
                head_x -= 1
            case Direction.RIGHT:
                head_x += 1
            case Direction.UP:
                head_y -= 1
            case Direction.DOWN:
                head_y += 1

        # place head at new position
        new_head = (head_x, head_y)
        self.body.appendleft(new_head)

        if not ate_food:
            tail = self.body.pop()

