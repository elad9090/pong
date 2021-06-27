import pygame
import random

old_load = pygame.image.load

def n_load(f):
	return old_load(f"Game/assets/{f}")

pygame.image.load = n_load

# General setup
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

# Main Window
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Global vars
bg_color = pygame.Color('#2F373F')
accent_color = (10, 3, 30)
basic_font = pygame.font.Font('Game/assets/04B_19.TTF', 32)
plob_sound = pygame.mixer.Sound("Game/assets/pong.ogg")
score_sound = pygame.mixer.Sound("Game/assets/score.ogg")
middle_strip = pygame.Rect(screen_width / 2 - 2, 0, 4, screen_height)
intro = True


from .Block import Block
from .GameManager import GameManager, GameManagerMP
from .Player import Player
# from .Ball import Ball


player: Player = None
opponent: Player = None
manager: GameManager = None
