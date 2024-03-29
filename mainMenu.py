import pygame as pg
from settings import *
import sys
from sprites import Panel, QuestionBox, MainMenuBackgroundIcon, MenuCategoryIcon, Arrow
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
        self.gamemodeRects = [pg.Rect(4 * TILESIZE, 8 * TILESIZE, 4 * TILESIZE, 1 * TILESIZE), pg.Rect(10 * TILESIZE, 8 * TILESIZE, 4 * TILESIZE, 1 * TILESIZE), pg.Rect(16 * TILESIZE, 8 * TILESIZE, 4 * TILESIZE, 1 * TILESIZE)]
        self.lifeLineRects = [pg.Rect(9.5 * TILESIZE, 10 * TILESIZE, 2 * TILESIZE, 1 * TILESIZE), pg.Rect(11.5 * TILESIZE, 10 * TILESIZE, 2 * TILESIZE, 1 * TILESIZE)]
        self.gamemodes = ["Lives Mode", "Time Mode", "Endless Mode"]
        self.lifeLineOptions = ["On", "Off"]
        self.menu = "main"
        self.main.getHighScore()
        self.createCategoryIcons()
        self.questions = self.main.allQuestions.copy()
        self.disabledCategories = []
        self.disabledDifficulties = []
        self.main.music_channel.unpause()
        self.main.music_channel.play(self.main.music_sound, -1)
        self.main.music_channel.set_volume(.1)
        self.arrow_left = Arrow(main, TILESIZE * 3,  TILESIZE * 4.2, self.main.arrow_left_image, "left")
        self.arrow_right = Arrow(main, TILESIZE * 24,  TILESIZE * 4.2, self.main.arrow_right_image, "right")
        self.currentCategoryStart = 0
        self.gamemodeSelected = 0
        self.lifeLines = 1

    def update(self):
        if self.menu == "newGame":
            for sprite in self.newGameMenuCatIcons:
                sprite.update()
            self.arrow_left.update()
            self.arrow_right.update()

    def filterOutCategory(self, category):
        filtered = self.questions.copy()
        for question in self.questions:
            if category in question['categories']:
                filtered.remove(question)
        if len(filtered) >= MIN_NUM_OF_QUESTIONS_TO_PLAY:
            self.questions = filtered
            self.disabledCategories.append(category)
            return True
        return False

    def unfilterCategory(self, category):
        filtered = self.questions.copy()
        for question in self.main.allQuestions:
            if category in question['categories'] and question not in self.questions:
                if question['difficulty'] not in self.disabledDifficulties:
                    filtered.append(question)
        self.disabledCategories.remove(category)
        self.questions = filtered

    def filterOutDifficulty(self, difficulty):
        filtered = self.questions.copy()
        for question in self.questions:
            if difficulty == question["difficulty"]:
                filtered.remove(question)
        if len(filtered) >= MIN_NUM_OF_QUESTIONS_TO_PLAY:
            self.questions = filtered
            self.disabledDifficulties.append(difficulty)
            return True
        return False

    def unfilterDifficulty(self, difficulty):
        filtered = self.questions.copy()
        for question in self.main.allQuestions:
            if difficulty == question["difficulty"] and question not in self.questions:
                catDisabled = False
                for cat in question['categories']:
                    if cat in self.disabledCategories:
                        catDisabled = True
                if not catDisabled:
                    filtered.append(question)
        self.disabledDifficulties.remove(difficulty)
        self.questions = filtered

    def createCategoryIcons(self):
        self.newGameMenuCatIcons = []
        for category in list(self.main.icon_images.keys()):
            self.newGameMenuCatIcons.append(MenuCategoryIcon(self.main, category))

    def draw(self):
        if self.menu == "main":
            self.drawMainMenuPanels()
            chance = randint(0, BACKGROUND_ICON_SPAWN_CHANCE)
            if chance == BACKGROUND_ICON_SPAWN_CHANCE:
                MainMenuBackgroundIcon(self.main)
        elif self.menu == "newGame":
            self.drawNewGameMenu()

    def drawGamemodeRects(self):
        index = 0
        for rect in self.gamemodeRects:
            gamemodeText = self.font.render(self.gamemodes[index], True, WHITE)
            width = self.font.size(self.gamemodes[index])[0] + 12
            rect.width = width
            if self.gamemodeSelected == index:
                pg.draw.rect(self.main.screen, BLACK, pg.Rect(rect.x - 5, rect.y - 5, rect.width + 10, rect.height + 10))
            pg.draw.rect(self.main.screen, PALETTE_1[0], rect)
            self.main.screen.blit(gamemodeText, (rect.x + 6, rect.y))
            index += 1

    def drawLifeLineRects(self):
        index = 0
        hintsText = self.font.render("LIFELINES: ", True, WHITE)
        self.main.screen.blit(hintsText, (TILESIZE * 4, self.lifeLineRects[0].y - 3))
        for rect in self.lifeLineRects:
            option = self.font.render(self.lifeLineOptions[index], True, WHITE)
            width = self.font.size(self.lifeLineOptions[index])[0] + 12
            rect.width = width
            if self.lifeLines == index:
                pg.draw.rect(self.main.screen, BLACK, pg.Rect(rect.x - 5, rect.y - 5, rect.width + 10, rect.height + 10))
            pg.draw.rect(self.main.screen, PALETTE_1[0], rect)
            self.main.screen.blit(option, (rect.x + 6, rect.y))
            index += 1

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
        self.main.screen.blit(self.arrow_left.image, (self.arrow_left.x, self.arrow_left.y))
        self.main.screen.blit(self.arrow_right.image, (self.arrow_right.x, self.arrow_right.y))
        self.drawGamemodeRects()
        self.drawLifeLineRects()

    def setDisplayedIcons(self):
        for sprite in self.newGameMenuCatIcons:
            sprite.isBeingDisplayed = False
        for spriteIndex in range(0, NUM_OF_MENU_ICONS_TO_DRAW):
            spriteIndex += self.currentCategoryStart
            spriteIndex %= len(self.newGameMenuCatIcons)
            sprite = self.newGameMenuCatIcons[spriteIndex]
            sprite.isBeingDisplayed = True

    def drawCategoryIcons(self):
        #for sprite in self.newGameMenuCatIcons:
        xOffset = TILESIZE * 5
        for spriteIndex in range(0, NUM_OF_MENU_ICONS_TO_DRAW):
            spriteIndex += self.currentCategoryStart
            spriteIndex %= len(self.newGameMenuCatIcons)
            sprite = self.newGameMenuCatIcons[spriteIndex]
            sprite.x = xOffset
            sprite.rect.x = xOffset
            sprite.drawCircle()
            self.main.screen.blit(sprite.image, (xOffset, sprite.y))
            if sprite.disabled:
                self.main.screen.blit(self.main.disabled_icon_image, (xOffset - 13, sprite.y - 13))
            xOffset += NEWGAME_MENU_CATEGORY_ICON_SIZE + 50
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
                self.main.music_channel.fadeout(3000)
                #self.main.music_channel.set_volume(.04)
                self.main.createGame(self.questions, self.gamemodes[self.gamemodeSelected], self.lifeLines)
            elif mouse.rect.colliderect(self.backRect):
                for sprite in self.main.all_sprites:
                    self.main.all_sprites.remove(sprite)
                    del sprite
                self.main.game = MainMenu(self.main)
            for rect in self.gamemodeRects:
                if mouse.rect.colliderect(rect):
                    self.gamemodeSelected = self.gamemodeRects.index(rect)
            for rect in self.lifeLineRects:
                if mouse.rect.colliderect(rect):
                    self.lifeLines = self.lifeLineRects.index(rect)

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
