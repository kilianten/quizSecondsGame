import pygame as pg
from settings import *
from random import choice, randint

def splitTextIntoLines(space, text, font):
    font.size(text)
    text = text.split()
    lines = [""]
    lineCount = 0
    if len(text) == 1:
        return text
    while(text):
        if font.size(lines[lineCount] + text[0])[0] < space:
            lines[lineCount] += text[0] + " "
            text.pop(0)
        else:
            lineCount += 1
            lines.append("")
    return lines

class Panel(pg.sprite.Sprite):
    def __init__(self, main, x, y, text, image):
        self.main = main
        self.groups = self.main.collidables
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = image
        self.x = x
        self.y = y
        self.text = text
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.isHoveredOn = False
        self.colour = PALETTE_1[0]

    def drawRect(self):
        pg.draw.rect(self.main.screen, self.colour, (self.x, self.y, self.image.get_width(), self.image.get_height()))

    def drawText(self):
        if self.isHoveredOn:
            font = self.main.baseFontUnderline
        else:
            font = self.main.baseFont
        textWidthSpace = self.image.get_width() - (MIN_PADDING_OF_PANELS * 2)
        textHeightSpace = self.image.get_height() - (MIN_PADDING_OF_PANELS * 2)
        text = splitTextIntoLines(textWidthSpace, str(self.text), font)
        lineSpace = len(text) * BASE_FONT_HEIGHT
        yOffset = textHeightSpace / len(text)
        emptySpace = textHeightSpace - BASE_FONT_HEIGHT * len(text)
        for x in range(0, len(text)):
            emptyXSpace = textWidthSpace - font.size(text[x])[0]
            levelText = font.render("{}".format(text[x]), True, WHITE)
            self.main.screen.blit(levelText, (self.x  + (emptyXSpace / 2) + MIN_PADDING_OF_PANELS, self.y + (x * BASE_FONT_HEIGHT) + (emptySpace / 2) + (MIN_PADDING_OF_PANELS)))

class questionPanel(Panel):
    def __init__(self, main, x, y, text):
        super().__init__(main, x, y, text, pg.transform.scale(main.panel_q_star, (960, 128)))

class optionPanel(Panel):
    def __init__(self, main, x, y, text):
        super().__init__(main, x, y, text, pg.transform.scale(main.panel_star, (512, 128)))
        self.clicked = False
        self.disabled = False

    def drawText(self):
        if not self.disabled:
            super().drawText()

    def drawRect(self):
        super().drawRect()
        if self.isHoveredOn == True and not self.disabled:
            pg.draw.rect(self.main.screen, WHITE, (self.x, self.y, self.image.get_width(), self.image.get_height()), PANEL_BORDER_RADIUS)

class LightJar(pg.sprite.Sprite):
    def __init__(self, main, x, y, colour):
        self.main = main
        self.image = self.main.light_jar
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.isOn = True
        self.colour = colour

    def drawRect(self):
        pg.draw.rect(self.main.screen, self.colour, (self.x + 16, self.y + 16, self.image.get_width() - 32, self.image.get_height() - 23))

class correctAnimation(pg.sprite.Sprite):
    def __init__(self, main, x, y):
        self.main = main
        self.groups = self.main.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.image = self.main.correct_text[0]
        self.lastUpdate = pg.time.get_ticks()
        self.main.game.isPaused = True

    def update(self):
        if pg.time.get_ticks() - self.lastUpdate > CORRECT_TEXT_UPDATE_TIME:
            currentImage = self.main.correct_text.index(self.image)
            currentImage += 1
            if currentImage < len(self.main.correct_text):
                self.image = self.main.correct_text[currentImage]
                self.lastUpdate = pg.time.get_ticks()
            else:
                self.kill()
                self.main.game.isPaused = False
                self.main.game.resetQuestion()

class incorrectAnimation(pg.sprite.Sprite):
    def __init__(self, main, x, y, panel, correctPanel):
        self.main = main
        self.groups = self.main.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.x = 0
        self.y = 0
        self.image = self.main.incorrect_image
        self.lastUpdate = pg.time.get_ticks()
        self.createTime = pg.time.get_ticks()
        self.main.game.isPaused = True
        panel.colour = RED
        self.correctPanel = correctPanel
        correctPanel.colour = GREEN

    def update(self):
        if pg.time.get_ticks() - self.createTime > INCORRECT_ANIMATION_DUTATION:
            self.main.game.isPaused = False
            self.main.game.resetQuestion()
            self.kill()
        elif pg.time.get_ticks() - self.lastUpdate > INCORRECT_COLOUR_UPDATE_TIME:
            if self.correctPanel.colour == GREEN:
                self.correctPanel.colour = PALETTE_1[0]
            else:
                self.correctPanel.colour = GREEN
            self.lastUpdate = pg.time.get_ticks()

class QuestionBox(pg.sprite.Sprite):
    def __init__(self, main, x, y, difficulty):
        self.main = main
        self.groups = self.main.all_sprites, self.main.collidables
        pg.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.image = self.main.question_box_ticked_image
        self.ticked = True
        self.difficulty = difficulty
        self.isHoveredOn = False
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.clicked = False

    def update(self):
        if self.clicked == True:
            if self.image == self.main.question_box_ticked_image:
                if self.main.game.filterOutDifficulty(self.difficulty):
                    self.image = self.main.question_box_image
                    self.ticked = False
                self.clicked = False
            else:
                self.main.game.unfilterDifficulty(self.difficulty)
                self.image = self.main.question_box_ticked_image
                self.ticked = True
                self.clicked = False

class CategoryIcon(pg.sprite.Sprite):
    def __init__(self, main, x, y, category="misc"):
        self.main = main
        self.groups = self.main.all_sprites, self.main.collidables
        pg.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        if category == "misc":
            self.image = self.main.icon_images["misc"]
            self.category = "misc"
        else:
            self.image = self.main.icon_images[category]
            self.category = category
        self.lastUpdate = pg.time.get_ticks()
        self.isHoveredOn = False
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.isBeingDisplayed = True

    def draw(self):
        if self.isHoveredOn and self.isBeingDisplayed:
            category = self.category.capitalize()
            categoryText = self.main.baseFont.render(category, True, WHITE)
            pg.draw.rect(self.main.screen, (BLACK), (self.main.mouse.x -1, self.main.mouse.y - 40, self.main.baseFont.size(category)[0] + HOVER_CATEGORY_PADDING, self.main.baseFont.size(category)[1] + HOVER_CATEGORY_PADDING))
            pg.draw.rect(self.main.screen, (PALETTE_1[0]), (self.main.mouse.x, self.main.mouse.y - 39, self.main.baseFont.size(category)[0] + HOVER_CATEGORY_PADDING - 2, self.main.baseFont.size(category)[1] + HOVER_CATEGORY_PADDING - 2))
            self.main.screen.blit(categoryText, (self.main.mouse.x + 4, self.main.mouse.y - 36))

    def changeImage(self, categories):
        foundImage = False
        for category in categories:
            if category in list(self.main.icon_images):
                self.image = self.main.icon_images[category]
                self.category = category
                foundImage = True
                break
        if not foundImage:
            self.image = self.main.icon_images["misc"]
            self.category = "misc"

    def drawCircle(self):
        #pg.draw.rect(self.main.screen, (244, 162, 97), (self.x + 16, self.y + 16, self.image.get_width() + 10, self.image.get_height() + 10))
        #pg.draw.rect(self.main.screen, (244, 162, 97), (self.x - 24, self.y, self.image.get_width() + 48, self.image.get_height() + 2))
        #pg.draw.rect(self.main.screen, ICON_CATEGORY_COLOUR, (self.x - 20, self.y, self.image.get_width() + 40, self.image.get_height() + 2))
        #pg.draw.circle(self.main.screen, (255,250,255), (self.x + self.image.get_width() / 2, self.y + self.image.get_height() / 2),  self.image.get_width() / 2 - 10)
        #pg.draw.circle(self.main.screen, ICON_CATEGORY_COLOUR, (self.x + self.image.get_width() / 2, self.y + self.image.get_height() / 2),  self.image.get_width() / 2 + 5)
        pass

class MainMenuBackgroundIcon(pg.sprite.Sprite):
    def __init__(self, main):
        self.main = main
        self.groups = main.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        randomIcon = choice(list(main.icon_images.values()))
        randSize = randint(60, 220)
        self.image = pg.transform.scale(randomIcon, (randSize, randSize))
        self.x = randint(0, WIDTH + self.image.get_width())
        self.y = 0 - self.image.get_height()
        self.lastUpdate = pg.time.get_ticks()
        self.speed = randint(2, 7)

    def update(self):
        self.y += self.speed
        if self.y >= HEIGHT:
            self.main.all_sprites.remove(self)
            del self

class MenuCategoryIcon(CategoryIcon):
    def __init__(self, main, category="misc"):
        super().__init__(main, 0, TILESIZE * 4, category)
        self.main.all_sprites.remove(self)
        self.image = pg.transform.scale(main.icon_images[category], (NEWGAME_MENU_CATEGORY_ICON_SIZE, NEWGAME_MENU_CATEGORY_ICON_SIZE))
        self.clicked = False
        self.disabled = False
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.isBeingDisplayed = False

    def update(self):
        if self.clicked == True:
            self.clicked = False
            if self.disabled == False:
                if self.main.game.filterOutCategory(self.category):
                    self.disabled = True
            else:
                self.main.game.unfilterCategory(self.category)
                self.disabled = False

    def draw(self):
        super().draw()

    def drawCircle(self):
        pg.draw.circle(self.main.screen, PALETTE_1[2], (self.x + self.image.get_width() / 2, self.y + self.image.get_height() / 2),  self.image.get_width() / 2 + 10)

class Arrow(pg.sprite.Sprite):
    def __init__(self, main, x, y, image, direction):
        self.main = main
        self.groups = self.main.collidables
        pg.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.image = image
        self.clicked = False
        self.disabled = False
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.direction = direction

    def update(self):
        if self.clicked == True:
            self.clicked = False
            if self.direction == "left":
                if self.main.game.currentCategoryStart == 0:
                    self.main.game.currentCategoryStart = len(self.main.game.newGameMenuCatIcons) - 1
                else:
                    self.main.game.currentCategoryStart -= 1
            else:
                self.main.game.currentCategoryStart += 1
                self.main.game.currentCategoryStart %= len(self.main.game.newGameMenuCatIcons)
            self.main.game.setDisplayedIcons()

class LifeLine(pg.sprite.Sprite):
    def __init__(self, main, x, y, images):
        self.main = main
        self.groups = self.main.all_sprites, self.main.collidables
        pg.sprite.Sprite.__init__(self, self.groups)
        self.images = images
        self.image = images[0]
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.isHoveredOn = False
        self.clicked = False
        self.used = False
        self.lastUpdate = 0
        self.isDead = False

class LifeLife50(LifeLine):
    def __init__(self, main, x, y):
        super().__init__(main, x, y, main.lifeline50Images)

    def update(self):
        if self.clicked and not self.used:
            self.clicked = False
            self.used = True
            self.lastUpdate = pg.time.get_ticks()
            self.main.game.disableIncorrect(2)
            self.main.s5050_sound.play()
        elif self.used and pg.time.get_ticks() - self.lastUpdate > LIFE_LINE_UPDATE_TIME:
            if self.images.index(self.image) != len(self.images) - 1:
                self.image = self.images[self.images.index(self.image) + 1]
                self.lastUpdate =  pg.time.get_ticks()
            else:
                self.isDead = True
