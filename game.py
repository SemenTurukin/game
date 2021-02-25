import pygame
import sys
import os
from pygame import mixer
import random


# Класс группы спрайтов
class SpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def get_event(self, all_sprites):
        for sprite in self:
            sprite.get_event(all_sprites)


pygame.init()
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Space")
icon = pygame.image.load("data/alien.png")
pygame.display.set_icon(icon)
font = pygame.font.Font('freesansbold.ttf', 45)
all_sprite_group = SpriteGroup()
shuttle_group = SpriteGroup()
fireball_group = SpriteGroup()
alien_group = SpriteGroup()
game_over = False


# Функция загрузки изображений
def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


# Функция выхода
def terminate():
    pygame.quit()
    sys.exit()


# Функция открытия начального меню
def start():
    back = pygame.image.load("data/back.png")
    screen.blit(back, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
        pygame.display.update()


# Класс врага и его действия
class Alien(pygame.sprite.Sprite):
    image = load_image("alien.png")

    def __init__(self):
        super().__init__(alien_group)
        self.rect = self.image.get_rect().move(random.randint(0, 755), random.randint(50, 200))
        self.duration = 1
        self.dead = False

    def update(self):
        global game_over
        if 45 < self.rect.x < screen_size[0] - 45:
            self.rect.x += 5 * self.duration
        else:
            self.rect.y += 45
            self.duration = -self.duration
            self.rect.x += 5 * self.duration
        if self.rect.y > 450:
            game_over = True


# Класс снаряда и его действия
class Fireball(pygame.sprite.Sprite):
    image = load_image("fireball.png")

    def __init__(self, x, y):
        super().__init__(fireball_group)
        fireball = self.image
        self.fireball = pygame.transform.scale(fireball, (35, 35))
        self.rect = self.image.get_rect().move(x, y)
        self.dead = False

    def update(self):
        self.rect.y -= 5
        if self.rect.y < 0:
            self.dead = True
        dead_alient = pygame.sprite.spritecollide(self, alien_group, True)
        for alien in dead_alient:
            alien.dead = True
            mixer.music.load("data/explosion.wav")
            mixer.music.play()


# Игрока и его действия
class Shuttle(pygame.sprite.Sprite):
    image = load_image("shuttle.png")

    def __init__(self):
        super().__init__(shuttle_group)
        shuttle = self.image
        self.shuttle = pygame.transform.scale(shuttle, (45, 45))
        self.shuttleX = 350
        self.shuttleY = 500
        self.rect = self.image.get_rect().move(self.shuttleX, self.shuttleY)

    def movingShuttle(self, duration):
        next = self.shuttleX + duration * 5
        if 0 <= next <= screen_size[0]:
            self.shuttleX = next
        self.rect = self.shuttle.get_rect().move(self.shuttleX, self.shuttleY)


# Класс победы (открывает меню победы)
class Win():
    def win():
        background = pygame.image.load("data/backwin.png")
        screen.blit(background, (0, 0))
        score = font.render("Было поражено:" + str(destroyed), True, (255, 255, 255))
        screen.blit(score, (215, 100))
        mixer.music.load("data/win.wav")
        mixer.music.play()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        terminate()
            pygame.display.update()


# Класс поражения (открывает меню поражения)
class GG():
    def gameover():
        background = pygame.image.load("data/backgg.png")
        screen.blit(background, (0, 0))
        score = font.render("Было поражено:" + str(destroyed), True, (255, 255, 255))
        screen.blit(score, (215, 100))
        mixer.music.load("data/gg.wav")
        mixer.music.play()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        terminate()
            pygame.display.update()


# Функция открытия игры и всего игрового цикла
def display():
    background = pygame.image.load("data/background.png")
    global destroyed
    destroyed = 0
    shuttle = Shuttle()
    move = False
    duration = 0
    all_fireball = []
    alient_count = 6
    all_alient = []
    new_alient = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move = True
                    duration = -1
                if event.key == pygame.K_RIGHT:
                    move = True
                    duration = 1
                if event.key == pygame.K_SPACE:
                    all_fireball.append(Fireball(shuttle.shuttleX, shuttle.shuttleY))
                    mixer.music.load("data/fireball.wav")
                    mixer.music.play()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    move = False
                    duration = 0
        if move:
            shuttle.movingShuttle(duration)
        new_alient += 1
        if new_alient % 100 == 0:
            if len(all_alient) < alient_count:
                all_alient.append(Alien())

        screen.blit(background, (0, 0))
        score = font.render("Поражено:" + str(destroyed), True, (255, 255, 255))
        screen.blit(score, (280, 20))
        fireball_group.update()
        for ball in all_fireball:
            if ball.dead:
                all_fireball.remove(ball)
        for alien in all_alient:
            if alien.dead:
                all_alient.remove(alien)
                destroyed += 1
        if destroyed == 25:
            Win.win()
            break
        if game_over:
            GG.gameover()
            break
        alien_group.update()
        alien_group.draw(screen)
        fireball_group.draw(screen)
        shuttle_group.draw(screen)
        pygame.display.update()
        pygame.display.flip()


# Запуск программы
start()
display()