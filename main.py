
import pygame as pg
import sys
from os import path
from os import listdir
from game import *
from settings import *
from game import *
import pickle

from sprites import *
from mainMenu import *

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
        self.getHighScore()
        self.loadQuestions()

    def loadQuestions(self):
        displayStats = True #print out question stats
        self.allQuestions = json.load(open('questions/questions.json'))
        self.numberOfQuestions = len(self.allQuestions)
        if displayStats:
            self.displayStats()

    def getHighScore(self):
        try:
            with open('score.dat', 'rb') as file:
                self.highScore = pickle.load(file)
        except:
            self.highScore = 0

    def writeHighScore(self, score):
        if score > self.highScore:
            with open('score.dat', 'wb') as file:
                pickle.dump(score, file)

    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.baseFont = pg.font.SysFont("Roman", BASE_FONT_SIZE)
        self.baseFontUnderline = pg.font.SysFont("Roman", BASE_FONT_SIZE)
        self.baseFontUnderline.set_underline(True)
        self.loadImages()

    def loadImages(self):
        img_folder = path.join(self.game_folder, 'images')
        snd_folder = path.join(self.game_folder, 'sounds')
        self.img_folder = path.join(self.game_folder, 'images')
        self.panel_star = pg.image.load(path.join(img_folder, PANEL_STAR_IMAGE)).convert_alpha()
        self.panel_q_star = pg.image.load(path.join(img_folder, PANEL_Q_STAR_IMAGE)).convert_alpha()
        self.light_jar = pg.image.load(path.join(img_folder,

         LIGHT_IMAGE)).convert_alpha()
        self.correct_text = []
        for image in CORRECT_TEXT_IMAGES:
            self.correct_text.append(pg.image.load(path.join(img_folder, image)).convert_alpha())
        self.correct_sound = pg.mixer.Sound(path.join(snd_folder, CORRECT_SOUND))
        self.background_image =pg.transform.scale( pg.image.load(path.join(img_folder, BACKGROUND_IMAGE)).convert_alpha(), (WIDTH, HEIGHT))
        self.menu_background_image = pg.transform.scale( pg.image.load(path.join(img_folder, BACKGROUND_IMAGE_MENU)).convert_alpha(), (WIDTH, HEIGHT))
        self.question_box_ticked_image = pg.image.load(path.join(img_folder, QUESTION_BOX_TICKED_IMAGE)).convert_alpha()
        self.question_box_hover_image = pg.image.load(path.join(img_folder, QUESTION_BOX_HOVER_IMAGE)).convert_alpha()
        self.question_box_image = pg.image.load(path.join(img_folder, QUESTION_BOX_IMAGE)).convert_alpha()
        self.logo = pg.transform.scale(pg.image.load(path.join(img_folder, LOGO)).convert_alpha(), (460, 350))
        self.numbers_images = []
        for image in NUMBER_IMAGES:
            self.numbers_images.append(pg.transform.scale(pg.image.load(path.join(img_folder, image)).convert_alpha(), (27, 53)))#
        self.icon_images = {}
        for icon_image in ICON_IMAGES:
            self.icon_images[icon_image] = pg.transform.scale(pg.image.load(path.join(img_folder, ICON_IMAGES[icon_image])).convert_alpha(), (175, 175))
        self.incorrect_image = pg.image.load(path.join(img_folder, INCORRECT_IMAGE)).convert_alpha()
        self.tint_image = pg.transform.scale( pg.image.load(path.join(img_folder, TINT_IMAGE)).convert_alpha(), (WIDTH, HEIGHT))

    def new(self):
        self.mouse = Sprite_Mouse_Location(0, 0, self)
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.collidables = pg.sprite.Group()
        self.game = MainMenu(self)

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
        self.game.update()
        for sprite in self.all_sprites:
            sprite.update()

    def newMenu(self):
        self.game = MainMenu(self)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        if isinstance(self.game, MainMenu):
            self.screen.blit(self.menu_background_image, (0, 0))
        else:
            self.screen.blit(self.background_image, (0, 0))

        #self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, MainMenuBackgroundIcon):
                self.screen.blit(sprite.image, (sprite.x, sprite.y))
        self.screen.blit(self.tint_image, (0, 0))
        self.game.draw()
        for sprite in self.all_sprites:
            if not isinstance(sprite, MainMenuBackgroundIcon):
                self.screen.blit(sprite.image, (sprite.x, sprite.y))
        pg.display.flip()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

    def events(self):
        #if pg.sprite.collide_rect(sprite, self.mouse):
        for event in pg.event.get():
            for sprite in self.collidables:
                sprite.isHoveredOn = False
                if pg.sprite.collide_rect(sprite, self.mouse):
                    sprite.isHoveredOn = True
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if isinstance(self.game, Game):
                        self.goToMainMenu()
                    else:
                        self.quit()
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
                if event.button == 1:
                    for sprite in self.collidables:
                        if pg.sprite.collide_rect(sprite, self.mouse):
                            sprite.clicked = True
                    self.game.checkCollision(self.mouse)

    def goToMainMenu(self):
        self.writeHighScore(self.game.score)
        for sprite in self.all_sprites:
            self.all_sprites.remove(sprite)
            del sprite
        self.game = MainMenu(self)

    def createGame(self, difficulties):
        menu = self.game
        self.game = StandardGame(self, difficulties)
        self.game.isPaused = False
        self.all_sprites = pg.sprite.LayeredUpdates()

    def displayStats(self):
        difficultyCount = {1:0, 2:0, 3:0, 4:0, 5:0}
        for question in self.allQuestions:
            difficultyCount[question['difficulty']] = difficultyCount[question['difficulty']] + 1
        print(difficultyCount)
        categoriesCounts = {}
        for question in self.allQuestions:
            for category in question['categories']:
                if category not in categoriesCounts.keys():
                    categoriesCounts[category] = 1
                else:
                    categoriesCounts[category] = categoriesCounts[category] + 1

        for category in categoriesCounts:
            print(category, ": ", categoriesCounts[category])
        categoriesWithoutIcons = []
        for category in categoriesCounts.keys():
            if category not in self.icon_images.keys():
                categoriesWithoutIcons.append(category)
        #categoriesWithoutIcons.sort()
        print("Categories without Icons: ", categoriesWithoutIcons)
        categoriesWithoutIconsOrdered = {}

        while categoriesWithoutIcons:
            max = 0
            maxCategory = " "
            for category in categoriesCounts:
                if max < categoriesCounts[category] and category in categoriesWithoutIcons:
                    max = categoriesCounts[category]
                    maxCategory = category
            categoriesWithoutIconsOrdered[maxCategory] = max
            categoriesWithoutIcons.remove(maxCategory)
        for category in categoriesWithoutIconsOrdered:
            print(category, ": ", categoriesWithoutIconsOrdered[category])

    def clearAllSprites(self):
        for sprite in self.all_sprites:
            self.all_sprites.remove(sprite)
            del sprite


class Sprite_Mouse_Location(pg.sprite.Sprite):
    def __init__(self,x,y, game):
        pg.sprite.Sprite.__init__(self)
        self.rect = pg.Rect(x, y, 1, 1)
        self.x = self.rect.x
        self.y = self.rect.y

# create the game object
g = Main()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
