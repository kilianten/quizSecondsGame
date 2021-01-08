import pygame as pg
from settings import *
import sys
from sprites import Panel, QuestionBox, MainMenuBackgroundIcon, MenuCategoryIcon
from random import randint

class MainMenu():
    def __init__(self, main):
        self.main = main
        self.font = pg.font.SysFont("Roman", MENU_FONT_SIZE)
        self.smallerFont = pg.font.SysFont("Roman", MENU_SMALLER_FONT_SIZE)
        self.newGameRect = pg.Rect(10 * TILESIZE, 6 * TILESIZE, 10 * TILESIZE, 2 * TILESIZE + 20)
        self.exitRect = pg.Rect(10 * TILESIZE, 9 * TILESIZE, 10 * TILESIZE, 2 * TILESIZE + 20)
        self.newGameMenuRect = pg.Rect(2 * TILESIZE, 1 * TILESIZE, 26 * TILESIZE, 15 * TILESIZE)
        self.startGameRect = pg.Rect(16 * TILESIZE, 13 * TILESIZE, 10 * TILESIZE, 2 * TILESIZE)
        self.backRect = pg.Rect(4 * TILESIZE, 13 * TILESIZE, 10 * TILESIZE, 2 * TILESIZE)
        self.menu = "main"
        self.main.getHighScore()
        self.createCategoryIcons()
        self.questions = self.main.allQuestions.copy()

    def update(self):
        if self.menu == "newGame":
            for sprite in self.newGameMenuCatIcons:
                sprite.update()

    def filterOutCategory(self, category):
        filtered = self.questions.copy()
        for question in self.questions:
            if category in question['categories']:
                filtered.remove(question)
        if len(filtered) >= MIN_NUM_OF_QUESTIONS_TO_PLAY:
            self.questions = filtered
            return True
        return False

    def unfilterCategory(self, category):
        filtered = self.questions.copy()
        for question in self.main.allQuestions:
            if category in question['categories'] and question not in self.questions:
                filtered.append(question)
        self.questions = filtered

    def filterOutDifficulty(self, difficulty):
        filtered = self.questions.copy()
        for question in self.questions:
            if difficulty == question["difficulty"]:
                filtered.remove(question)
        if len(filtered) >= MIN_NUM_OF_QUESTIONS_TO_PLAY:
            self.questions = filtered
            return True
        return False

    def unfilterDifficulty(self, difficulty):
        filtered = self.questions.copy()
        for question in self.main.allQuestions:
            if difficulty == question["difficulty"] and question not in self.questions:
                filtered.append(question)
        self.questions = filtered

    def createCategoryIcons(self):
        self.newGameMenuCatIcons = []
        xOffset = TILESIZE * 5
        for category in list(self.main.icon_images.keys()):
            self.newGameMenuCatIcons.append(MenuCategoryIcon(self.main, xOffset, TILESIZE * 4, category))
            xOffset += NEWGAME_MENU_CATEGORY_ICON_SIZE + 50

    def draw(self):
        if self.menu == "main":
            self.drawMainMenuPanels()
            chance = randint(0, BACKGROUND_ICON_SPAWN_CHANCE)
            if chance == BACKGROUND_ICON_SPAWN_CHANCE:
                MainMenuBackgroundIcon(self.main)
        elif self.menu == "newGame":
            self.drawNewGameMenu()

    def drawNewGameMenu(self):
        pg.draw.rect(self.main.screen, PALETTE_1[1], self.newGameMenuRect)
        difficultyText = self.smallerFont.render("Include difficulty levels (1 is easy - 5 dificult): ", True, WHITE)
        self.main.screen.blit(difficultyText, (3 * TILESIZE, 2 * TILESIZE))
        for questionBox in self.questionBoxes:
            if questionBox.isHoveredOn:
                self.main.screen.blit(self.main.question_box_hover_image, (questionBox.x, questionBox.y))
            levelText = self.smallerFont.render(str(questionBox.difficulty), True, WHITE)
            self.main.screen.blit(levelText, (questionBox.x + 23, questionBox.y - 20))
        pg.draw.rect(self.main.screen, PALETTE_1[0], self.startGameRect)
        newGameText = self.font.render("NEW GAME", True, WHITE)
        self.main.screen.blit(newGameText, (self.startGameRect.x + TILESIZE * 2.2, self.startGameRect.y + 0.5 * TILESIZE))
        pg.draw.rect(self.main.screen, PALETTE_1[0], self.backRect)
        backText = self.font.render("BACK", True, WHITE)
        self.main.screen.blit(backText, (self.backRect.x + TILESIZE * 3.5, self.backRect.y + 0.5 * TILESIZE))
        self.drawCategoryIcons()

    def drawCategoryIcons(self):
        for sprite in self.newGameMenuCatIcons:
            sprite.drawCircle()
            self.main.screen.blit(sprite.image, (sprite.x, sprite.y))
            if sprite.disabled:
                self.main.screen.blit(self.main.disabled_icon_image, (sprite.x - 13, sprite.y - 13))
        for sprite in self.newGameMenuCatIcons:
            sprite.draw()

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
        self.drawVersion()

    def checkCollision(self, mouse):
        if self.menu == "main":
            if mouse.rect.colliderect(self.newGameRect):
                self.menu = "newGame"
                self.main.clearAllSprites()
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
                self.main.createGame(self.questions)
                print("Num of Questions in game", len(self.questions))

            elif mouse.rect.colliderect(self.backRect):
                for sprite in self.main.all_sprites:
                    self.main.all_sprites.remove(sprite)
                    del sprite
                self.main.game = MainMenu(self.main)

    def drawNumberOfQuestions(self):
        numberOfQuestions = self.smallerFont.render("No. Of Questions: ", True, WHITE)
        self.main.screen.blit(numberOfQuestions, (3.9 * TILESIZE, 2 * TILESIZE))
        numbersAsString = str(self.main.numberOfQuestions)
        numbers = len(numbersAsString)
        xOffset = 0
        for x in range(0, numbers):
            self.main.screen.blit(self.main.numbers_images[int(numbersAsString[x])], (4.7 * TILESIZE + xOffset, 3 * TILESIZE))
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

    def drawVersion(self):
        versionText = "Version: " + VERSION
        renderedVersionText = self.smallerFont.render(versionText, True, WHITE)
        self.main.screen.blit(renderedVersionText, (WIDTH - (self.smallerFont.size(versionText)[0]) - 50, HEIGHT - (self.smallerFont.size(versionText)[1]) - 50))

    def createGame(self):
        self.main.createGame()
