class Settings():

    def __init__(self):

        self.screen_width = 1000
        self.screen_height = 600
        self.bg_color = (230,230,230)
        #self.ship_speed = 1
        self.ship_limit = 3

        '''子弹设置'''
        #self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 10
        self.bullet_color = 60,60,60
        self.bullet_allowed = 10

        '''外星人设置'''
        #self.alien_speed_factor = 2
        self.fleet_drop_speed = 10
        #移动方向
        #self.fleet_direction = 1

        '''游戏节奏控制'''
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        self.fleet_direction = 1

        self.alien_points = 30
        self.score_scale = 1.5

    def increase_speed(self):

        self.ship_speed *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)