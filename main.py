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
def sound(name):
    if not muted and name in sounds:
        sounds[name].play()
def text(message, y, color='white'):
    img = font.render(str(message), True, color)
    screen.blit(img, img.get_rect(center=(450, y)))
def start():
    global player, shots, enemies, score, lives, frame, state
    player = pygame.Rect(420, 500, 60, 60)
    shots, enemies = [], []
    score, lives, frame, = 0, levels[selected][1], 0
    state = 'PLAY'
running = True
while running:
    clock.tick(60)     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if state == 'MENU' and event.type == pygame.MOUSEMOTION:
            for i, button in enumerate(button):
                if button.collidepoint(event.pos):
                    selected = i
            if state == 'MENU' and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if  buttons [selected].collidepoint(event.pos):
                    start()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.k_m:
                        muted = not muted
                    elif state == 'MENU':
                        if event.key in (pygame.K_UP, pygame.K_w): selected = (selected - 1) % 3
                        if event.key in (pygame.K_DOWN, pygame.K_s): selected = (selected + 1) % 3
                        if event.key == pygame.K_RETURN: start()
                    elif state in ('WIN', 'LOSE') and event.key == pygame.K_RETURN:
                        state = 'MENU'
                    elif event.key == pygame.K_p and state in('PLAY', 'PAUSE'):
                        state = 'PAUSE' if state == 'PLAY' else 'PLAY'

                    elif state == 'PLAY' and event.key == pygame.K_SPACE:

                        shots.append(pygame.Rect(player.centerx - 8, player.top - 24, 16, 34))

                        sound('shoot')    
    #change the space background every five seconds
    if pygame.time.get_ticks() - last_bg_change >= 5000:
        bg_index - (bg_index + 1) % len(backgrounds)
        last_bg_change = pygame.time.get_ticks()
    screen.blit(backgrounds[bg_index], (o, 0))
    if state == 'MENU':
        text('STARFALL DEFENDER', 145)
        text('SELECT DIFFICULTY', 235)
        for i, button in enumerate(buttons):
            if i == selected:
                pygame.draw.rect(screen, "blue", button, border_radius=24)
                pygame.draw.rect(screen, "red", button, 2, border_radius=24)
            text(levels[i][0], button.centery, "beige" if i == selected else "green")
