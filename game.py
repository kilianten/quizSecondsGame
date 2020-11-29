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
        self.colour = self.colour_scheme[0]
        self.startGame()
        self.createLights()
        self.startTime = NORMAL_START_TIME
        self.timeRemaining = NORMAL_START_TIME
        self.lastUpdate = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.lastUpdate > 1000:
            self.timeRemaining -= 1
            self.dimLights()
            self.lastUpdate = pg.time.get_ticks()
        for panel in self.panels:
            if panel.clicked == True and panel.text in self.question["answers"]:
                panel.clicked = False
                self.resetQuestion()
                self.timeRemaining += NORMAL_CORRECT_BONUS
                if self.timeRemaining > NORMAL_START_TIME:
                    self.timeRemaining = NORMAL_START_TIME

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
                self.panels.append(optionPanel(self.main, panelx, panely, option, self.colour))
            self.questionPanel = questionPanel(self.main, (7 * TILESIZE), (6 * TILESIZE), self.question["question"], self.colour)

    def removeExtraOptionsAnswers(self, question):
        dup = dict(question)
        answer = choice(dup["answers"])
        options = list(question["options"])
        while(len(options) > 3):
            options.remove(choice(options))
        options.append(answer)
        shuffle(options)
        return options

    def drawQuestionPanel(self):
        questionPanel = self.questionPanel
        questionPanel.drawRect()
        self.main.screen.blit(questionPanel.image, (questionPanel.x, questionPanel.y))
        questionPanel.drawText()

    def draw(self):
        for panel in self.panels:
            panel.drawRect()
            self.main.screen.blit(panel.image, (panel.x, panel.y))
            panel.drawText()
        self.drawQuestionPanel()
        for light in self.lights:
            if light.isOn:
                light.drawRect()
            self.main.screen.blit(light.image, (light.x, light.y))

    def createLights(self):
        index = 0
        self.lights = []
        while index < WIDTH:
            self.lights.append(LightJar(self.main, index, 0, self.colour))
            index += TILESIZE

    def dimLights(self):
        percentageTimeRemain = self.timeRemaining / NORMAL_START_TIME
        numOfLightsOn = int(percentageTimeRemain * NUM_OF_LIGHTS)
        self.updateColor(percentageTimeRemain)
        for x in range(numOfLightsOn, NUM_OF_LIGHTS):
            self.lights[x].isOn = False
        for x in range(0, numOfLightsOn + 1):
            self.lights[x].isOn = True

    def updateColor(self, percentageRemainingTime):
        if percentageRemainingTime <= 0.25:
            colour = self.colour_scheme[3]
        elif percentageRemainingTime <= 0.5:
            colour = self.colour_scheme[2]
        elif percentageRemainingTime <= 0.75:
            colour = self.colour_scheme[1]
        else:
            colour = self.colour_scheme[0]
        self.colour = colour
        for light in self.lights:
            light.colour = colour
        for panel in self.panels:
            panel.colour = colour
        self.questionPanel.colour = colour

class StandardGame(Game):
    def __init__(self, main):
        super().__init__(main)
