# 1 - Import Library ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import pygame
from pygame.locals import *

# 2 - Initialize the Game ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))


set_index = 0
frame_set_start = set_index*3
frame_set_end = frame_set_start+2

dwell = 200  # number frames to spend on each image


class AnimatedSprite:
    def __init__(self, screen, position, frames):
        self.screen = screen
        self.pos = position
        self.index = 0
        self.frames = frames
        self.rect = self.frames[self.index].get_rect()
        self.dwell_countdown = dwell

    def advanceImage(self):
        self.dwell_countdown -= 1
        if self.dwell_countdown < 0:
            self.dwell_countdown = dwell
            self.index = (self.index+1) % (frame_set_end+1)
            if self.index < frame_set_start:
                self.index = frame_set_start
            # print(self.index)

    def draw(self):
        self.screen.blit(self.frames[self.index],(int(self.pos[0]-self.rect.width/2),int(self.pos[1]-self.rect.height/2)))


def strip_from_sheet():
    sheet = pygame.image.load('img/summoner.png').convert()

    r = sheet.get_rect()
    rows = 1
    columns = 3
    img_width = r.w/columns
    img_height = r.h/rows

    frames = []
    for row in range(rows):
        for col in range(columns):
            rect = pygame.Rect(col*img_width, row*img_height,
                               img_width, img_height)
            frames.append(sheet.subsurface(rect))

    return frames


def game():

    running = True

    playerpos = [100, 100]  # initial position for player

    # 3 - Load Game Assets ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # 3.1 - Load Images
    # player = pygame.image.load("img/luigi_higher_res.png")

    frames = strip_from_sheet()

    player = AnimatedSprite(screen, playerpos, frames)

    # 4 - The Game Loop ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    while(running):

        # 5 - Clear the screen ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        screen.fill(0)

        # 6 - Draw the game object ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # screen.blit(player, playerpos)

        player.draw()
        player.advanceImage()

        # 7 - Update the sceeen ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        pygame.display.flip()

        # 8 - Event Loop ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        for event in pygame.event.get():
            # event saat tombol exit diklik
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
