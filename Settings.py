class Settings:
    def __init__(self):
        ###game dimensions
        self.game_x = 20
        self.game_y = 20

        ###rewards
        #collect food
        self.food_reward = 100
        #crash into wall
        self.wall_reward = -100
        #crash into own body
        self.body_reward = -100
