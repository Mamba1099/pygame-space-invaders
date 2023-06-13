import os
import pygame


WIDTH = 1500
HEIGHT = 750

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

BG = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT)
)

FPS = 60

run = True
level = 1
lives = 5
lost = False
lost_count = 0
clock = pygame.time.Clock()
player_vel = 8
enemies = []
wave_length = 5
enemy_vel = 1
laser_vel = 4
player_vel = 8
