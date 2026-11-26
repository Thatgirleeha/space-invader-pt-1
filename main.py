
import pygame
import random
from pathlib import Path
pygame.init()
pygame.mixer.init()
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Star Wars: Young Jedi")
clock = pygame.time.Clock()
FPS = 60
assets = Path(__file__).parent / "assets"
def load_image(name, size):
    image = pygame.image.load(assets / name).convert_alpha()
    return pygame.transform.scale(image, size)
def load_sound(name):
    try:
        return pygame.mixer.Sound(assets / name)
    except pygame.error:
        print("Could not load sound:", name)
        return None
backgrounds = [
    load_image("pic 1.png", (WIDTH, HEIGHT)),
    load_image("pic 2.png", (WIDTH, HEIGHT)),
    load_image("pic 3.png", (WIDTH, HEIGHT)),
    load_image("pic 4.png", (WIDTH, HEIGHT))
]
player_img = load_image("player.png", (60, 60))
enemy_img = load_image("enemy-1.png", (55, 55))
bullet_img = load_image("bullet.png", (20, 20))
shoot_sound = load_sound("shoot.s.mp3")
win_sound = load_sound("winner sound.mp3")
game_over_sound = load_sound("game over sound.mp3")
background_sound = load_sound("bg-sound.mp3")
font = pygame.font.SysFont("arial", 32, bold=True)
small_font = pygame.font.SysFont("arial", 22)
levels = [
    {"name": "EASY", "lives": 5, "speed": 3, "spawn": 60, "target": 500},
    {"name": "NORMAL", "lives": 4, "speed": 5, "spawn": 40, "target": 1000},
    {"name": "HARD", "lives": 3, "speed": 7, "spawn": 25, "target": 1500}
]
buttons = [
    pygame.Rect(325, 240, 150, 55),
    pygame.Rect(325, 315, 150, 55),
    pygame.Rect(325, 390, 150, 55)
]
selected = 0
state = "MENU"
muted = False
player = pygame.Rect(370, 500, 60, 60)
shots = []
enemies = []
score = 0
lives = 5
frame = 0
bg_index = 0
last_bg_change = pygame.time.get_ticks()
shoot_cooldown = 0
def play_sound(sound):
    if not muted and sound is not None:
        sound.play()
def draw_text(message, y, color="white", selected_font=None):
    if selected_font is None:
        selected_font = font
    image = selected_font.render(str(message), True, color)
    rect = image.get_rect(center=(WIDTH // 2, y))
    screen.blit(image, rect)
def start_game():
    global player, shots, enemies, score, lives, frame, state, shoot_cooldown
    player = pygame.Rect(370, 500, 60, 60)
    shots = []
    enemies = []
    score = 0
    lives = levels[selected]["lives"]
    frame = 0
    shoot_cooldown = 0
    state = "PLAY"
def shoot():
    global shoot_cooldown
    if shoot_cooldown == 0:
        bullet = pygame.Rect(player.centerx - 10, player.top - 20, 20, 20)
        shots.append(bullet)
        play_sound(shoot_sound)
        shoot_cooldown = 15
def draw_menu():
    draw_text("STARFALL DEFENDER", 145)
    draw_text("SELECT DIFFICULTY", 200, "yellow", small_font)
    for i, button in enumerate(buttons):
        if i == selected:
            pygame.draw.rect(screen, "blue", button, border_radius=15)
            pygame.draw.rect(screen, "red", button, 3, border_radius=15)
        else:
            pygame.draw.rect(screen, "gray", button, border_radius=15)
        draw_text(levels[i]["name"], button.centery, "white")
    draw_text("Use UP/DOWN arrows to select", 480, "white", small_font)
    draw_text("Press ENTER to start", 515, "white", small_font)
    draw_text("Press M to mute/unmute", 550, "white", small_font)
def update_game():
    global score, lives, frame, state, shoot_cooldown
    settings = levels[selected]
    frame += 1
    if shoot_cooldown > 0:
        shoot_cooldown -= 1
    keys = pygame.key.get_pressed()
    x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
    y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])
    player.x += x * 6
    player.y += y * 6
    player.clamp_ip(screen.get_rect())
    if frame % settings["spawn"] == 0:
        enemy = pygame.Rect(random.randint(0, WIDTH - 55), -60, 55, 55)
        enemies.append(enemy)
    for bullet in shots[:]:
        bullet.y -= 10
        if bullet.bottom < 0:
            shots.remove(bullet)
    for enemy in enemies[:]:
        enemy.y += settings["speed"]
        if enemy.top > HEIGHT:
            enemies.remove(enemy)
            lives -= 1
            continue
        if enemy.colliderect(player):
            enemies.remove(enemy)
            lives -= 1
            continue
        for bullet in shots[:]:
            if enemy.colliderect(bullet):
                enemies.remove(enemy)
                shots.remove(bullet)
                score += 100
                break
    if score >= settings["target"]:
        state = "WIN"
        play_sound(win_sound)
    elif lives <= 0:
        state = "LOSE"
        play_sound(game_over_sound)
def draw_game():
    screen.blit(player_img, player)
    for enemy in enemies:
        screen.blit(enemy_img, enemy)
    for bullet in shots:
        screen.blit(bullet_img, bullet)
    score_image = small_font.render(f"SCORE: {score}", True, "white")
    lives_image = small_font.render(f"LIVES: {max(0, lives)}", True, "white")
    screen.blit(score_image, (20, 15))
    screen.blit(lives_image, (650, 15))
if background_sound is not None and not muted:
    background_sound.play(-1)
running = True
while running:
    clock.tick(FPS)
    current_time = pygame.time.get_ticks()
    if current_time - last_bg_change >= 5000:
        bg_index = (bg_index + 1) % len(backgrounds)
        last_bg_change = current_time
    screen.blit(backgrounds[bg_index], (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                muted = not muted
                if background_sound is not None:
                    if muted:
                        background_sound.stop()
                    else:
                        background_sound.play(-1)
            if state == "MENU":
                if event.key in (pygame.K_UP, pygame.K_w):
                    selected = (selected - 1) % 3
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    selected = (selected + 1) % 3
                elif event.key == pygame.K_RETURN:
                    start_game()
            elif state == "PLAY":
                if event.key == pygame.K_SPACE:
                    shoot()
                elif event.key == pygame.K_p:
                    state = "PAUSE"
            elif state == "PAUSE":
                if event.key == pygame.K_p:
                    state = "PLAY"
            elif state in ("WIN", "LOSE"):
                if event.key == pygame.K_RETURN:
                    state = "MENU"
        if state == "MENU":
            if event.type == pygame.MOUSEMOTION:
                for i, button in enumerate(buttons):
                    if button.collidepoint(event.pos):
                        selected = i
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, button in enumerate(buttons):
                        if button.collidepoint(event.pos):
                            selected = i
                            start_game()
    if state == "MENU":
        draw_menu()
    elif state == "PLAY":
        update_game()
        draw_game()
        draw_text("P = PAUSE", 580, "yellow", small_font)
    elif state == "PAUSE":
        draw_game()
        draw_text("GAME PAUSED", 280, "yellow")
        draw_text("Press P to resume", 330, "white", small_font)
    elif state == "WIN":
        draw_game()
        draw_text("YOU WIN!", 250, "yellow")
        draw_text(f"FINAL SCORE: {score}", 310)
        draw_text("PRESS ENTER FOR MENU", 380, "white", small_font)
    elif state == "LOSE":
        draw_game()
        draw_text("GAME OVER", 250, "red")
        draw_text(f"FINAL SCORE: {score}", 310)
        draw_text("PRESS ENTER FOR MENU", 380, "white", small_font)
    pygame.display.flip()
pygame.quit()
