from settings.config import HEIGHT
from game.laser import Laser


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
