import pygame
import random
import sys


WIDTH, HEIGHT = 440, 480
BLOCK_SIZE = 20

pygame.display.set_caption("Snek and apple")

GRID_WIDTH = WIDTH // BLOCK_SIZE
GRID_HEIGHT = HEIGHT // BLOCK_SIZE

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)


clock = pygame.time.Clock()

# Snake
snake_pos = [[5, 5], [4, 5], [3, 5]]
snake_direction = [1, 0]

# Food
food_pos = [random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)]
food_spawn = True

# Walls
walls = []

# Background
background = pygame.image.load("./assets/snake_background.jpeg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# snake head and body
snake_head = pygame.image.load("./assets/snakeHead.png")
snake_head = pygame.transform.scale(snake_head, (BLOCK_SIZE, BLOCK_SIZE))

snake_body = pygame.image.load("./assets/snakeBody.png")

# Block
block_image = pygame.image.load("./assets/block.jpeg")
block_image = pygame.transform.scale(block_image, (BLOCK_SIZE, BLOCK_SIZE))

# food
food_image = pygame.image.load("./assets/apple.png")


def generate_blocks(level):
    blocks = []
    for _ in range(level):
        while True:
            new_block = [
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1),
            ]
            if (
                new_block not in blocks
                and new_block not in snake_pos
                and new_block != food_pos
            ):
                blocks.append(new_block)
                break
    return blocks


def generate_walls():
    num_walls = random.randint(5, 10)
    for _ in range(num_walls):
        wall = [random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)]
        walls.append(wall)


def draw_game_over(win):
    font = pygame.font.Font(None, 36)
    game_over_text = font.render("Game Over", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    win.blit(game_over_text, game_over_rect)


def main(win, level=1):

    # Snake
    snake_pos = [[5, 5], [4, 5], [3, 5]]
    snake_direction = [1, 0]

    # Food
    food_pos = [random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)]

    # Blocks and level
    food_eaten = 0
    game_over = False

    walls.clear()

    # started game
    game_started = False

    FPS = 10

    # Generate walls
    generate_walls()

    # add game background
    win.blit(background, (0, 0))

    # Game loop
    while not game_over:
        win.blit(background, (0, 0))

        for index, pos in enumerate(snake_pos):

            if index == 0:
                if snake_direction == [1, 0]:
                    head_image = pygame.transform.rotate(snake_head, 90)
                elif snake_direction == [-1, 0]:
                    head_image = pygame.transform.rotate(snake_head, 90)
                elif snake_direction == [0, -1]:
                    head_image = pygame.transform.rotate(snake_head, 180)
                elif snake_direction == [0, 1]:
                    head_image = pygame.transform.rotate(snake_head, 180)
                win.blit(head_image, (pos[0] * BLOCK_SIZE, pos[1] * BLOCK_SIZE))
            else:
                win.blit(snake_body, (pos[0] * BLOCK_SIZE, pos[1] * BLOCK_SIZE))

        # Draw the food
        win.blit(food_image, (food_pos[0] * BLOCK_SIZE, food_pos[1] * BLOCK_SIZE))

        # Draw the walls
        for wall in walls:
            win.blit(block_image, (wall[0] * BLOCK_SIZE, wall[1] * BLOCK_SIZE))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                game_started = True  # Start the game when a key is pressed
                if (
                    event.key == pygame.K_UP or event.key == pygame.K_w
                ) and snake_direction[
                    1
                ] == 0:  # Prevent reversing direction
                    snake_direction = [0, -1]
                elif (
                    event.key == pygame.K_DOWN or event.key == pygame.K_s
                ) and snake_direction[1] == 0:
                    snake_direction = [0, 1]
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a and snake_direction[0] == 0:
                    snake_direction = [-1, 0]
                elif (
                    event.key == pygame.K_RIGHT
                    or event.key == pygame.K_d
                    and snake_direction[0] == 0
                ):
                    snake_direction = [1, 0]

        # Update the snake's position
        new_head = [
            snake_pos[0][0] + snake_direction[0],
            snake_pos[0][1] + snake_direction[1],
        ]

        if not game_started:
            # Display a message to prompt the user to start the game
            font = pygame.font.Font(None, 36)
            start_text = font.render("Press any key to start", True, WHITE)
            text_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            win.blit(start_text, text_rect)
            pygame.display.update()
            continue

        for block in walls:
            if new_head == block:
                game_over = True
                break

        if (
            new_head[0] < 0
            or new_head[0] >= GRID_WIDTH
            or new_head[1] < 0
            or new_head[1] >= GRID_HEIGHT
            or new_head in snake_pos[1:]
            or new_head in walls
        ):
            game_over = True

        snake_pos.insert(0, new_head)

        if new_head == food_pos:
            food_eaten += 1

        else:
            snake_pos.pop()

        if food_eaten >= 10:
            level += 1
            food_eaten = 0
            FPS *= 1.1
            generate_walls()

        # Inside the game loop
        if new_head == food_pos:
            food_eaten += 1

            food_pos = [
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1),
            ]

        pygame.display.update()
        clock.tick(FPS)

    # Game over screen
    font = pygame.font.Font(None, 36)
    game_over_text = font.render("Game Over, Press enter to restart", True, WHITE)
    text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    win.blit(game_over_text, text_rect)
    pygame.display.update()

    # Wait for the user to press Enter
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main(win, level=1)


pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
main(win)
