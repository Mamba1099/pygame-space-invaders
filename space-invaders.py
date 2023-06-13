import pygame
import random

from settings.config import *
from settings.lasers import *
from settings.ships import *

from game.ship import Ship
from game.player import Player

pygame.font.init()


class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel


def main():
    run = True
    FPS = 60
    level = 1
    lives = 5
    clock = pygame.time.Clock()
    player = Player(200, 450)
    player_vel = 8
    enemies = []
    wave_length = 5
    laser_vel = 4
    enemy_vel = 1
    lost = False
    lost_count = 0
    main_font = pygame.font.SysFont("comicsans", 10)
    lost_font = pygame.font.SysFont("comicsans", 50)

    def redraw_window():
        WIN.blit(BG, (0, 0))
        lives_label = main_font.render(f"lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"level: {level}", 1, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("You lost!!", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))

        pygame.display.update()

    redraw_window()

    while run:
        clock.tick(FPS)

        if lives <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(
                    random.randrange(50, WIDTH - 100),
                    random.randrange(-1500, -100),
                    random.choice(["blue", "red", "green"]),
                )
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        key = pygame.key.get_pressed()
        if key[pygame.K_a] and player.x - player_vel > 0:  # left
            player.x -= player_vel
        if (
            key[pygame.K_d] and player.y + player_vel + player.get_width() < WIDTH
        ):  # right
            player.x += player_vel
        if key[pygame.K_w] and player.x - player_vel > 0:  # up
            player.y -= player_vel
        if key[pygame.K_s] and player.y + player_vel + player.get_height() < HEIGHT:
            player.y += player_vel
        if key[pygame.K_SPACE]:
            player.move_laser(-laser_vel, player_vel)

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_laser(laser_vel, player)
            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)
        player.move_laser(laser_vel, enemies)

        redraw_window()


main()
