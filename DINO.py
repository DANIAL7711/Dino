import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIN_WIDTH = 800
WIN_HEIGHT = 537
GROUND_HEIGHT = 418
DINO_WIDTH = 40
DINO_HEIGHT = 50
CACTUS_WIDTH = 40
CACTUS_HEIGHT = 30
JUMP_STRENGTH = 13
GRAVITY = 0.7
FPS = 90

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CACTUS_GREEN = (34, 139, 34)
BUTTON_COLOR = (255, 0, 0)
BUTTON_HOVER_COLOR = (0, 0, 200)

# Setup display
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Dino Game")

# Load assets
dino_image = pygame.Surface((DINO_WIDTH, DINO_HEIGHT))
dino_image.fill(BLACK)  # Gantikan dengan imej dinosaur
cactus_image = pygame.Surface((CACTUS_WIDTH, CACTUS_HEIGHT))
cactus_image.fill(CACTUS_GREEN)  # Gantikan dengan imej kaktus

# Load images for menu and game background
background_image_menu = pygame.image.load('game.jpg')  # Gambar latar belakang menu
background_image_game = pygame.image.load('background2.jpg')      # Gambar latar belakang permainan

# Game variables
dino_x = 50
dino_y = GROUND_HEIGHT - DINO_HEIGHT
dino_y_velocity = 0
is_jumping = False

cactus_x = WIN_WIDTH
cactus_y = GROUND_HEIGHT - CACTUS_HEIGHT

# Score and level variables
score = 0
level = 1
cactus_speed = 5

clock = pygame.time.Clock()

def draw_window(game_over=False, menu=False):
    if menu:
        # Display menu background
        win.blit(background_image_menu, (0, 0))
        
        # Draw "Play" button
        font = pygame.font.SysFont(None, 74)
        play_text = font.render("Play", True, WHITE)
        play_rect = play_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))
        pygame.draw.rect(win, BUTTON_COLOR, play_rect.inflate(20, 10))
        win.blit(play_text, play_rect)
        
    else:
        # Display game background
        win.blit(background_image_game, (0, 0))
        
        # Draw dinosaur
        win.blit(dino_image, (dino_x, dino_y))
        
        # Draw cactus
        win.blit(cactus_image, (cactus_x, cactus_y))
        
        # Draw ground line
        pygame.draw.line(win, BLACK, (-200, GROUND_HEIGHT), (WIN_WIDTH, GROUND_HEIGHT))
        
        # Draw score and level
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score} Level: {level}", True, BLACK)
        win.blit(score_text, (10, 10))
        
        if game_over:
            game_over_font = pygame.font.SysFont(None, 74)
            game_over_text = game_over_font.render("Game Over", True, BLACK)
            score_text = game_over_font.render(f"Your Score: {score}", True, BLACK)
            win.blit(game_over_text, (WIN_WIDTH // 2 - game_over_text.get_width() // 2, WIN_HEIGHT // 2 - game_over_text.get_height()))
            win.blit(score_text, (WIN_WIDTH // 2 - score_text.get_width() // 2, WIN_HEIGHT // 2 + 50))
    
    pygame.display.update()

def update_level():
    global level, cactus_speed
    level = score // 10 + 1  # Every 10 points increase the level
    cactus_speed = 5 + (level - 1) * 2  # Increase cactus speed with each level

def reset_game():
    global dino_y, dino_y_velocity, is_jumping, cactus_x, score, cactus_speed
    dino_y = GROUND_HEIGHT - DINO_HEIGHT
    dino_y_velocity = 0
    is_jumping = False
    cactus_x = WIN_WIDTH
    score = 0
    update_level()  # Ensure initial speed and level are set

def main_game():
    global dino_y, dino_y_velocity, is_jumping, cactus_x, score, cactus_speed
    
    reset_game()  # Initialize game variables
    run = True
    game_over = False
    
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        
        # Dino jump logic
        if keys[pygame.K_SPACE] and not is_jumping:
            is_jumping = True
            dino_y_velocity = -JUMP_STRENGTH
        
        if is_jumping:
            dino_y += dino_y_velocity
            dino_y_velocity += GRAVITY
            if dino_y >= GROUND_HEIGHT - DINO_HEIGHT:
                dino_y = GROUND_HEIGHT - DINO_HEIGHT
                is_jumping = False
        
        # Move cactus
        cactus_x -= cactus_speed
        if cactus_x < -CACTUS_WIDTH:
            cactus_x = WIN_WIDTH
            score += 1  # Increase score when the cactus is reset
            update_level()  # Update level and cactus speed
        
        # Check collision
        if (dino_x + DINO_WIDTH > cactus_x and
            dino_x < cactus_x + CACTUS_WIDTH and
            dino_y + DINO_HEIGHT > cactus_y):
            game_over = True
            print(f"Game Over! Your score: {score}")
        
        draw_window(game_over)
        
        if game_over:
            pygame.time.wait(3000)  # Wait 3 seconds before returning to menu
            return  # Return to main menu after game over
    
    pygame.quit()

def main():
    global dino_y, dino_y_velocity, is_jumping, cactus_x, score, cactus_speed
    
    while True:
        menu = True
        
        while menu:
            draw_window(menu=True)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # Check if mouse click is within "Play" button
                    font = pygame.font.SysFont(None, 74)
                    play_text = font.render("Play", True, WHITE)
                    play_rect = play_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))
                    
                    if play_rect.collidepoint((mouse_x, mouse_y)):
                        menu = False
        
        main_game()

if __name__ == "__main__":
    main()
