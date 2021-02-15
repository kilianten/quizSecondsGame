import pygame as pg
from settings import *
from sprites import *
import json
from random import randint
from random import choice
from random import shuffle

class Game():
    def __init__(self, main, questions):
        self.main = main
        self.colour_scheme = PALETTE_1
        self.allQuestions = self.main.allQuestions
        self.questions = questions
        self.panels = []
        self.question = ""
        self.colour = self.colour_scheme[0]
        self.categoryIcon = CategoryIcon(main, 2 * TILESIZE, 6 * TILESIZE)
        self.startGame()
        self.lastUpdate = pg.time.get_ticks()
        self.isPaused = False
        self.score = 0
        self.correctQuestions = 0
        self.difficulty = 1

    def update(self):
        if self.isPaused == False:
            self.updateTimer()
            for panel in self.panels:
                if panel.clicked == True and panel.text in self.question["answers"]:
                    self.score += self.question["difficulty"] * self.difficulty
                    self.correctQuestions += 1
                    panel.clicked = False
                    self.correctAnswerConsequence()
                    correctAnimation(self.main, 1, 1)
                    self.main.correct_sound.play()
                    panel.colour = GREEN
                elif panel.clicked == True and not panel.text in self.question["answers"]:
                    self.incorrectAnswerConsequence()
                    self.main.incorrect_sound.play()
                    panel.colour = RED
                    for ypanel in self.panels:
                        if ypanel.text in self.question["answers"]:
                            correctPanel = ypanel
                    incorrectAnimation(self.main, 1, 1, panel, correctPanel)

    def updateTimer(self):
        if pg.time.get_ticks() - self.lastUpdate > 1000:
            self.lastUpdate = pg.time.get_ticks()

    def correctAnswerConsequence(self):
        pass

    def incorrectAnswerConsequence(self):
        pass

    def endGame(self):
        self.main.newMenu()

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
                self.panels.append(optionPanel(self.main, panelx, panely, option))
            self.questionPanel = questionPanel(self.main, (7 * TILESIZE), (7 * TILESIZE), self.question["question"])
        self.categoryIcon.changeImage(self.question["categories"])

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
        self.draw_categry_icon()
        self.drawQuestionPanel()
        self.drawScores()
        self.categoryIcon.draw()

    def draw_categry_icon(self):
        categoryIcon = self.categoryIcon
        categoryIcon.drawCircle()
        self.main.screen.blit(categoryIcon.image, (categoryIcon.x, categoryIcon.y))

    def drawScores(self):
        scoreText = self.main.baseFont.render("Score: {}".format(self.score), True, WHITE)
        text = "Score: " + str(self.score)
        pg.draw.rect(self.main.screen, PALETTE_1[1], (5 * TILESIZE - SCORE_BOX_PADDING, 4 * TILESIZE - (SCORE_BOX_PADDING / 2), (self.main.baseFont.size(text)[0]) + 2 * SCORE_BOX_PADDING, (self.main.baseFont.size(text)[1]) + 2 * (SCORE_BOX_PADDING / 2) + 5))
        pg.draw.rect(self.main.screen, PALETTE_1[0], (5 * TILESIZE - SCORE_BOX_PADDING, 4 * TILESIZE - (SCORE_BOX_PADDING / 2), (self.main.baseFont.size(text)[0]) + 2 * SCORE_BOX_PADDING, (self.main.baseFont.size(text)[1]) + 2 * (SCORE_BOX_PADDING / 2)))
        self.main.screen.blit(scoreText, (5 * TILESIZE, 4 * TILESIZE))
        questionsCorrect = self.main.baseFont.render("Correct Answers: {}".format(self.correctQuestions), True, WHITE)
        text = "Correct Answers: " + str(self.correctQuestions)
        pg.draw.rect(self.main.screen, PALETTE_1[1], (21 * TILESIZE - SCORE_BOX_PADDING, 4 * TILESIZE - (SCORE_BOX_PADDING / 2), (self.main.baseFont.size(text)[0]) + 2 * SCORE_BOX_PADDING, (self.main.baseFont.size(text)[1]) + 2 * (SCORE_BOX_PADDING / 2) + 5))
        pg.draw.rect(self.main.screen, PALETTE_1[0], (21 * TILESIZE - SCORE_BOX_PADDING, 4 * TILESIZE - (SCORE_BOX_PADDING / 2), (self.main.baseFont.size(text)[0]) + 2 * SCORE_BOX_PADDING, (self.main.baseFont.size(text)[1]) + 2 * (SCORE_BOX_PADDING / 2)))
        self.main.screen.blit(questionsCorrect, (21 * TILESIZE, 4 * TILESIZE))

    def checkCollision(self, mouse):
        pass

class TimedGame(Game):
    def __init__(self, main, difficulties):
        super().__init__(main, difficulties)
        self.timeRemaining = NORMAL_START_TIME
        self.startTime = NORMAL_START_TIME
        self.createLights()

    def createLights(self):
        index = 0
        self.lights = []
        while index < WIDTH:
            self.lights.append(LightJar(self.main, index, 0, self.colour))
            index += TILESIZE

    def incorrectAnswerConsequence(self):
        super().incorrectAnswerConsequence()
        self.timeRemaining -= NORMAL_PUNISHMENT_TIME

    def correctAnswerConsequence(self):
        super().correctAnswerConsequence()
        self.timeRemaining += NORMAL_CORRECT_BONUS
        if self.timeRemaining > NORMAL_START_TIME:
            self.timeRemaining = NORMAL_START_TIME

    def updateTimer(self):
        if self.timeRemaining < 0:
            self.endGame()
        if pg.time.get_ticks() - self.lastUpdate > 1000:
            self.timeRemaining -= 1
            self.dimLights()
        super().updateTimer()

    def endGame(self):
        if self.main.highScore < self.score:
            self.main.writeHighScore(self.score)
        ## TODO BUTTON TO RETURN TO MENU:
        super().endGame()

    def draw(self):
        super().draw()
        for light in self.lights:
            if light.isOn:
                light.drawRect()
            self.main.screen.blit(light.image, (light.x, light.y))

    def dimLights(self):
        percentageTimeRemain = self.timeRemaining / NORMAL_START_TIME
        numOfLightsOn = int(percentageTimeRemain * NUM_OF_LIGHTS)
        self.updateColour(percentageTimeRemain)
        for x in range(numOfLightsOn, NUM_OF_LIGHTS):
            self.lights[x].isOn = False
        for x in range(0, numOfLightsOn + 1):
            self.lights[x].isOn = True

    def updateColour(self, percentageRemainingTime):
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

class LivesGame(Game):
    def __init__(self, main, difficulties, numOfLives):
        super().__init__(main, difficulties)
        self.livesRemaing = numOfLives

    def incorrectAnswerConsequence(self):
        super().incorrectAnswerConsequence()
        self.livesRemaing -= 1

    def update(self):
        if self.livesRemaing <= 0:
            self.endGame()
        else:
            super().update()

    def endGame(self):
        if self.main.highScore < self.score:
            self.main.writeHighScore(self.score)
        ## TODO BUTTON TO RETURN TO MENU:
        super().endGame()
