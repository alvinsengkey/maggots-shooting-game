import pygame
from pygame.locals import *
from game3withMenu import game

pygame.init()

font = pygame.font.SysFont('colonna', 35)
menu_sound = pygame.mixer.Sound("resources/audio/Sword4.ogg")

MENU = (255, 244, 230)
MENU_ACTIVE = (232, 235, 94)

click = False


def main_menu(screen, width, height):
    while True:

        screen.fill((0, 0, 0))
        background = pygame.image.load("resources/images/bg_mainmenu.png")
        screen.blit(background, (0, 0))
        title = pygame.image.load("resources/images/title.png")
        title_rect = title.get_rect(center=(width/2, height/2-60))
        screen.blit(title, title_rect)

        mx, my = pygame.mouse.get_pos()

        start = font.render("Start", True, MENU)
        quit = font.render("Quit", True, MENU)
        start_rect = start.get_rect(center=(width/2, height/2+80))
        quit_rect = quit.get_rect(center=(width/2, height/2+130))
        screen.blit(start, start_rect)
        screen.blit(quit, quit_rect)
        if start_rect.collidepoint(mx, my):
            start = font.render("Start", True, MENU_ACTIVE)
            screen.blit(start, start_rect)
            if click:
                menu_sound.play()
                game()
        if quit_rect.collidepoint(mx, my):
            quit = font.render("Quit", True, MENU_ACTIVE)
            screen.blit(quit, quit_rect)
            if click:
                pygame.quit()
                exit(0)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
