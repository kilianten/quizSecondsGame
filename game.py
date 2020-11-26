import pygame as pg
from settings import *
from sprites import *
import json

class Game():
    def __init__(self, main):
        self.main = main
        self.panel = Panel(main, 0, 0)
        self.colour_scheme = PALETTE_1
        self.questions = json.load(open('questions/questions.json'))
        print("Number of Questions: ",len(self.questions))

    def getQuesiton(self):
        self.panel = Panel(self, 0, 0)
        print(len(self.questions))

    def draw(self):
        pg.draw.rect(self.main.screen, PALETTE_1[0], (0, 0, self.panel.image.get_width(), self.panel.image.get_height()))

class StandardGame(Game):
    def __init__(self, main):
        super().__init__(main)
