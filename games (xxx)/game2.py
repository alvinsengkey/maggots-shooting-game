import pygame
from pygame.locals import *
import math
from random import randint

pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))



running = True



exitcode = 0
exit_code_game_over = 0
exit_code_win = 1

score = 0
health_p = 194
countdown = 65000

swords = []

enemy_timer = 100
enemies = []

player = pygame.image.load("resources/images/dude.png")
background = pygame.image.load("resources/images/grass.png")
people = pygame.image.load("resources/images/castle.png")
sword_img = pygame.image.load("resources/images/bullet.png")
enemy_img = pygame.image.load("resources/images/badguy.png")
health_bar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
gameover = pygame.image.load("resources/images/gameover.png")
win = pygame.image.load("resources/images/youwin.png")

# audio
pygame.mixer.init()
hit_people_sound = pygame.mixer.Sound("resources/audio/explode.wav")
hit_enemy_sound = pygame.mixer.Sound("resources/audio/enemy.wav")
sword_sound = pygame.mixer.Sound("resources/audio/shoot.wav")
hit_people_sound.set_volume(0.08)
hit_enemy_sound.set_volume(0.08)
sword_sound.set_volume(0.08)

# bg music
pygame.mixer.music.load("resources/audio/moonlight.wav")
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

#PLAYER CLASS
class Player:
    def __init__(self, x, y):
        self.playerpos = [x, y] #[150, 100]
        self.keys = {
            "top": False,
            "bottom": False,
            "left": False,
            "right": False
        }
        self.mousepos = pygame.mouse.get_pos()
        # self.angle_rad = 0
        # self.angle_deg = 0
        # self.playerpos_rot = (0, 0)
        #
        # def rotate(self):
        self.angle_rad = math.atan2(self.mousepos[1] - (self.playerpos[1]), self.mousepos[0] - (self.playerpos[0]))
        self.angle_deg = self.angle_rad * 57.29  # 180/pi
        player_rot = pygame.transform.rotate(player, 360 - self.angle_deg)
        self.playerpos_rot = (self.playerpos[0] - player_rot.get_rect().width / 2, self.playerpos[1] - player_rot.get_rect().height / 2)
        # screen.blit(player_rot, self.playerpos_rot)
        screen.blit(player, (self.playerpos[0], self.playerpos[1]))

    def walk(self):
        if self.keys["top"] and self.keys["right"]:
            self.playerpos[1] -= 1
            self.playerpos[0] += 1
        elif self.keys["top"] and self.keys["left"]:
            self.playerpos[1] -= 1
            self.playerpos[0] -= 1
        elif self.keys["bottom"] and self.keys["right"]:
            self.playerpos[1] += 1
            self.playerpos[0] += 1
        elif self.keys["bottom"] and self.keys["left"]:
            self.playerpos[1] += 1
            self.playerpos[0] -= 1
        elif self.keys["top"]:
            self.playerpos[1] -= 3
        elif self.keys["bottom"]:
            self.playerpos[1] += 3
        elif self.keys["left"]:
            self.playerpos[0] -= 3
        elif self.keys["right"]:
            self.playerpos[0] += 3
# PLAYER CLASS END

# SWORD CLASS
class Sword(Player):
    def __init__(self):
        Player.__init__(self, 150, 100)

    def shoot(self):
        angle = self.angle_rad
        swordx = self.playerpos_rot[0]+32
        swordy = self.playerpos_rot[1]+23

        velx = math.cos(angle) * 10
        vely = math.sin(angle) * 10
        swordx += velx
        swordy += vely
        if swordx < -50 or swordx > width or swordy < -50 or swordy > height:
            self.kill()
        sword_rot = pygame.transform.rotate(sword_img, 360 - angle * 57.29)
        screen.blit(sword_rot, (swordx, swordy))


while(running):
    screen.fill(0)

    for x in range(int(width/background.get_width()+1)):
        for y in range(int(height/background.get_width()+1)):
            screen.blit(background, (x*100, y*100))

    screen.blit(people, (0, 30))
    screen.blit(people, (0, 135))
    screen.blit(people, (0, 240))
    screen.blit(people, (0, 345))

    # blit player
    me = Player(150, 100)
    sword = Sword()


    # for sword in swords:

    # SWORD END

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
            hit_people_sound.play()
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
                hit_enemy_sound.play()
                print("JLEB!")
                print("Sccore: {}".format(score))
            sword_idx += 1
        enemy_idx += 1

        screen.blit(enemy_img, enemy)
    # ENEMY END

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
            # swords.append([angle_rad, playerpos_rot[0]+32, playerpos_rot[1]+23])
            sword.shoot()
            sword_sound.play()

        # keydown keyup
        if event.type == pygame.KEYDOWN:
            if event.key == K_w:
                me.keys["top"] = True
            elif event.key == K_s:
                me.keys["bottom"] = True
            elif event.key == K_a:
                me.keys["left"] = True
            elif event.key == K_d:
                me.keys["right"] = True

        if event.type == pygame.KEYUP:
            if event.key == K_w:
                me.keys["top"] = False
            elif event.key == K_s:
                me.keys["bottom"] = False
            elif event.key == K_a:
                me.keys["left"] = False
            elif event.key == K_d:
                me.keys["right"] = False
    # EVENT END




    # win lose
    if pygame.time.get_ticks() > countdown:
        running = False
        exitcode = exit_code_win
    if health_p <= 0:
        running = False
        exitcode = exit_code_game_over
# GAME LOOP RUNNING END

# show win lose
if exitcode == exit_code_game_over:
    screen.blit(gameover, (0, 0))
else:
    screen.blit(win, (0, 0))

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
