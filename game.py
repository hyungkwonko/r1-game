import pygame
import random

# Initialize pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
MISSILE_WIDTH = 50
MISSILE_HEIGHT = 20
GROUND_LEVEL = SCREEN_HEIGHT - PLAYER_HEIGHT - 50  # Ground level 50px from bottom
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
FPS = 60

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dodge the Missiles!")

# Clock object to control the frame rate
clock = pygame.time.Clock()


# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = GROUND_LEVEL
        self.jump = False
        self.velocity_y = 0

    def update(self):
        # Gravity
        if self.jump:
            self.velocity_y += 1  # Gravity effect
            self.rect.y += self.velocity_y
            if self.rect.y >= GROUND_LEVEL:
                self.rect.y = GROUND_LEVEL
                self.jump = False
                self.velocity_y = 0

    def handle_jump(self):
        if not self.jump:  # Only jump if not already jumping
            self.jump = True
            self.velocity_y = -15  # Jump strength


# Missile class
class Missile(pygame.sprite.Sprite):
    def __init__(self, missile_speed):
        super().__init__()
        self.image = pygame.Surface((MISSILE_WIDTH, MISSILE_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = (
            GROUND_LEVEL + (PLAYER_HEIGHT - MISSILE_HEIGHT) // 2
        )  # Align missile to player
        self.missile_speed = missile_speed

    def update(self):
        self.rect.x -= self.missile_speed
        if self.rect.right < 0:
            self.rect.x = SCREEN_WIDTH


# Difficulty selection screen
def difficulty_selection():
    font = pygame.font.SysFont(None, 48)
    selected = None

    while selected is None:
        screen.fill(GRAY)
        easy_text = font.render("1. Easy", True, WHITE)
        medium_text = font.render("2. Medium", True, WHITE)
        hard_text = font.render("3. Hard", True, WHITE)
        screen.blit(easy_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 3))
        screen.blit(medium_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 3 + 50))
        screen.blit(hard_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 3 + 100))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected = "easy"
                elif event.key == pygame.K_2:
                    selected = "medium"
                elif event.key == pygame.K_3:
                    selected = "hard"

    return selected


# Main game function
def main_game(difficulty):
    player = Player()
    missiles = pygame.sprite.Group()

    if difficulty == "easy":
        missile_speed = 5
        spawn_rate = 120  # Spawn a missile every 2 seconds
    elif difficulty == "medium":
        missile_speed = 7
        spawn_rate = 80  # Spawn a missile every ~1.33 seconds
    elif difficulty == "hard":
        missile_speed = 10
        spawn_rate = 50  # Spawn a missile every ~0.83 seconds

    player_group = pygame.sprite.Group()
    player_group.add(player)

    lives = 3
    font = pygame.font.SysFont(None, 36)
    frame_count = 0  # To control missile spawn rate

    running = True
    while running:
        screen.fill(GRAY)  # Background color - Light gray

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.handle_jump()

        # Update player and missiles
        player_group.update()
        missiles.update()

        # Check for collisions
        if pygame.sprite.spritecollide(player, missiles, False):
            lives -= 1
            if lives == 0:
                running = False

        # Spawn new missiles
        frame_count += 1
        if frame_count % spawn_rate == 0:
            missile = Missile(missile_speed)
            missiles.add(missile)

        # Draw ground line
        pygame.draw.line(
            screen,
            BLACK,
            (0, GROUND_LEVEL + PLAYER_HEIGHT),
            (SCREEN_WIDTH, GROUND_LEVEL + PLAYER_HEIGHT),
            5,
        )

        # Draw everything
        player_group.draw(screen)
        missiles.draw(screen)

        # Display lives
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(lives_text, (10, 10))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

    pygame.quit()


# Run the game
if __name__ == "__main__":
    difficulty = difficulty_selection()  # Show difficulty selection screen
    main_game(difficulty)  # Start the game with the selected difficulty
