import pygame
import numpy as np

class Game:
    """ class for snake game """

    def __init__(self, game_dimensions, screen_dimensions):
        """ init for snake game """
        pygame.init()
        self.background_color = (255,255,255)
        self.game_dimensions = game_dimensions
        self.screen_dimensions = screen_dimensions
        self.screen = pygame.display.set_mode(screen_dimensions)
        self.running = True # is game running
        self.done = False # is game won/lost
        self.reset()

    def reset(self):
        """ reset game """
        self.points = 0
        self.done = False
        self.board = np.zeros(self.game_dimensions)
        #self.snake = self.place_snake()
        #self.place_food()

    def render(self):
        """ render game state to screen """
        rows = self.game_dimensions[0]
        cols = self.game_dimensions[1]
        screen_width = self.screen_dimensions[0]
        screen_height = self.screen_dimensions[1]

        snake_color = (255,0,0)
        food_color = (0,0,255)

        self.board[4][5] = -1
        self.board[4][6] = -1
        self.board[4][7] = -1
        self.board[2][1] = 1

        # fill background
        self.screen.fill(self.background_color)

        for row in range(rows):
            row_width = screen_width // rows
            x = row_width * row
            for col in range(cols):
                col_width = screen_height // cols
                y = col_width * col
                current_tile = self.board[col][row]
                if current_tile == -1:
                    pygame.draw.circle(self.screen, snake_color, (x, y), row_width)
                elif current_tile == 1:
                    pygame.draw.circle(self.screen, food_color, (x, y), row_width)

        # update display
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            # handle window close button
            if event.type == pygame.QUIT:
                self.running = False

    def shutdown(self):
        """ handle closing game """
        self.running = False
        pygame.quit()


def main():
    screen_width = 500
    screen_height = 500
    rows = 10
    cols = 10
    background_color = (255, 255, 255)
    snake_color = (0, 0, 255)

    screen_dimensions = (500, 500)
    game_dimensions = (10, 10)

    game = Game(game_dimensions, screen_dimensions)

    while game.running:

        game.handle_events()
        game.render()

    game.shutdown()

if __name__ == "__main__":
    main()
