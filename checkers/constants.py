import pygame

WIDTH, HEIGHT = 1000, 800
ROWS, COLS = 8, 10
SQUARE_SIZE = WIDTH//COLS

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)

CROWN = pygame.transform.scale(pygame.image.load('assets\\crown.png'), (60, 50))
