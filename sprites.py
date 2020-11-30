import pygame as pg
from settings import *

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
    def __init__(self, main, x, y, text, image, colour):
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
        self.colour = colour

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
            levelText = font.render("{}".format(text[x]), False, WHITE)
            self.main.screen.blit(levelText, (self.x  + (emptyXSpace / 2) + MIN_PADDING_OF_PANELS, self.y + (x * BASE_FONT_HEIGHT) + (emptySpace / 2) + (MIN_PADDING_OF_PANELS)))

class questionPanel(Panel):
    def __init__(self, main, x, y, text, colour):
        super().__init__(main, x, y, text, pg.transform.scale(main.panel_q_star, (960, 128)), colour)

class optionPanel(Panel):
    def __init__(self, main, x, y, text, colour):
        super().__init__(main, x, y, text, pg.transform.scale(main.panel_star, (512, 128)), colour)
        self.clicked = False

    def drawRect(self):
        super().drawRect()
        if self.isHoveredOn == True:
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
