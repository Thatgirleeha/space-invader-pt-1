import random
from pathlib import Path
import pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("star wars:Young jedi")
clock = pygame.time.Clock()
assets = Path(__file__).parent / "assets"
def load(name, size):
    return pygame.transform.scale(pygame.image.load(assets / name).convert_alpha(), size)
backgrounds = [load("pic 1.png", (800, 600)), load("pic 2.png", (800, 600))] + [load("pic 3.png", (800, 600)), load("pic 4.png", (800, 600))]
bg_index = 0
last_bg_change = pygame.time.get_ticks()
player = load("player.png", (50, 50))
enemy = load("enemy.png", (50, 50))
bullets = [load("bullet.png", (20, 20))]
font = pygame.font.Font("arial.ttf", 36)
try:
    sounds = {s: pygame.mixer.Sound(assets / f"{s}.wav") for s in ["shoot", "explosion","win", "game_over"]}
except pygame.error:
    sounds = {}
levels = [('EASY', 5, 1), ('NORMAL', 10, 2), ('HARD', 15, 3)]
buttons = [pygame.Rect(350, 200, 100, 50), pygame.Rect(350, 275, 100, 50), pygame.Rect(350, 350, 100, 50)]
selected, state,muted = 0, "menu", False