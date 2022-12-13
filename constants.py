import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 178)
GRAY = (220,220,220)
RED = (255, 17, 16)
CYAN = (164, 255, 173)
PINK = (255, 24, 158)
WALL = (255, 203, 37)
GREEN = (0, 178, 0)
WIN_HEIGHT = 720
WIN_WIDTH = 1200
BLOCK_SIZE = 40
FONT_SIZE = 12
SPEED = 50
diagonal_allowed = False
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()