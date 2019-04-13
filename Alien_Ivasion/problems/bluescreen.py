import pygame
import sys

def run():
    pygame.init()
    blue_screen = pygame.display.set_mode((600,600))
    pygame.display.set_caption('Blue Screen')
    bg_color = (246,255,134)
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        blue_screen.fill(bg_color)
        pygame.display.flip()
run()