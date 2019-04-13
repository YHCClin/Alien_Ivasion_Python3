import pygame
import sys
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
def run_game():
#初始化游戏并创建一个屏幕对象
    ai_settings = Settings()
    pygame.init()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption('Alien Ivasion')
    play_button = Button(ai_settings,screen,"Play")
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings,screen,stats)
    ship = Ship(ai_settings,screen)
    #创建一个用于存储ｂｕｌｌｅｔ的编组
    bullets = Group()
    aliens = Group()
    gf.create_fleet(ai_settings,screen,ship,aliens)


#开始游戏的主循环
    while True:
        #监听键盘和鼠标事件
        gf.check_events(ai_settings,stats,play_button,screen,ship,aliens,bullets)
        if stats.game_active:
            ship.update()
            bullets.update()
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)
            gf.update_aliens(ai_settings,stats,screen,ship,aliens,bullets)

        #更新屏幕
        gf.update_screen(ai_settings,stats,sb,screen,ship,aliens,bullets,play_button)

#运行测试
run_game()

