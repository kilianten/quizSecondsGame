
import pygame as pg
import sys
from os import path
from os import listdir
from game import *
from settings import *
from game import *
from sprites import *

class Main:
    def __init__(self):
        pg.init()
        pg.font.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        self.isFullScreen = False

    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.baseFont = pg.font.SysFont("Roman", 20)
        self.loadImages()

    def loadImages(self):
        img_folder = path.join(self.game_folder, 'images')
        self.img_folder = path.join(self.game_folder, 'images')
        self.starPanel = pg.image.load(path.join(img_folder, STAR_PANEL_IMAGE)).convert_alpha()

    def new(self):
        self.mouse = Sprite_Mouse_Location(0, 0, self)

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.mouse.rect.x, self.mouse.rect.y = pg.mouse.get_pos()
        self.mouse.x, self.mouse.y =  pg.mouse.get_pos()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        pg.display.flip()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

    def events(self):
        #if pg.sprite.collide_rect(sprite, self.mouse):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_F1:
                    if (self.isFullScreen):
                        #if fullscreen set to window
                        print("Entering Windowed mode")
                        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
                        self.isFullScreen = False
                    else:
                        print("Entering Fullscreen mode")
                        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
                        self.isFullScreen = True
            if event.type == pg.MOUSEBUTTONUP:
                pass
                #if pg.sprite.collide_rect(sprite, self.mouse):

class Sprite_Mouse_Location(pg.sprite.Sprite):
    def __init__(self,x,y, game):
        pg.sprite.Sprite.__init__(self)
        self.rect = pg.Rect(x,y,1,1)
        self.x = self.rect.x
        self.y = self.rect.y

# create the game object
g = Main()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
