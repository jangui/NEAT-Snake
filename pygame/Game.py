import pygame
import numpy as np
import random

from Snake import Snake, Direction

class Game:
    """ class for snake game """

    def __init__(self, game_dimensions: (int, int)):
        """ init for snake game """
        self.background_color = (0,0,0)
        self.game_dimensions = game_dimensions
        self.food_color = (220,0,0)
        self.snake_color = (0,250,0)
        self.snake_head_color = (25, 200, 25)
        self.border_color = (0,255,0)
        self.border_width = 2
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.font_color = (220, 0, 0)
        self.reset()

    def reset(self):
        """ reset game """
        self.points = 0
        self.done = False
        self.board = np.zeros(self.game_dimensions)
        self.snake = self.place_snake()
        self.place_food()

    def move(self):
        """ move snake """
        # get snake head and tail before moving
        snake_head_x = self.snake.body[0][0]
        snake_head_y = self.snake.body[0][1]
        snake_tail_x = self.snake.body[-1][0]
        snake_tail_y = self.snake.body[-1][1]

        # check wall collisions
        direction = self.snake.direction
        match direction:
            case Direction.LEFT:
                snake_head_x -= 1
                if snake_head_x < 0: # hit left wall
                    self.done = True

            case Direction.RIGHT: # move right
                snake_head_x += 1
                if snake_head_x >= self.game_dimensions[0] : # hit right wall
                    self.done = True

            case Direction.UP: # move up
                snake_head_y -= 1
                if snake_head_y < 0 : # hit top wall
                    self.done = True

            case Direction.DOWN: # move down
                snake_head_y += 1
                if snake_head_y >= self.game_dimensions[1] : # hit bottom wall
                    self.done = True

        if self.done:
            return

        # check if snake hit own body
        head_position = self.board[snake_head_y][snake_head_x]
        if head_position == -1:
            self.done = True
            return

        # check if snake ate food
        ate_food = False
        if head_position == 1:
            ate_food = True
            self.points += 1

        # move snake
        self.snake.move(ate_food)

        # move snake head
        self.board[snake_head_y][snake_head_x] = -1

        # move snake tail
        if ate_food:
            self.board[snake_tail_y][snake_tail_x] = -1
            self.place_food()
        else:
            self.board[snake_tail_y][snake_tail_x] = 0

    def place_snake(self) -> Snake:
        """ place snake on board when game is reset """
        rows = self.game_dimensions[0]
        cols = self.game_dimensions[1]

        # place snake on random starting position
        snake_x = random.randint(0, cols-1)
        snake_y = random.randint(0, rows-1)
        starting_position = (snake_x, snake_y)
        self.board[snake_y][snake_x] = -1

        return Snake(starting_position, self.snake_color)

    def place_food(self):
        """ place a food pallet on game board """
        rows = self.game_dimensions[0]
        cols = self.game_dimensions[1]

        # place food on random position
        food_x = random.randint(0, cols-1)
        food_y = random.randint(0, rows-1)

        # re select position if on snake
        while self.board[food_y][food_x] == -1:
            food_x = random.randint(0, cols-1)
            food_y = random.randint(0, rows-1)

        self.board[food_y][food_x] = 1

    def render(self, screen: pygame.Surface):
        """ render game state to screen """
        rows = self.game_dimensions[0]
        cols = self.game_dimensions[1]
        screen_width, screen_height = screen.get_size()

        # fill background
        screen.fill(self.background_color)

        # displaying parameters
        row_width =  (screen_width // rows) * 0.8
        col_width = (screen_height // cols) * 0.8
        x_margin = screen_width * 0.14
        y_margin = screen_height * 0.14
        screen_width = screen_width - x_margin * 2
        screen_height = screen_height - y_margin * 2

        # draw points to screen
        text = self.font.render(f'Points: {self.points}', True, self.font_color)
        textRect = text.get_rect()
        textRect.center = (textRect.width, textRect.height)
        screen.blit(text, textRect)

        # draw appropriate object in each game cell
        for row in range(rows):
            y = (row_width * row) + y_margin
            for col in range(cols):
                x = (col_width * col) + x_margin

                # draw object for current cell
                current_cell = self.board[row][col]
                if current_cell == -1: # draw snake
                    snake_radius_size = col_width // 4
                    snake_head_x, snake_head_y = self.snake.body[0]
                    snake_color = self.snake_color
                    if snake_head_x == col and snake_head_y == row:
                        snake_radius_size *= 1.3
                        snake_color = self.snake_head_color
                    pygame.draw.circle(screen, snake_color, (x, y), snake_radius_size)

                elif current_cell == 1: # draw food
                    food_radius_size = col_width // 2.5
                    pygame.draw.circle(screen, self.food_color, (x, y), food_radius_size)

                # draw border
                if col == 0:
                    x1 = (x - col_width // 2) - self.border_width // 2
                    x2 = (x - col_width // 2) - self.border_width // 2
                    y1 = y - row_width // 2
                    y2 = y + row_width // 2
                    pygame.draw.line(screen, self.border_color, (x1, y1), (x2, y2), self.border_width)
                elif col == self.game_dimensions[1]-1:
                    x1 = x + col_width // 2
                    x2 = x + col_width // 2
                    y1 = y - row_width // 2
                    y2 = y + row_width // 2
                    pygame.draw.line(screen, self.border_color, (x1, y1), (x2, y2), self.border_width)
                if row == 0:
                    x1 = x - col_width // 2
                    x2 = x + col_width // 2
                    y1 = y - row_width // 2
                    y2 = y - row_width // 2
                    pygame.draw.line(screen, self.border_color, (x1, y1), (x2, y2), self.border_width)
                elif row == self.game_dimensions[0]-1:
                    x1 = x - col_width // 2
                    x2 = x + col_width // 2
                    y1 = y + row_width // 2
                    y2 = y + row_width // 2
                    pygame.draw.line(screen, self.border_color, (x1, y1), (x2, y2), self.border_width)
