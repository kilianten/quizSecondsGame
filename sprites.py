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
    def __init__(self, main, x, y, text):
        self.main = main
        self.groups = self.main.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.transform.scale(self.main.panel_star, (512, 128))
        self.x = x
        self.y = y
        self.text = text

    def drawRect(self):
        pg.draw.rect(self.main.screen, PALETTE_1[0], (self.x, self.y, self.image.get_width(), self.image.get_height()))

    def drawText(self):
        textWidthSpace = self.image.get_width() - (MIN_PADDING_OF_PANELS * 2)
        textHeightSpace = self.image.get_height() - (MIN_PADDING_OF_PANELS * 2)
        text = str(self.text)
        text = splitTextIntoLines(textWidthSpace, text, self.main.baseFont)
        lineSpace = len(text) * BASE_FONT_HEIGHT
        yOffset = textHeightSpace / len(text)
        emptySpace = textHeightSpace - BASE_FONT_HEIGHT * len(text)
        for x in range(0, len(text)):
            emptyXSpace = textWidthSpace - self.main.baseFont.size(text[x])[0]
            levelText = self.main.baseFont.render("{}".format(text[x]), False, WHITE)
            self.main.screen.blit(levelText, (self.x  + (emptyXSpace / 2) + MIN_PADDING_OF_PANELS, self.y + (x * BASE_FONT_HEIGHT) + (emptySpace / 2) + (MIN_PADDING_OF_PANELS)))
