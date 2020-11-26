import pygame as pg
from settings import *

class Panel(pg.sprite.Sprite):
    def __init__(self, main, x, y):
        print("creating")
        self.main = main
        self.groups = self.main.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.x = 0
        self.y = 0
        self.image = pg.transform.scale(self.main.panel_star, (512, 128))
