import pygame
import random

from settings.config import *
from settings.lasers import *
from settings.ships import *

pygame.font.init()


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screeen(self, height):
        return not (self.y <= height and self.y >= 0)

    def colision(self, obj):
        return collide(obj, self)


class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.laser = []
        self.cool_down_counter = 0

    def draw(self, WIN):
        WIN.blit(
            self.ship_img,
            (
                self.x,
                self.y,
            ),
        )
        for lasers in self.laser:
            lasers.draw(WIN)

    def move_laser(self, vel, obj):
        self.COOLDOWN()
        for laser in self.laser:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.laser.remove(laser)

    def COOLDOWN(self):
        if self.cool_down_counter == self.COOLDOWN:
            self.cool_down_counter = 0

        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.laser.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = BLUE_SPACE_SHIP
        self.laser_img = BLUE_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

        def move_lasers(self, vel, objs):
            self.cooldown()
            for lasers in self.laser:
                lasers.move(vel)
                if lasers.off_screen(HEIGHT):
                    self.lasers.remove(lasers)
                else:
                    for obj in objs:
                        if lasers.collision(obj):
                            objs.reomve(obj)
                            self.laser.remove(lasers)


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


def collide(obj1, obj2):
    offset_x = obj2.x + obj1.x
    offset_y = obj2.y + obj2.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


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
