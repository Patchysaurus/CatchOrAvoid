import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Full-screen mode
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Food Frenzy")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Load assets
title_image = pygame.image.load("C:/PatchyCode/Catch or Avoid/assets/title.png")
title_image = pygame.transform.scale(title_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
background_image = pygame.image.load("C:/PatchyCode/Catch or Avoid/assets/background.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
basket_image = pygame.image.load("C:/PatchyCode/Catch or Avoid/assets/gumball.png")
basket_image = pygame.transform.scale(basket_image, (200, 150))
game_over_background = pygame.image.load("C:/PatchyCode/Catch or Avoid/assets/gameover.png")
game_over_background = pygame.transform.scale(game_over_background, (SCREEN_WIDTH, SCREEN_HEIGHT))


# Load assets for more variety
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
    pygame.image.load("C:/PatchyCode/Catch or Avoid/assets/apple.png"),
    pygame.image.load("C:/PatchyCode/Catch or Avoid/assets/banana.png"),
]
bomb_image = pygame.image.load("C:/PatchyCode/Catch or Avoid/assets/bomb.png")

# Scale images as needed
food_images = [pygame.transform.scale(img, (50, 50)) for img in food_images]
trash_images = [pygame.transform.scale(img, (50, 50)) for img in trash_images]
bomb_image = pygame.transform.scale(bomb_image, (50, 50))

pygame.mixer.music.load("C:/PatchyCode/Catch or Avoid/assets/bgm.mp3")
pygame.mixer.music.play(-1)

# Load sound effects
food_catch_sound = pygame.mixer.Sound("C:/PatchyCode/Catch or Avoid/assets/caught.mp3")
trash_catch_sound = pygame.mixer.Sound("C:/PatchyCode/Catch or Avoid/assets/crumple.mp3")
bomb_sound = pygame.mixer.Sound("C:/PatchyCode/Catch or Avoid/assets/bombhiss.mp3")
falling_sound = pygame.mixer.Sound("C:/PatchyCode/Catch or Avoid/assets/drop.mp3")
game_over_sound = pygame.mixer.Sound("C:/PatchyCode/Catch or Avoid/assets/gameover.mp3")


game_over_sound.set_volume(0.8)
food_catch_sound.set_volume(0.7)
trash_catch_sound.set_volume(0.7)
bomb_sound.set_volume(0.9)
falling_sound.set_volume(0.5)

# Welcome Screen
def show_welcome_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Press Enter to play
                    return  # Exit the welcome screen and start the game

        # Draw the title screen
        screen.blit(title_image, (0, 0))

        # Draw "Press ENTER to Play" text
        play_text = font.render("Press ENTER to Play", True, WHITE)
        screen.blit(play_text, (SCREEN_WIDTH // 2 - play_text.get_width() // 2, SCREEN_HEIGHT - 100))

        # Update the display
        pygame.display.flip()
        clock.tick(60)


# Game settings
clock = pygame.time.Clock()
font = pygame.font.Font(None, 48)

basket = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 100, 100, 50)
basket_speed = 15

items = []  # Falling items
item_speed = 3
lives = 3
score = 0


# Function: create_item
def create_item():
    item_type = random.choices(
        ["food", "trash", "bomb"], weights=[60, 30, 10]
    )[0]  # Adjust probabilities
    x_pos = random.randint(50, SCREEN_WIDTH - 50)
    if item_type == "food":
        image = random.choice(food_images)
    elif item_type == "trash":
        image = random.choice(trash_images)
    else:  # Bomb
        image = bomb_image

    item = {
        "rect": pygame.Rect(x_pos, 0, 50, 50),
        "type": item_type,
        "image": image,  # Store the specific image to display
    }
    items.append(item)

# Function: draw_game
def draw_game():
    screen.blit(background_image, (0, 0))
    screen.blit(basket_image, basket)

    for item in items:
        screen.blit(item["image"], item["rect"])  # Draw the correct image

    # Display score and lives
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (20, 20))
    screen.blit(lives_text, (20, 70))

# Function: main_game
def main_game():
    global lives, score, items, item_speed

    running = True
    spawn_timer = 0  # Initialize spawn_timer at the start of the function
    spawn_interval = 30  # Initial spawn interval (in frames)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Quit on ESC key
                    pygame.quit()
                    sys.exit()

        # Basket movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and basket.left > 0:
            basket.move_ip(-basket_speed, 0)
        if keys[pygame.K_RIGHT] and basket.right < SCREEN_WIDTH:
            basket.move_ip(basket_speed, 0)

        # Spawn items at regular intervals
        spawn_timer += 1
        if spawn_timer >= spawn_interval:
            create_item()
            spawn_timer = 0  # Reset spawn_timer after spawning an item

        # Update item positions
        for item in items[:]:
            item["rect"].move_ip(0, item_speed)
            if item["rect"].colliderect(basket):  # Caught item
                items.remove(item)
                if item["type"] == "food":
                    food_catch_sound.play()
                    score += 10
                elif item["type"] == "trash":
                    trash_catch_sound.play()
                    score -= 10
                    lives -= 1
                elif item["type"] == "bomb":
                    bomb_sound.play()
                    lives -= 3
            elif item["rect"].top > SCREEN_HEIGHT:  # Missed item
                items.remove(item)
                if item["type"] == "food":
                    falling_sound.play()
                    lives -= 1

        # Draw everything
        draw_game()
        pygame.display.flip()

        # Check for game over
        if lives <= 0:
            running = False

        # Gradually increase difficulty
        if item_speed < 10:  # Cap the speed increase
            item_speed += 0.0005
        if spawn_interval > 15:  # Reduce spawn interval but cap it
            spawn_interval -= 0.005

        clock.tick(60)

    game_over_screen()


# Game over screen
def game_over_screen():
    """Display the Game Over screen with a background image."""
    screen.blit(game_over_background, (0, 0))  # Draw the Game Over background

    # Game Over message
    score_text = font.render(f"Your Score: {score}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 250))

    # Replay button
    replay_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 350, 200, 50)
    pygame.draw.rect(screen, (0, 128, 0), replay_button_rect)
    replay_text = font.render("Replay", True, WHITE)
    screen.blit(replay_text, (replay_button_rect.x + 50, replay_button_rect.y - 5))

    pygame.display.flip()

    # Wait for the player to click the replay button
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if replay_button_rect.collidepoint(event.pos):
                    return  # Replay the game

# Run Game Loop
def reset_game_variables():
    """Reset game variables for a new game."""
    global lives, score, items, item_speed
    lives = 3
    score = 0
    items = []
    item_speed = 3


def game_loop():
    """Main game loop with welcome screen, gameplay, and game over."""
    while True:
        show_welcome_screen()  # Show the title screen
        reset_game_variables()  # Reset variables before starting a new game
        main_game()  # Run the main game
        game_over_screen()  # Show the game over screen

# Run the game
game_loop()
main_game()
show_welcome_screen()
pygame.quit()
