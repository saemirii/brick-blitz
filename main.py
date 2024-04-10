import pygame
import random

# Initialize Pygame
pygame.init()

# Set screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brick Blitz")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
NEON_PINK = (255, 105, 180)
NEON_BLUE = (0, 191, 255)
RAINBOW_COLORS = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 128, 0), (0, 0, 255), (75, 0, 130), (238, 130, 238)]

# Game states
MENU = 0
GAME = 1
WIN = 2

# Paddle dimensions
PADDLE_WIDTH = 200
PADDLE_HEIGHT = 10
PADDLE_COLOR = BLUE
PADDLE_SPEED = 10

# Ball dimensions
BALL_RADIUS = 10
BALL_COLOR = RED

# Brick dimensions
BRICK_PADDING = 5

# Initialize paddle position
paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
paddle_y = SCREEN_HEIGHT - PADDLE_HEIGHT - 10

# Initialize ball position and speed
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2
ball_dx = 0
ball_dy = 0

# Initialize bricks
bricks = []

# Game variables
score = 0
stage = 1
game_over = False
win = False

# Current game state
current_state = MENU

# High score dictionary for each stage
high_scores = {
    "Jungle Jive": 0,
    "Arctic Adventure": 0,
    "Cyber Challenge": 0
}

# Stage names
stage_names = {
    1: "Jungle Jive",
    2: "Arctic Adventure",
    3: "Cyber Challenge"
}

# Functions

def reset_ball_position():
    global ball_x, ball_y
    ball_x = SCREEN_WIDTH // 2
    ball_y = SCREEN_HEIGHT // 2

def reset_game():
    global score, game_over, ball_dx, ball_dy, bricks, paddle_x, paddle_y
    score = 0
    game_over = False
    reset_ball_position()
    paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2  # Reset paddle position
    paddle_y = SCREEN_HEIGHT - PADDLE_HEIGHT - 10
    if stage == 1:
        ball_dx = random.choice([-1, 1]) * (2 + stage)
        ball_dy = -(2 + stage)
    elif stage == 2:
        ball_dx = random.choice([-1, 1]) * 4
        ball_dy = -4
    elif stage == 3:
        ball_dx = random.choice([-1, 1]) * 6
        ball_dy = -6
    bricks = generate_bricks()

def generate_bricks():
    bricks = []
    rows = 8 + stage * 2
    cols = 10 + stage * 2
    brick_width = (SCREEN_WIDTH - BRICK_PADDING * (cols + 1)) // cols
    brick_height = 20 + stage * 3
    for row in range(rows):
        for col in range(cols):
            if stage == 2:
                # Adjust brick layout for Arctic Adventure (castle-like pattern)
                brick = pygame.Rect(
                    col * (brick_width + BRICK_PADDING) + BRICK_PADDING,
                    row * (brick_height + BRICK_PADDING) + BRICK_PADDING,
                    brick_width,
                    brick_height if col % 2 == 0 else brick_height - 5,  # Adjust column heights
                )
                bricks.append((brick, NEON_PINK if col % 2 == 0 else NEON_BLUE))
            elif stage == 3:
                # Adjust brick layout for Cyber Challenge (pyramid shape)
                if col >= (rows - row) // 2 and col < cols - (rows - row) // 2:
                    brick = pygame.Rect(
                        col * (brick_width + BRICK_PADDING) + BRICK_PADDING,
                        row * (brick_height + BRICK_PADDING) + BRICK_PADDING,
                        brick_width,
                        brick_height,
                    )
                    bricks.append((brick, random.choice(RAINBOW_COLORS)))
            else:
                brick = pygame.Rect(
                    col * (brick_width + BRICK_PADDING) + BRICK_PADDING,
                    row * (brick_height + BRICK_PADDING) + BRICK_PADDING,
                    brick_width,
                    brick_height,
                )
                bricks.append((brick, GREEN))
    return bricks

def draw_menu():
    SCREEN.fill(BLACK)
    font = pygame.font.SysFont(None, 48)
    menu_text = font.render("Press SPACE to play", True, WHITE)
    SCREEN.blit(menu_text, (200, SCREEN_HEIGHT // 2))
    # Display high scores for each stage
    stage_text = font.render("High Scores:", True, WHITE)
    SCREEN.blit(stage_text, (200, SCREEN_HEIGHT // 2 + 50))
    for i, (stage_name, high_score) in enumerate(high_scores.items()):
        score_text = font.render(f"{stage_name}: {high_score}", True, WHITE)
        SCREEN.blit(score_text, (200, SCREEN_HEIGHT // 2 + 100 + i * 50))

def draw_game():
    global paddle_x, ball_x, ball_y, ball_dx, ball_dy, score, game_over
    SCREEN.fill(BLACK)
    # Update paddle position
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle_x -= PADDLE_SPEED
    if keys[pygame.K_RIGHT]:
        paddle_x += PADDLE_SPEED
    # Ensure paddle doesn't go out of bounds
    if paddle_x < 0:
        paddle_x = 0
    elif paddle_x > SCREEN_WIDTH - PADDLE_WIDTH:
        paddle_x = SCREEN_WIDTH - PADDLE_WIDTH
    # Update ball position
    ball_x += ball_dx
    ball_y += ball_dy
    # Collision detection with walls
    if ball_x <= 0 or ball_x >= SCREEN_WIDTH:
        ball_dx *= -1
    if ball_y <= 0:
        ball_dy *= -1
    # Collision detection with paddle
    if ball_y >= paddle_y - BALL_RADIUS and ball_x >= paddle_x and ball_x <= paddle_x + PADDLE_WIDTH:
        ball_dy *= -1
    # Collision detection with bricks
    for brick, color in bricks:
        if pygame.Rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2).colliderect(
            brick
        ):
            bricks.remove((brick, color))
            ball_dy *= -1
            score += 1
    # Check if the ball falls off the bottom of the screen
    if ball_y > SCREEN_HEIGHT:
        game_over = True
    # Draw paddle
    pygame.draw.rect(SCREEN, PADDLE_COLOR, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    # Draw ball
    pygame.draw.circle(SCREEN, BALL_COLOR, (ball_x, ball_y), BALL_RADIUS)
    # Draw bricks
    for brick, color in bricks:
        pygame.draw.rect(SCREEN, color, brick)
    # Display score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    SCREEN.blit(score_text, (10, 10))
    # Display "You lose" text if game over
    if game_over:
        lose_text = font.render("You lose! Press 'R' to play again or 'Q' to quit.", True, WHITE)
        SCREEN.blit(lose_text, (200, SCREEN_HEIGHT // 2))

def draw_win():
    SCREEN.fill(BLACK)
    font = pygame.font.SysFont(None, 48)
    win_text = font.render("Congratulations! You beat Brick Blitz!", True, WHITE)
    SCREEN.blit(win_text, (150, SCREEN_HEIGHT // 2 - 50))
    score_text = font.render(f"Your Score: {score}", True, WHITE)
    SCREEN.blit(score_text, (300, SCREEN_HEIGHT // 2 + 50))

def adjust_stage_properties():
    global BALL_RADIUS, ball_dx, ball_dy, PADDLE_WIDTH
    if stage == 2:
        # Stage 2 (Arctic) adjustments
        BALL_RADIUS = 12
        ball_dx = 4
        ball_dy = -4
        PADDLE_WIDTH = 150
    elif stage == 3:
        # Stage 3 (Cyber) adjustments
        BALL_RADIUS = 8
        ball_dx = 6
        ball_dy = -6
        PADDLE_WIDTH = 100

def draw_stage_text():
    font = pygame.font.SysFont(None, 48)
    stage_text = font.render("Stage: " + stage_names[stage], True, WHITE)
    SCREEN.blit(stage_text, (200, 50))

def go_to_main_menu():
    global current_state
    current_state = MENU

def skip_to_next_stage():
    global stage, game_over
    if stage < 3:
        stage += 1
        reset_game()
    else:
        game_over = True

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_r and game_over:
                reset_game()
                current_state = GAME
            elif event.key == pygame.K_SPACE and current_state == MENU:
                reset_game()
                current_state = GAME
            elif event.key == pygame.K_m:
                go_to_main_menu()
            elif event.key == pygame.K_s:
                skip_to_next_stage()
    if current_state == MENU:
        draw_menu()
    elif current_state == GAME:
        adjust_stage_properties()
        draw_stage_text()
        draw_game()
        if len(bricks) == 0:
            if score >= (stage + 1) * 20:
                high_scores[stage_names[stage]] = max(high_scores[stage_names[stage]], score)
                skip_to_next_stage()
            else:
                game_over = True
    elif current_state == WIN:
        draw_win()
    pygame.display.flip()

# Quit Pygame
pygame.quit()
