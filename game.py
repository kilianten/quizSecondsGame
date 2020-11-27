import pygame as pg
from settings import *
from sprites import *
import json
from random import randint
from random import choice
from random import shuffle

class Game():
    def __init__(self, main):
        self.main = main
        self.colour_scheme = PALETTE_1
        self.questions = json.load(open('questions/questions.json'))
        print("Number of Questions: ", len(self.questions))
        self.panels = []
        self.question = ""
        self.startGame()

    def update(self):
        for panel in self.panels:
            if panel.clicked == True and panel.text in self.question["answers"]:
                panel.clicked = False
                self.resetQuestion()

    def resetQuestion(self):
        for panel in self.panels:
            panel.clicked = False
            self.main.all_sprites.remove(panel)
            self.panels.remove(panel)
        self.panels.clear()
        self.getQuesiton()

    def startGame(self):
        self.getQuesiton()

    def getQuesiton(self):
        question = self.questions[randint(0, (len(self.questions) - 1))].copy()
        self.question = question.copy()
        options = list(self.removeExtraOptionsAnswers(question))
        panelx = 0
        panely = 0
        for y in range(0,  (int(len(options) / 2))):
            panely = (TILESIZE) * y + PANEL_Y_OFFSET
            if(int(len(options))  == 2): #If only 2 options increase y to centralize it
                panely += 128
            for x in range(0, 2):
                panelx = (TILESIZE + 512) * x + PANEL_X_OFFSET
                option = choice(options)
                options.remove(option)
                self.panels.append(Panel(self.main, panelx, panely, option))

    def removeExtraOptionsAnswers(self, question):
        dup = dict(question)
        answer = choice(dup["answers"])
        options = list(question["options"])
        while(len(options) > 3):
            options.remove(choice(options))
        options.append(answer)
        shuffle(options)
        return options

    def draw(self):
        for panel in self.panels:
            panel.drawRect()
            self.main.screen.blit(panel.image, (panel.x, panel.y))
            panel.drawText()

class StandardGame(Game):
    def __init__(self, main):
        super().__init__(main)
