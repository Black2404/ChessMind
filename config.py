import pygame

# CONFIG

WIDTH, HEIGHT = 640, 700 #cửa sổ game
SQ_SIZE = WIDTH // 8 #ô cờ
FPS = 30

# Colors
WHITE = (240, 217, 181)
BLACK = (181, 136, 99)
HIGHLIGHT = (106, 162, 70)
RED = (255, 0, 0)
GREEN = (0, 200, 0)

BG_COLOR = (230, 230, 250)
BTN_COLOR = (180, 200, 250)
BTN_HOVER = (100, 140, 220)

# Pygame setup
pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")
CLOCK = pygame.time.Clock()

FONT = pygame.font.SysFont("Arial", 24, bold=True)
BIG_FONT = pygame.font.SysFont("Arial", 48, bold=True)
