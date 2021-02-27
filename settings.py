DARKGREY = (16, 105, 75)
LIGHTGREY = (100, 100, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255,36,0)
GREEN = (157, 193, 131)

WIDTH = 1920   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 1080  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "HighQ Quiz"
BGCOLOR = DARKGREY
TILESIZE = 64

#panels
MIN_PADDING_OF_PANELS = 6
PANEL_BORDER_RADIUS = 3
PANEL_X_OFFSET = TILESIZE * 6
PANEL_Y_OFFSET = TILESIZE * 10
SCORE_BOX_PADDING = 30
HOVER_CATEGORY_PADDING = 10
NEWGAME_MENU_CATEGORY_ICON_SIZE = 160

BASE_FONT_SIZE = 28
BASE_FONT_HEIGHT = 27
MENU_FONT_SIZE = 60
MENU_SMALLER_FONT_SIZE = 35
NUM_OF_MENU_ICONS_TO_DRAW = 6

#Images
PANEL_STAR_IMAGE =  "panelStar.png"
PANEL_Q_STAR_IMAGE = "panelQStar.png"
LIGHT_IMAGE = "light2.png"
CORRECT_TEXT_IMAGES = ["correct1.png", "correct2.png", "correct3.png", "correct4.png", "correct5.png", "correct6.png", "correct7.png", "correct8.png", "correct9.png",  "correct10.png", "correct11.png", "correct12.png", "correct13.png", "correct14.png", "correct15.png", "correct16.png", "correct17.png", "correct18.png", "correct19.png", "correct20.png", "correct21.png", "correct22.png", "correct23.png", "correct24.png", "correct25.png", "correct26.png", "correct27.png", "correct28.png", "correct29.png", "correct30.png", "correct31.png", "correct32.png"]
BACKGROUND_IMAGE = "background.png"
BACKGROUND_IMAGE_MENU = "background2.jpg"
QUESTION_BOX_IMAGE = "questionBox.png"
QUESTION_BOX_TICKED_IMAGE = "questionBoxTicked.png"
QUESTION_BOX_HOVER_IMAGE = "questionBoxHovered-export.png"
LOGO = "logo.png"
QUESTION_COUNTER_IMAGE = "questionCounter.png"
NUMBER_IMAGES = ["0.png", "1.png", "2.png", "3.png", "4.png", "5.png", "6.png", "7.png", "8.png", "9.png"]
ICON_IMAGES = {"science": "icon_science_blur.png", "misc": "icon_misc_blur.png", "geography": "icon_geography_blur.png", "history": "icon_history_blur.png", "film": "icon_film.png", "music": "icon_music.png", "language": "icon_language.png", "art": "icon_art.png", "videogames": "icon_videogames.png", "books": "icon_books.png", "quotes": "icon_language.png"}
INCORRECT_IMAGE = "1pixel.png"
TINT_IMAGE = "tintBackground.png"
DISABLED_ICON_IMAGE = "disabled_icon.png"
ARROW_RIGHT_IMAGE = "arrow_right.png"
ARROW_LEFT_IMAGE = "arrow_left.png"
LIFE_LINE_50_IMAGES = ["lifeLine50.png", "lifeLine501.png", "lifeLine502.png", "lifeLine503.png", "lifeLine504.png", "lifeLine505.png", "lifeLine506.png"]
LIFE_LINE_SWAP_IMAGES = ["lifeLineSwap.png", "lifeLineSwap01.png", "lifeLineSwap02.png", "lifeLineSwap03.png", "lifeLineSwap04.png", "lifeLineSwap05.png"]


#sounds
CORRECT_SOUND = "correct.wav"
INCORRECT_SOUND = "incorrect.wav"
MUSIC_SOUND = "music.wav"
s5050_SOUND = "5050.wav"

#updateTimes
CORRECT_TEXT_UPDATE_TIME = 40
LIFE_LINE_UPDATE_TIME = 50
INCORRECT_COLOUR_UPDATE_TIME = 450
INCORRECT_ANIMATION_DUTATION = 3000
CATEGORY_ICON_ROTATE_SPEED = 100
CATEGORY_ICON_ROTATE_ANGLE = -20
BACKGROUND_ICON_SPAWN_CHANCE = 60

MIN_NUM_OF_QUESTIONS_TO_PLAY = 100


VERSION = "BETA 0.1.0"

#Colorpalettes
PALETTE_1 = [(231, 111, 81, 0), (244, 162, 97), (42, 157, 143), (38, 70, 83)]

ICON_CATEGORY_COLOUR = (92, 168, 181)

NORMAL_START_TIME = 60
NORMAL_CORRECT_BONUS = 10
NORMAL_PUNISHMENT_TIME = 7
NUM_OF_LIGHTS = int(WIDTH / TILESIZE)

NUMBERS_OFFSET = 10
