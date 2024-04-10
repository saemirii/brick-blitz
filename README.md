# Brick Blitz

Brick Blitz is a simple brick-breaking game developed in Python using the Pygame library.

## Description

Brick Blitz is a classic arcade-style game where players control a paddle to bounce a ball and break bricks. The goal is to clear all the bricks from the screen while keeping the ball from falling off the bottom of the screen. Each stage presents different challenges with varying brick layouts and paddle sizes.

## Features

- Three stages with increasing difficulty: Jungle Jive, Arctic Adventure, and Cyber Challenge.
- High score tracking for each stage.
- Dynamic ball and paddle properties based on the current stage.
- Ability to reset the game, skip to the next stage, or return to the main menu.
- Colorful and engaging visual design.

## Getting Started

### Prerequisites

- Python 3.x installed on your computer.
- Pygame library installed.

### Installing Pygame

#### For PyCharm:

1. File > Manage IDE Settings > Settings Sync
2. Project: \<filename>
3. Python interpreter > `+` button > install pygame

## Controls

- Use the left and right arrow keys to move the paddle.
- Press 'R' to reset the game and restart the countdown.
- Press 'M' to return to the main menu.
- Press 'S' to skip to the next stage.
- Press 'Q' to quit the game.

## Debugging and Error Logging
#### `start_countdown()`
- to ensure that each 3-second countdown works before each stage begins
- timer functions before stage 1, transitioning from one level to another, and resetting game
- doesn't run whenever stages are skipped
```py
    print("Drawing countdown")  # Added print statement
    print("Countdown Timer:", countdown_timer)  # Print countdown timer value
```

## Stage Customization
### 1. **Define Stage Characteristics**: Edit variables: `stage_names`, `BALL_RADIUS`, `ball_dx`, `ball_dy`, and `PADDLE_WIDTH` respectively

```py
#adding new stage
stage_names[4] = "Jungle Jive"
BALL_RADIUS = 15
ball_dx = 3
ball_dy = -3 
PADDLE_WIDTH = 180
```

**Note**: The lesser the `ball_dx` and `ball_dy` values are, the slower the velocity of the pong ball. 

### 2. Generate Brick Layout: Use the generate_bricks() function 
#### **Generating brick structure for a new stage**
```py
def generate_bricks():
    bricks = []
    # Customize brick layout for stage 4
    # Add code here to define brick arrangement
    return bricks
```

### 3. Removing a Stage
#### Delete a specific stage
```py
del stage_names[3]
```
