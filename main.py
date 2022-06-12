import sys
import time

import pygame
import random
from pygame.math import Vector2


class PLAYER:
    def __init__(self):
        self.position = Vector2(9, 15)
        self.direction = Vector2(0, -1)
        self.score = 0
        self.health = 3
        self.wall = pygame.mixer.Sound('Sounds/ouch.wav')

    def draw_bear(self):
        block_rect = pygame.Rect(self.position.x * cell_size, self.position.y * cell_size, cell_size, cell_size)
        screen.blit(bear_sprite, block_rect)

    def move_bear(self):  # Sprawdza czy nie wychodzi za ekran
        if not 0 <= self.position.x + self.direction.x <= cell_number - 1 \
                or not 0 <= self.position.y + self.direction.y <= cell_number - 1:  # Granice okienka
            self.direction *= -1  # "Odbijanie od ściany"
            self.health -= 1
            self.wall.play()
        self.position += self.direction


class ENEMY:
    def __init__(self):
        self.position = Vector2(9, 2)
        self.direction = Vector2(0, 1)

    def draw_enemy(self):
        block_rect = pygame.Rect(self.position.x * cell_size, self.position.y * cell_size, cell_size, cell_size)
        screen.blit(enemy_sprite, block_rect)


class FRUIT:
    def __init__(self):
        self.x = random.randint(0, cell_number - 2)
        self.y = random.randint(0, cell_number - 2)
        self.position = Vector2(self.x, self.y)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.position.x * cell_size, self.position.y * cell_size, cell_size, cell_size)
        screen.blit(fruit_sprite, fruit_rect)


class HEART:
    def __init__(self):
        self.position = Vector2(-1, -1)

    def draw_heart(self):
        heart_rect = pygame.Rect(self.position.x * cell_size, self.position.y * cell_size, cell_size, cell_size)
        screen.blit(heart_sprite, heart_rect)


class POWERSLOW:
    def __init__(self):
        self.position = Vector2(-1, -1)

    def draw_powerslow(self):
        power_rect = pygame.Rect(self.position.x * cell_size, self.position.y * cell_size, cell_size, cell_size)
        screen.blit(powerslow_sprite, power_rect)


class POWERFAST:
    def __init__(self):
        self.position = Vector2(-1, -1)

    def draw_powerfast(self):
        power_rect = pygame.Rect(self.position.x * cell_size, self.position.y * cell_size, cell_size, cell_size)
        screen.blit(powerfast_sprite, power_rect)


class MAIN:
    def __init__(self):
        self.bear = PLAYER()
        self.fruit = FRUIT()
        self.enemy = ENEMY()
        self.heart = HEART()
        self.powerslow = POWERSLOW()
        self.powerfast = POWERFAST()
        self.powerslow_active = False
        self.powerfast_active = False
        self.play = True
        self.timer = 0
        self.control = 0
        self.eat = pygame.mixer.Sound('Sounds/munch.wav')
        self.enemy_hit = pygame.mixer.Sound('Sounds/enemy_hit.wav')
        self.collect = pygame.mixer.Sound('Sounds/pop.wav')

    def update(self):
        self.check_collision()
        self.bear.move_bear()

        if self.timer % 1.5 and not self.powerslow_active:
            self.move_enemy()
        if self.timer % 5 == 0 and self.powerslow_active:
            self.move_enemy()
            if self.control == 5:
                self.powerslow_active = False
                self.control = 0
            self.control += 1

        if self.timer % 132 == 0 and not self.powerfast_active:  # Co jaki czas pojawia się powerslow
            self.powerslow.position = Vector2(random.randint(0, cell_number - 2), random.randint(0, cell_number - 2))
        elif self.timer % 67 == 0 and self.powerfast_active:
            self.powerslow.position = Vector2(random.randint(0, cell_number - 2), random.randint(0, cell_number - 2))

        if self.timer % 194 == 0:  # Co jaki czas pojawia się powerfast
            self.powerfast.position = Vector2(random.randint(0, cell_number - 2), random.randint(0, cell_number - 2))

        if self.timer % 174 == 0 and not self.powerfast_active:  # Co jaki czas pojawia się serce
            self.heart.position = Vector2(random.randint(0, cell_number - 2), random.randint(0, cell_number - 2))
        elif self.timer % 86 == 0 and self.powerfast_active:
            self.heart.position = Vector2(random.randint(0, cell_number - 2), random.randint(0, cell_number - 2))

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.bear.draw_bear()
        self.heart.draw_heart()
        self.powerslow.draw_powerslow()
        self.powerfast.draw_powerfast()
        self.enemy.draw_enemy()
        self.draw_score()
        self.draw_health()
        self.game_over()

    def check_collision(self):  # Kolizja z innymi obiektami
        if self.bear.position == self.enemy.position:  # Kolizja z przeciwnikiem  > niż owoc? + self.bear.direction?
            self.bear.health -= 1
            self.enemy.direction *= -1
            self.powerfast_active = False
            self.enemy_hit.play()
        elif self.bear.position == self.fruit.position:  # Kolizja z owockiem
            global fruit_sprite
            if int(time.time()) % 3 == 0:
                fruit_sprite = pygame.image.load('Graphics/FRUIT.png').convert_alpha()
            if int(time.time()) % 4 == 0:
                fruit_sprite = pygame.image.load('Graphics/WATERMELON.png').convert_alpha()
            if int(time.time()) % 5 == 0:
                fruit_sprite = pygame.image.load('Graphics/BERRIES.png').convert_alpha()
            self.fruit = FRUIT()  # Tworzymy owoc w innym miejscu
            self.bear.score += 1  # Dodajemy 1 do wyniku
            self.eat.play()
        elif self.bear.position == self.powerslow.position:  # Kolizja z powerupem
            self.collect.play()
            self.powerslow.position = Vector2(-1, -1)
            self.powerslow_active = True
        elif self.bear.position == self.powerfast.position:  # Kolizja z powerupem
            self.collect.play()
            self.powerfast.position = Vector2(-1, -1)
            self.powerfast_active = True
        elif self.bear.position == self.heart.position:  # Kolizja z sercem
            self.collect.play()
            self.heart.position = Vector2(-1, -1)
            self.bear.health += 1

    def move_enemy(self):
        distance = self.bear.position - self.enemy.position
        if abs(distance.x) <= abs(distance.y):  # Obecnie priorytet kolumnowy
            if distance.y > 0:
                self.enemy.position += Vector2(0, 1)
            elif distance.y < 0:
                self.enemy.position += Vector2(0, -1)
            else:
                pass
        else:
            if distance.x > 0:
                self.enemy.position += Vector2(1, 0)
            elif distance.x < 0:
                self.enemy.position += Vector2(-1, 0)

    def change_direction(self, key):
        if key == pygame.K_UP:
            self.bear.direction = Vector2(0, -1)
        if key == pygame.K_DOWN:
            self.bear.direction = Vector2(0, 1)
        if key == pygame.K_LEFT:
            self.bear.direction = Vector2(-1, 0)
        if key == pygame.K_RIGHT:
            self.bear.direction = Vector2(1, 0)
        # if key == pygame.K_RETURN:  # Zatrzymywanie do testowania
        #     self.bear.direction = Vector2(0, 0)

    def draw_score(self):
        score_text = "Score: " + str(self.bear.score)
        score_surface = game_font.render(score_text, True, (53, 54, 49))
        score_x = cell_size * cell_number - 60
        score_y = cell_size * cell_number - 40
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        screen.blit(score_surface, score_rect)

    def draw_health(self):
        health_text = "Health: " + str(self.bear.health)
        health_surface = game_font.render(health_text, True, (53, 54, 49))
        health_x = cell_size * cell_number - 160
        health_y = cell_size * cell_number - 40
        health_rect = health_surface.get_rect(center=(health_x, health_y))
        screen.blit(health_surface, health_rect)

    def game_over(self):
        if self.bear.health <= 0:
            lose_text = "You lost!"
            lose_surface = lose_font.render(lose_text, True, (53, 54, 49))
            lose_x = cell_size * cell_number - 400
            lose_y = cell_size * cell_number - 400
            health_rect = lose_surface.get_rect(center=(lose_x, lose_y))
            screen.blit(lose_surface, health_rect)
            self.play = False  # Zatrzymuje input i update

    def start_again(self):
        self.powerfast_active = False
        self.powerslow_active = False
        self.powerfast.position = Vector2(-1, -1)
        self.powerslow.position = Vector2(-1, -1)
        pygame.time.set_timer(SCREEN_UPDATE, 110)
        self.bear = PLAYER()
        self.fruit = FRUIT()
        self.enemy = ENEMY()
        self.play = True


pygame.init()
pygame.display.set_caption('Bear game')  # Tytuł okienka

cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
game_font = pygame.font.Font(None, 32)
lose_font = pygame.font.Font(None, 88)

heart_sprite = pygame.image.load('Graphics/HEART.png').convert_alpha()
bear_sprite = pygame.image.load('Graphics/BEAR.png').convert_alpha()
enemy_sprite = pygame.image.load('Graphics/HEDGEHOG.png').convert_alpha()
grass_sprite = pygame.image.load('Graphics/grass.png').convert_alpha()
powerfast_sprite = pygame.image.load('Graphics/UP.png').convert_alpha()
powerslow_sprite = pygame.image.load('Graphics/DOWN.png').convert_alpha()
fruit_sprite = pygame.image.load('Graphics/FRUIT.png').convert_alpha()

pygame.display.set_icon(bear_sprite)

#bgm = pygame.mixer.Sound('Sounds/bgm.mp3')
#bgm.play()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 100)  # Tutaj można modyfikować szybkość gry (Mniej -> szybciej) [110]

game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE and game.play:
            game.timer += 1
            game.update()
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN) and game.play:
                game.change_direction(event.key)
            if event.key == pygame.K_SPACE and not game.play:  # Spacja -> reset po game_over
                game.start_again()

    board = pygame.Rect(0, 0, cell_number * cell_size, cell_number * cell_size)
    screen.blit(grass_sprite, board)

    game.draw_elements()
    pygame.display.update()
    clock.tick(60)
