import pygame as pg
from settings import *
import sys
from sprites import Panel, QuestionBox

class MainMenu():
    def __init__(self, main):
        self.main = main
        self.font = pg.font.SysFont("Roman", MENU_FONT_SIZE)
        self.smallerFont = pg.font.SysFont("Roman", MENU_SMALLER_FONT_SIZE)
        self.newGameRect = pg.Rect(10 * TILESIZE, 6 * TILESIZE, 10 * TILESIZE, 2 * TILESIZE + 20)
        self.exitRect = pg.Rect(10 * TILESIZE, 9 * TILESIZE, 10 * TILESIZE, 2 * TILESIZE + 20)
        self.newGameMenuRect = pg.Rect(2 * TILESIZE, 1 * TILESIZE, 26 * TILESIZE, 15 * TILESIZE)
        self.startGameRect = pg.Rect(16 * TILESIZE, 13 * TILESIZE, 10 * TILESIZE, 2 * TILESIZE)
        self.menu = "main"

    def update(self):
        pass

    def draw(self):
        if self.menu == "main":
            self.drawMainMenuPanels()
        elif self.menu == "newGame":
            self.drawNewGameMenu()


    def drawNewGameMenu(self):
        pg.draw.rect(self.main.screen, PALETTE_1[1], self.newGameMenuRect)
        difficulyText = self.smallerFont.render("Include difficuly levels (1 is easy - 5 dificult): ", True, WHITE)
        self.main.screen.blit(difficulyText, (3 * TILESIZE, 2 * TILESIZE))
        for questionBox in self.questionBoxes:
            if questionBox.isHoveredOn:
                self.main.screen.blit(self.main.question_box_hover_image, (questionBox.x, questionBox.y))
            levelText = self.smallerFont.render(str(questionBox.difficulty), True, WHITE)
            self.main.screen.blit(levelText, (questionBox.x + 23, questionBox.y - 20))
        pg.draw.rect(self.main.screen, PALETTE_1[0], self.startGameRect)
        newGameText = self.font.render("NEW GAME", True, WHITE)
        self.main.screen.blit(newGameText, (self.startGameRect.x + TILESIZE * 2.2, self.startGameRect.y + 0.5 * TILESIZE))


    def drawMainMenuPanels(self):
        pg.draw.rect(self.main.screen, PALETTE_1[1], self.newGameRect)
        pg.draw.rect(self.main.screen, PALETTE_1[0], (10 * TILESIZE, 6 * TILESIZE, 10 * TILESIZE, 2 * TILESIZE))
        newGameText = self.font.render("NEW GAME", True, WHITE)
        self.main.screen.blit(newGameText, (10 * TILESIZE * 1.5 - (self.font.size("NEW GAME")[0]) / 2, 7 * TILESIZE - (self.font.size("NEW GAME")[1]) / 2))

        pg.draw.rect(self.main.screen, PALETTE_1[1], self.exitRect)
        pg.draw.rect(self.main.screen, PALETTE_1[0], (10 * TILESIZE, 9 * TILESIZE, 10 * TILESIZE, 2 * TILESIZE))
        newGameText = self.font.render("EXIT", True, WHITE)
        self.main.screen.blit(newGameText, (10 * TILESIZE * 1.5 - (self.font.size("EXIT")[0]) / 2, 10 * TILESIZE - (self.font.size("EXIT")[1]) / 2))
        self.main.screen.blit(self.main.logo, (11.2 * TILESIZE, .2 * TILESIZE))
        self.drawNumberOfQuestions()
        self.drawScore()

    def checkCollision(self, mouse):
        if self.menu == "main":
            if mouse.rect.colliderect(self.newGameRect):
                self.menu = "newGame"
                self.questionBoxes = [QuestionBox(self.main, 14 * TILESIZE, 2 * TILESIZE, 1), QuestionBox(self.main, 16 * TILESIZE, 2 * TILESIZE, 2), QuestionBox(self.main, 18 * TILESIZE, 2 * TILESIZE, 3), QuestionBox(self.main, 20 * TILESIZE, 2 * TILESIZE, 4), QuestionBox(self.main, 22 * TILESIZE, 2 * TILESIZE, 5)]
            elif mouse.rect.colliderect(self.exitRect):
                pg.quit()
                sys.exit()
        elif self.menu == "newGame":
            if mouse.rect.colliderect(self.startGameRect):
                difficulties = []
                for questionBox in self.questionBoxes:
                    if questionBox.ticked:
                        difficulties.append(questionBox.difficulty)
                self.main.createGame(difficulties)

    def drawNumberOfQuestions(self):
        numberOfQuestions = self.smallerFont.render("Number Of Questions: ", True, WHITE)
        self.main.screen.blit(numberOfQuestions, (3.5 * TILESIZE, 2 * TILESIZE))
        numbersAsString = str(self.main.numberOfQuestions)
        numbers = len(numbersAsString)
        xOffset = 0
        for x in range(0, numbers):
            self.main.screen.blit(self.main.numbers_images[int(numbersAsString[x])], (5 * TILESIZE + xOffset, 3 * TILESIZE))
            xOffset += self.main.numbers_images[x].get_width() + NUMBERS_OFFSET

    def drawScore(self):
        score = self.smallerFont.render("High Score: ", True, WHITE)
        self.main.screen.blit(score, (23 * TILESIZE, 2 * TILESIZE))
        numbersAsString = str(self.main.highScore)
        numbers = len(numbersAsString)
        xOffset = 0
        for x in range(0, numbers):
            self.main.screen.blit(self.main.numbers_images[int(numbersAsString[x])], (24 * TILESIZE + xOffset, 3 * TILESIZE))
            xOffset += self.main.numbers_images[x].get_width() + NUMBERS_OFFSET

    def createGame(self):
        self.main.createGame()
