import os
import pygame

WIDTH = 1500
HEIGHT = 750

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

BG = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT)
)
