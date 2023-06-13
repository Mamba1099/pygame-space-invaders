import pygame

from game.ship import Ship

from settings.ships import BLUE_SPACE_SHIP
from settings.lasers import BLUE_LASER
from settings.config import HEIGHT


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
