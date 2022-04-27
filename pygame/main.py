import pygame
import time

from Game import Game

def main():
    # init pygame
    pygame.init()

    screen_dimensions = (500, 500)
    main_screen = pygame.display.set_mode(screen_dimensions)

    game_dimensions = (10, 10)
    game = Game(game_dimensions)

    running = True
    game.render(main_screen)
    time.sleep(1)
    while running:
        # handle events
        direction = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # handle window close button
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.snake.change_direction(2)
                elif event.key == pygame.K_LEFT:
                    game.snake.change_direction(0)
                elif event.key == pygame.K_DOWN:
                    game.snake.change_direction(3)
                elif event.key == pygame.K_RIGHT:
                    game.snake.change_direction(1)

        # move snake
        game.move()

        # render to screen
        game.render(main_screen)

        # update display
        pygame.display.flip()

        time.sleep(0.2)

        # check if game over
        if game.done:
            game.reset()
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()
