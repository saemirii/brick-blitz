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
PADDLE_SPEED = 3




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




background_image = pygame.image.load("BricK Blitz.png").convert_alpha()




# Current game state
current_state = MENU




# High score dictionary for each stage
high_scores = {
  "Jungle Jive": 0,
  "Crumbling Castle": 0,
  "Rainbow Rush": 0
}




# Stage names
stage_names = {
  1: "Jungle Jive",
  2: "Crumbling Castle",
  3: "Rainbow Rush"
}




# Countdown variables
countdown_timer = 0
countdown_font = pygame.font.SysFont(None, 72)




# Functions




def reset_game():
  global score, game_over, ball_dx, ball_dy, bricks, paddle_x, paddle_y
  score = 0
  game_over = False
  reset_ball_position()
  paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2  # Reset paddle position
  paddle_y = SCREEN_HEIGHT - PADDLE_HEIGHT - 10
  set_initial_ball_position()


  ball_dx =  (0.1 + stage)
  ball_dy = -(0.1 + stage)
  bricks = generate_bricks()




def reset_ball_position():
  global ball_x, ball_y
  ball_x = SCREEN_WIDTH // 2
  ball_y = SCREEN_HEIGHT // 2




def set_initial_ball_position():
  global ball_x, ball_y
  ball_x = paddle_x + PADDLE_WIDTH // 2  # Set ball's initial x-position aligned with paddle
  ball_y = paddle_y - BALL_RADIUS  # Set ball's initial y-position just above the paddle




def draw_countdown():
  SCREEN.fill(BLACK)  # Clear the screen
  countdown_text = str((countdown_timer // 60) + 1)
  if countdown_timer // 60 == 0:
      countdown_text = "Go!"
  countdown_surface = countdown_font.render(countdown_text, True, WHITE)
  countdown_rect = countdown_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
  SCREEN.blit(countdown_surface, countdown_rect)




# Create a function to draw the stage name text
def draw_stage_name():
  font = pygame.font.SysFont(None, 48)
  stage_text = font.render(stage_names[stage], True, WHITE)
  text_rect = stage_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
  SCREEN.blit(stage_text, text_rect)




def skip_to_next_stage():
  global stage
  if stage < 3:
      stage += 1
      reset_game()
      set_initial_ball_position()  # Set initial ball position when skipping stages
  else:
      game_over = True




def generate_bricks():
  bricks = []
  rows = 8 + stage * 2
  cols = 10 + stage * 2
  brick_width = (SCREEN_WIDTH - BRICK_PADDING * (cols + 1)) // cols
  brick_height = 20 + stage * 3
  for row in range(rows):
      for col in range(cols):
          if stage == 2:
              # Adjust brick layout for Crumbling Castle (castle-like pattern)
              brick = pygame.Rect(
                  col * (brick_width + BRICK_PADDING) + BRICK_PADDING,
                  row * (brick_height + BRICK_PADDING) + BRICK_PADDING,
                  brick_width,
                  brick_height if col % 2 == 0 else brick_height - 5,  # Adjust column heights
              )
              bricks.append((brick, NEON_PINK if col % 2 == 0 else NEON_BLUE))
          elif stage == 3:
              # Adjust brick layout for Pyramid Puzzle (pyramid-like pattern)
              if col >= (rows - row) // 2 and col < cols - (rows - row) // 2:
                  brick = pygame.Rect(
                      col * (brick_width + BRICK_PADDING) + BRICK_PADDING,
                      row * (brick_height + BRICK_PADDING) + BRICK_PADDING,
                      brick_width,
                      brick_height,
                  )
                  bricks.append((brick, random.choice(RAINBOW_COLORS)))  # Assign random rainbow color to bricks




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
  SCREEN.blit(background_image, (0, 0))
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
  # Update ball position if game is not over
  if not game_over:
      ball_x += ball_dx
      ball_y += ball_dy
  # Collision detection with walls
  if ball_x <= 0 or ball_x >= SCREEN_WIDTH:
      ball_dx *= -1
  if ball_y <= 0:
      ball_dy *= -1
  # Collision detection with paddle
  if ball_y + BALL_RADIUS >= paddle_y and ball_y + BALL_RADIUS <= paddle_y + PADDLE_HEIGHT and ball_x >= paddle_x and ball_x <= paddle_x + PADDLE_WIDTH:
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
      # Update high score if current score is higher
      high_scores[stage_names[stage]] = max(high_scores[stage_names[stage]], score)
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




  stage_text = font.render("Stage: " + stage_names[stage], True, WHITE)
  text_rect = stage_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
  SCREEN.blit(stage_text, text_rect)




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




def draw_stage_text():
  font = pygame.font.SysFont(None, 48)
  stage_text = font.render("Stage: " + stage_names[stage], True, WHITE)
  SCREEN.blit(stage_text, (200, 50))




def go_to_main_menu():
  global current_state
  current_state = MENU




def start_countdown():
  global countdown_timer
  countdown_timer = 180  # 3 seconds at 60 frames per second




def draw_countdown():
  SCREEN.fill(BLACK)  # Clear the screen
  countdown_text = str((countdown_timer // 60) + 1)
  if countdown_timer // 60 == 0:
      countdown_text = "Go!"
  countdown_surface = countdown_font.render(countdown_text, True, WHITE)
  countdown_rect = countdown_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
  SCREEN.blit(countdown_surface, countdown_rect)




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
              start_countdown()
          elif event.key == pygame.K_SPACE and current_state == MENU:
              reset_game()
              current_state = GAME
              start_countdown()
          elif event.key == pygame.K_m:
              go_to_main_menu()
          elif event.key == pygame.K_s:
              skip_to_next_stage()
  if current_state == MENU:
      draw_menu()
  elif current_state == GAME:
      if countdown_timer > 0:
          draw_countdown()
          countdown_timer -= 1
          # Reset ball position and velocity during countdown
          #ball_x = SCREEN_WIDTH // 2
          #ball_y = SCREEN_HEIGHT // 2
          #ball_dx = 0
          #ball_dy = 0
          # Reset paddle position during countdown
          #paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
      else:
          draw_stage_text()
          draw_game()
          if len(bricks) == 0:
              if score >= (stage + 1) * 20:
                  high_scores[stage_names[stage]] = max(high_scores[stage_names[stage]], score)
                  skip_to_next_stage()
              else:
                  game_over = True
                  # Update high score if current score is higher
                  high_scores[stage_names[stage]] = max(high_scores[stage_names[stage]], score)
  elif current_state == WIN:
      draw_win()
  pygame.display.flip()




# Quit Pygame
pygame.quit()
