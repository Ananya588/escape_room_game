import pygame

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GROUND_Y = HEIGHT - 20

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Escape Room - Sample")
clock = pygame.time.Clock()

# Player class with acceleration-based movement
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

        self.vel_x = 0
        self.vel_y = 0
        self.acceleration = 0.5
        self.max_speed = 5
        self.friction = -0.2
        self.gravity = 0.5
        self.jump_strength = -10
        self.on_ground = False

    def update(self, keys, left_key, right_key, jump_key):
        # Horizontal movement with acceleration
        if keys[left_key]:
            self.vel_x -= self.acceleration
        if keys[right_key]:
            self.vel_x += self.acceleration

        # Clamp horizontal speed
        if self.vel_x > self.max_speed:
            self.vel_x = self.max_speed
        if self.vel_x < -self.max_speed:
            self.vel_x = -self.max_speed

        # Apply friction
        if not keys[left_key] and not keys[right_key]:
            if self.vel_x > 0:
                self.vel_x += self.friction
                if self.vel_x < 0: self.vel_x = 0
            elif self.vel_x < 0:
                self.vel_x -= self.friction
                if self.vel_x > 0: self.vel_x = 0

        # Gravity
        if not self.on_ground:
            self.vel_y += self.gravity

        # Jump
        if self.on_ground and keys[jump_key]:
            self.vel_y = self.jump_strength
            self.on_ground = False

        # Update position
        self.rect.x += int(self.vel_x)
        self.rect.y += int(self.vel_y)

        # Simple ground collision
        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.vel_y = 0
            self.on_ground = True

# Create players
playerA = Player(100, GROUND_Y - 60, BLUE)
playerB = Player(200, GROUND_Y - 60, RED)
all_sprites = pygame.sprite.Group(playerA, playerB)

def show_tutorial():
    showing = True
    font = pygame.font.SysFont(None, 32)
    big_font = pygame.font.SysFont(None, 48)

    while showing:
        screen.fill((30, 30, 30))

        # Title
        title = big_font.render("Welcome to Quantum Escape!", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

        # Instructions
        instructions = [
            "Player A (Blue):",
            "  - Move Left/Right: A / D",
            "  - Jump: W",
            "",
            "Player B (Red):",
            "  - Move Left/Right: Left / Right Arrows",
            "  - Jump: Up Arrow",
            "",
            "Both players must reach the green platform.",
            "Press ENTER to start."
        ]

        for i, line in enumerate(instructions):
            text = font.render(line, True, (200, 200, 200))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 160 + i * 30))

        pygame.display.flip()

        # Wait for ENTER key
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    showing = False
show_tutorial()


# Game loop
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    playerA.update(keys, pygame.K_a, pygame.K_d, pygame.K_w)        # WASD
    playerB.update(keys, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP)  # Arrows

    # Drawing
    screen.fill(WHITE)
    pygame.draw.rect(screen, (0, 200, 0), (0, GROUND_Y, WIDTH, 20))  # Ground
    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
