import pygame
import random
import sys
import tkinter as ctk
from tkinter import ttk

# Initialize Pygame
pygame.init()

# Full-screen mode
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Catch or Avoid")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

PIXEL_FONT_PATH = "C:/PatchyCode/Catch or Avoid/assets/ttf/PixelifySans-Regular.ttf"
font = pygame.font.Font(PIXEL_FONT_PATH, 48)

# Load assets
title_image = pygame.image.load("C:/PatchyCode/Catch or Avoid/assets/title.png")
title_image = pygame.transform.scale(title_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
background_image = pygame.image.load("C:/PatchyCode/Catch or Avoid/assets/background.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
basket_image = pygame.image.load("C:/PatchyCode/Catch or Avoid/assets/gumball.png")
basket_image = pygame.transform.scale(basket_image, (200, 150))
game_over_background = pygame.image.load("C:/PatchyCode/Catch or Avoid/assets/gameover.png")
game_over_background = pygame.transform.scale(game_over_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

food_images = [
    pygame.image.load("C:/PatchyCode/Catch or Avoid/assets/pizza.png"),
    pygame.image.load("C:/PatchyCode/Catch or Avoid/assets/donut.png"),
    pygame.image.load("C:/PatchyCode/Catch or Avoid/assets/chicken.png"),
    pygame.image.load("C:/PatchyCode/Catch or Avoid/assets/hamburger.png"),
    pygame.image.load("C:/PatchyCode/Catch or Avoid/assets/hot-dog.png"),
    pygame.image.load("C:/PatchyCode/Catch or Avoid/assets/ice-cream.png"),
    pygame.image.load("C:/PatchyCode/Catch or Avoid/assets/narutomaki.png"),
    pygame.image.load("C:/PatchyCode/Catch or Avoid/assets/steak.png")
]

trash_images = [
    pygame.image.load("C:/PatchyCode/Catch or Avoid/assets/fishbone.png"),
    pygame.image.load("C:/PatchyCode/Catch or Avoid/assets/applebone.png"),
    pygame.image.load("C:/PatchyCode/Catch or Avoid/assets/bananapeel.png"),
]

bomb_image = pygame.image.load("C:/PatchyCode/Catch or Avoid/assets/bomb.png")

food_images = [pygame.transform.scale(img, (50, 50)) for img in food_images]
trash_images = [pygame.transform.scale(img, (50, 50)) for img in trash_images]
bomb_image = pygame.transform.scale(bomb_image, (50, 50))
slowmotion_image = pygame.transform.scale(pygame.image.load("C:/PatchyCode/Catch or Avoid/assets/slowmotion.png"), (60, 50))
magnet_image = pygame.transform.scale(pygame.image.load("C:/PatchyCode/Catch or Avoid/assets/magnet.png"), (60, 50))

pygame.mixer.music.load("C:/PatchyCode/Catch or Avoid/assets/bgm.mp3")
pygame.mixer.music.play(-1)

food_catch_sound = pygame.mixer.Sound("C:/PatchyCode/Catch or Avoid/assets/caught.mp3")
trash_catch_sound = pygame.mixer.Sound("C:/PatchyCode/Catch or Avoid/assets/crumple.mp3")
bomb_sound = pygame.mixer.Sound("C:/PatchyCode/Catch or Avoid/assets/bombhiss.mp3")
falling_sound = pygame.mixer.Sound("C:/PatchyCode/Catch or Avoid/assets/drop.mp3")
game_over_sound = pygame.mixer.Sound("C:/PatchyCode/Catch or Avoid/assets/gameover.mp3")

# Volume settings
game_over_sound.set_volume(0.8)
food_catch_sound.set_volume(0.7)
trash_catch_sound.set_volume(0.7)
bomb_sound.set_volume(0.9)
falling_sound.set_volume(0.5)

# Game settings
clock = pygame.time.Clock()
font = pygame.font.Font(None, 48)

basket = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 100, 100, 50)
basket_speed = 15
missed_food_count = 0
items = []
item_speed = 3

score = 0
high_score = 0

COMBOS = {
    ("pizza", "donut", "ice-cream"): 50,
    ("hamburger", "hot-dog", "chicken"): 75,
}
combo_tracker = []

slow_time_active = False
slow_time_timer = 0

magnet_active = False
magnet_timer = 0

# Welcome Screen
def show_welcome_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

        screen.blit(title_image, (0, 0))
        play_text = font.render("Press ENTER to Play", True, WHITE)
        screen.blit(play_text, (SCREEN_WIDTH // 2 - play_text.get_width() // 2, SCREEN_HEIGHT - 100))

        pygame.display.flip()
        clock.tick(60)

# Game logic functions
def create_item():
    item_type = random.choices(
        ["food", "trash", "bomb", "slow-time", "magnet"], weights=[60, 20, 15, 10, 10]
    )[0]  # Adjust probabilities
    diagonal_chance = random.random()

    if diagonal_chance < 0.1:  # Rare chance for diagonal or line spawn
        x_pos = random.randint(50, SCREEN_WIDTH - 200)  # Constrain x to avoid moving off-screen
        y_pos = random.randint(-150, -50)  # Spawn higher for diagonal effect

        dx = random.choice([-1, 1])  # Random left or right direction
        for i in range(10):  # Create diagonal items
            item = {
                "rect": pygame.Rect(x_pos + i * dx * 20, y_pos + i * 20, 50, 50),  # Diagonal movement
                "type": item_type,
                "image": (
                    random.choice(food_images) if item_type == "food"
                    else random.choice(trash_images) if item_type == "trash"
                    else bomb_image if item_type == "bomb"
                    else slowmotion_image if item_type == "slow-time"
                    else magnet_image
                ),
                "dx": dx,  # Direction for diagonal movement
            }
            items.append(item)
    else:
        x_pos = random.randint(50, SCREEN_WIDTH - 50)  # Normal random horizontal position
        if item_type == "food":
            image = random.choice(food_images)
        elif item_type == "trash":
            image = random.choice(trash_images)
        elif item_type == "bomb":
            image = bomb_image
        elif item_type == "slow-time":
            image = slowmotion_image
        else:  # Magnet
            image = magnet_image

        item = {
            "rect": pygame.Rect(x_pos, 0, 50, 50),
            "type": item_type,
            "image": image,
            "dx": 0,  # No diagonal movement for regular items
        }
        items.append(item)

def check_combo():
    global score, combo_tracker
    for combo, bonus in COMBOS.items():
        if tuple(combo_tracker[-len(combo):]) == combo:
            score += bonus
            combo_tracker = []
            break

def activate_slow_time():
    global slow_time_active, item_speed
    slow_time_active = True
    item_speed /= 2

def activate_magnet():
    global magnet_active
    magnet_active = True

def draw_game():
    screen.blit(background_image, (0, 0))
    screen.blit(basket_image, basket)
    for item in items:
        screen.blit(item["image"], item["rect"])

    score_text = font.render(f"Score: {score}", True, WHITE)
    missed_text = font.render(f"Missed: {missed_food_count}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(score_text, (20, 20))
    screen.blit(missed_text, (20, 70))
    screen.blit(high_score_text, (SCREEN_WIDTH - high_score_text.get_width() - 20, 20))

def main_game():
    global score, items, item_speed, high_score, missed_food_count
    global slow_time_active, slow_time_timer, magnet_active, magnet_timer

    running = True
    spawn_timer = 0
    spawn_interval = 100
    pygame.mixer.music.play(-1)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        mouse_x, _ = pygame.mouse.get_pos()
        basket.centerx = mouse_x

        spawn_timer += 1
        if spawn_timer >= spawn_interval:
            create_item()
            spawn_timer = 0

        for item in items[:]:
            item["rect"].move_ip(0, item_speed)

            if item["rect"].colliderect(basket):
                items.remove(item)
                if item["type"] == "food":
                    food_catch_sound.play()
                    score += 10
                    check_combo()
                elif item["type"] == "trash":
                    trash_catch_sound.play()
                    score -= 10
                elif item["type"] == "bomb":
                    bomb_sound.play()
                    running = False
                elif item["type"] == "slow-time":
                    activate_slow_time()
                elif item["type"] == "magnet":
                    activate_magnet()

            elif item["rect"].top > SCREEN_HEIGHT:
                items.remove(item)
                if item["type"] == "food":
                    missed_food_count += 1
                    falling_sound.play()

        if missed_food_count >= 10:
            running = False

        if score > high_score:
            high_score = score

        draw_game()
        pygame.display.flip()
        clock.tick(60)

    game_over_screen()

def game_over_screen():
    global score, high_score
    game_over_sound.play()
    pygame.mixer.music.stop()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    score = 0
                    main_game()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        screen.blit(game_over_background, (0, 0))
        final_score_text = font.render(f"Final Score: {score}", True, WHITE)
        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        restart_text = font.render("Press ENTER to Restart or ESC to Quit", True, WHITE)

        screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 150))
        screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))

        pygame.display.flip()
        clock.tick(60)

# Start the game
def game_loop():
    show_welcome_screen()
    main_game()

game_loop()

