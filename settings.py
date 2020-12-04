DARKGREY = (16, 105, 75)
LIGHTGREY = (100, 100, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

WIDTH = 1920   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 1080  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Seconds Quiz"
BGCOLOR = DARKGREY
TILESIZE = 64

#panels
MIN_PADDING_OF_PANELS = 6
PANEL_BORDER_RADIUS = 3
PANEL_X_OFFSET = TILESIZE * 6
PANEL_Y_OFFSET = TILESIZE * 9
SCORE_BOX_PADDING = 30

BASE_FONT_SIZE = 28
BASE_FONT_HEIGHT = 27
MENU_FONT_SIZE = 60

#Images
PANEL_STAR_IMAGE =  "panelStar.png"
PANEL_Q_STAR_IMAGE = "panelQStar.png"
LIGHT_IMAGE = "light2.png"
CORRECT_TEXT_IMAGES = ["correct1.png", "correct2.png", "correct3.png", "correct4.png", "correct5.png", "correct6.png", "correct7.png", "correct8.png", "correct9.png",  "correct10.png", "correct11.png", "correct12.png", "correct13.png", "correct14.png", "correct15.png", "correct16.png", "correct17.png", "correct18.png", "correct19.png", "correct20.png", "correct21.png", "correct22.png", "correct23.png", "correct24.png", "correct25.png", "correct26.png", "correct27.png", "correct28.png", "correct29.png", "correct30.png", "correct31.png", "correct32.png"]
BACKGROUND_IMAGE = "background.png"

#sounds
CORRECT_SOUND = "correct.wav"

#updateTimes
CORRECT_TEXT_UPDATE_TIME = 40

#Colorpalettes
PALETTE_1 = [(231, 111, 81, 0), (244, 162, 97), (42, 157, 143), (38, 70, 83)]

NORMAL_START_TIME = 60
NORMAL_CORRECT_BONUS = 12
NORMAL_PUNISHMENT_TIME = 6
NUM_OF_LIGHTS = int(WIDTH / TILESIZE)
