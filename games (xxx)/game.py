import pygame
from pygame.locals import *
import math
from random import randint

pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

keys = {
    "top": False,
    "bottom": False,
    "left": False,
    "right": False
}

playerpos = [150, 100]
swords = []
enemy_timer = 100
enemies = []
score = 0
health_p = 194
countdown = 65000

exitcode = 0
exit_code_game_over = 0
exit_code_win = 1

player = pygame.image.load("resources/imagesxxx/dude.png")
background = pygame.image.load("resources/imagesxxx/grass.png")
people = pygame.image.load("resources/imagesxxx/castle.png")
sword_img = pygame.image.load("resources/imagesxxx/bullet.png")
enemy_img = pygame.image.load("resources/imagesxxx/badguy.png")
health_bar = pygame.image.load("resources/imagesxxx/healthbar.png")
health = pygame.image.load("resources/imagesxxx/health.png")
gameover = pygame.image.load("resources/imagesxxx/gameover.png")
win = pygame.image.load("resources/imagesxxx/youwin.png")

# pygame.mixer.init()
# hit_people_sound = pygame.mixer.Sound("resources/audio/explode.wav")
# hit_enemy_sound = pygame.mixer.Sound("resources/audio/enemy.wav")
# sword_sound = pygame.mixer.Sound("resources/audio/shoot.wav")
# hit_people_sound.set_volume(0.05)
# hit_enemy_sound.set_volume(0.05)
# sword_sound.set_volume(0.05)
#
# pygame.mixer.music.load("resources/audio/moonlight.wav")
# pygame.mixer.music.play(-1, 0.0)
# pygame.mixer.music.set_volume(0.25)

running = True

while(running):
    screen.fill(0)

    for x in range(int(width/background.get_width()+1)):
        for y in range(int(height/background.get_width()+1)):
            screen.blit(background, (x*100, y*100))

    screen.blit(people, (0, 30))
    screen.blit(people, (0, 135))
    screen.blit(people, (0, 240))
    screen.blit(people, (0, 345))

    mousepos = pygame.mouse.get_pos()
    angle_rad = math.atan2(mousepos[1] - (playerpos[1]), mousepos[0] - (playerpos[0]))
    angle_deg = angle_rad * 57.29 #180/pi
    player_rot = pygame.transform.rotate(player, 360 - angle_deg)
    playerpos_rot = (playerpos[0] - player_rot.get_rect().width / 2, playerpos[1] - player_rot.get_rect().height / 2)
    screen.blit(player_rot, playerpos_rot)

    for sword in swords:
        velx = math.cos(sword[0])*10
        vely = math.sin(sword[0])*10
        sword[1] += velx
        sword[2] += vely
        if sword[1] < -50 or sword[1] > width or sword[2] < -50 or sword[2] > height:
            swords.pop(0)
        sword_rot = pygame.transform.rotate(sword_img, 360 - sword[0] * 57.29)
        screen.blit(sword_rot, (sword[1], sword[2]))

    enemy_timer -= 1
    if enemy_timer == 0:
        enemies.append([width,randint(46, height-46)])
        enemy_timer = randint(1, 100)

    enemy_idx = 0
    for enemy in enemies:
        enemy[0] -= 5
        if enemy[0] < -65:
            enemies.pop(enemy_idx)

        enemy_rect = pygame.Rect(enemy_img.get_rect())
        enemy_rect.top = enemy[1]
        enemy_rect.left = enemy[0]

        if enemy_rect.left < 64:
            enemies.pop(enemy_idx)
            health_p -= 20 #damage point
            # hit_people_sound.play()
            print("AAAA!!! OH, NO!")

        sword_idx = 0
        for sword in swords:
            sword_rect = pygame.Rect(sword_img.get_rect())
            sword_rect.top = sword[2]
            sword_rect.left = sword[1]

            if enemy_rect.colliderect(sword_rect):
                score += 1
                enemies.pop(enemy_idx)
                swords.pop(sword_idx)
                # hit_enemy_sound.play()
                print("JLEB!")
                print("Sccore: {}".format(score))
            sword_idx += 1
        enemy_idx += 1

        screen.blit(enemy_img, enemy)

    screen.blit(health_bar, (5, 8))
    for hp in range(health_p):
        screen.blit(health, (hp+8, 11))

    font = pygame.font.Font("resources/font/Wilderness_0.ttf", 24)
    minutes = int((countdown - pygame.time.get_ticks())/60000)
    seconds = int((countdown - pygame.time.get_ticks())/1000%60)
    time_text = "{:02}:{:02}".format(minutes, seconds)
    clock = font.render(time_text, True, (255,255,255))
    text_rect = clock.get_rect()
    text_rect.topright = [630, 8]
    screen.blit(clock, text_rect)

    pygame.display.flip()

    for event in pygame.event.get():
        # exit
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

        # mousebuttondown to summon sword
        if event.type == pygame.MOUSEBUTTONDOWN:
            swords.append([angle_rad, playerpos_rot[0]+32, playerpos_rot[1]+23])
            # sword_sound.play()

        # keydown keyup
        if event.type == pygame.KEYDOWN:
            if event.key == K_w:
                keys["top"] = True
            elif event.key == K_s:
                keys["bottom"] = True
            elif event.key == K_a:
                keys["left"] = True
            elif event.key == K_d:
                keys["right"] = True

        if event.type == pygame.KEYUP:
            if event.key == K_w:
                keys["top"] = False
            elif event.key == K_s:
                keys["bottom"] = False
            elif event.key == K_a:
                keys["left"] = False
            elif event.key == K_d:
                keys["right"] = False


    if keys["top"] and keys["right"]:
        playerpos[1] -= 1
        playerpos[0] += 1
    elif keys["top"] and keys["left"]:
        playerpos[1] -= 1
        playerpos[0] -= 1
    elif keys["bottom"] and keys["right"]:
        playerpos[1] += 1
        playerpos[0] += 1
    elif keys["bottom"] and keys["left"]:
        playerpos[1] += 1
        playerpos[0] -= 1
    elif keys["top"]:
        playerpos[1] -= 3
    elif keys["bottom"]:
        playerpos[1] += 3
    elif keys["left"]:
        playerpos[0] -= 3
    elif keys["right"]:
        playerpos[0] += 3

    # win lose
    if pygame.time.get_ticks() > countdown:
        running = False
        exitcode = exit_code_win
    if health_p <= 0:
        running = False
        exitcode = exit_code_game_over

# show win lose
if exitcode == exit_code_game_over:
    screen.blit(gameover, (0, 0))
else:
    screen.blit(win, (0, 0))

# TAMPILKAN SCORE SMNTRA PRMAINAN

finalscoretext = font.render("Score: {}".format(score), True, (255,255,255))
finalscoretext_rect = finalscoretext.get_rect()
finalscoretext_rect.centerx = screen.get_rect().centerx
finalscoretext_rect.centery = screen.get_rect().centery + 24
screen.blit(finalscoretext, finalscoretext_rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()
