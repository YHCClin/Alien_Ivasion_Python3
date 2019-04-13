import sys
import pygame
from time import sleep
from bullet import Bullet
from alien import Alien
import matplotlib

def get_number_aliens_x(ai_settings,alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_alien_x = int(available_space_x / (2 * alien_width))
    return number_alien_x

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    alien = Alien(ai_settings,screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    #给定外星人的绘制位置
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings,screen,ship,aliens):
    #创建外星人编组
    alien = Alien(ai_settings,screen)
    alien_width = alien.rect.width
    number_alien_x = get_number_aliens_x(ai_settings,alien_width)
    number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    for number_row in range(number_rows):
        for alien_number in range(number_alien_x):
            create_alien(ai_settings,screen,aliens,alien_number,number_row)

def get_number_rows(ai_settings,ship_height,alien_height):
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def check_keydown_events(event,ai_settings,screen,ship,bullets):

    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)

def check_keyup_events(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False

'''监听鼠标和键盘的事件'''
def check_events(ai_settings,stats,play_button,screen,ship,aliens,bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,play_button,ship,aliens,bullets,mouse_x,mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)

def check_play_button(ai_settings,screen,stats,play_button,ship,aliens,bullets,mouse_x,mouse_y):

    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)

    stats.reset_stats()
    stats.game_active = True

    aliens.empty()
    bullets.empty()

    create_fleet(ai_settings,screen,ship,aliens)
    ship.center_ship()


'''更新屏幕显示内容'''
def update_screen(ai_settings,stats,sb,screen,ship,aliens,bullets,play_button):
    '''每次循环都重新绘制屏幕'''

    screen.fill(ai_settings.bg_color)
    #bullets.update()
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()

def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):

    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)
    print('Number of bullet: '+str(len(bullets)))

def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):

    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        stats.score += ai_settings.alien_points
        sb.prep_score()

    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings,screen,ship,aliens)

def fire_bullet(ai_settings,screen,ship,bullets):

    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def ship_hit(ai_settings,stats,screen,ship,aliens,bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1

        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()

        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def update_aliens(ai_settings,stats,screen,ship,aliens,bullets):
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship,aliens):
        '''
        alien_coll = pygame.sprite.spritecollideany(ship,aliens)
        aliens.remove(alien_coll)
        '''
        ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
        print('alien hit !!!')
    check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets)
    print('Number of alien: '+str(len(aliens)))

def check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets):
    for alien in aliens.sprites():
        if alien.rect.bottom > ai_settings.screen_height:
            ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
            break
def check_fleet_edges(ai_settings,aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    #改变左右移动的方向
    ai_settings.fleet_direction *= -1
