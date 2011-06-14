import os


BASE_PATH = os.path.dirname(os.path.dirname(__file__))
MEDIA_PATH = os.path.join(BASE_PATH, 'media')
IMAGE_PATH = os.path.join(MEDIA_PATH, 'img')
SOUND_PATH = os.path.join(MEDIA_PATH, 'sound')

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = (SCREEN_WIDTH, SCREEN_HEIGHT)
FPS = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BOARD_BG = (0, 0, 255)
RED_TILE = (255, 0, 0)
YELLOW_TILE = (255, 255, 0)
TRANSPARENT = (255, 0, 255)

# Menu
MENU_FONT = os.path.join(MEDIA_PATH, "fonts", "inconsolata.otf")
MENU_FONT_SIZE = 20
MENU_FONT_SIZE_ACTIVE = 30
MENU_FONT_COLOR = (0, 0, 255)

# Game
TILES_ACROSS = 7
TILES_DOWN = 6
NECESSARY_CONSEC = 4 # connect FO'
TILE_SIZE = 26
TILE_SPACING = 20
BOARD_WIDTH = (TILES_ACROSS * TILE_SIZE * 2) + ((TILES_ACROSS + 1) * TILE_SPACING)
BOARD_HEIGHT = (TILES_DOWN * TILE_SIZE * 2) + ((TILES_DOWN + 1) * TILE_SPACING)
BOARD_LEFT = (SCREEN_WIDTH - BOARD_WIDTH) / 2
BOARD_RIGHT = BOARD_LEFT + BOARD_WIDTH
BOARD_TOP = 122
BOARD_BOTTOM = BOARD_TOP + BOARD_HEIGHT

# Media

IMAGES = {
    'title': 'title.jpg',
    'main_bg': 'main_bg.png',
    'about': 'about_up.png',
    'dragon1': 'dragon1.gif',
    'dragon2': 'dragon2.gif',
    'arrow': 'arrow.png',
    'about_down': 'about_down.png',
}
SOUNDS = {
    'button': 'button.wav',
    'button_press': 'button2.wav',
    'win': 'win.wav',
}
MUSIC = {
    'intro': 'intro.ogg',
}
